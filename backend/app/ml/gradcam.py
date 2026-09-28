"""
gradcam.py
----------
Grad-CAM (Gradient-weighted Class Activation Mapping) for the trained
brain tumor CNN.

Produces:
  - a raw heatmap (numpy array, 0-1)
  - an overlay image (heatmap blended over the original MRI)

IMPORTANT (per project requirements): Grad-CAM output shows which regions
influenced the model's prediction. It is NOT a segmentation mask and does
NOT draw a tumor boundary. This must always be surfaced with the
disclaimer defined in DISCLAIMER_TEXT below, both here and in the API/UI.
"""
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

DISCLAIMER_TEXT = (
    "The highlighted region shows areas that contributed to the model's "
    "prediction. It is not a confirmed tumor boundary or medical diagnosis."
)


class GradCAM:
    """Generic Grad-CAM wrapper that works for ResNet-style and the
    custom Sequential CNN defined in train.py, by hooking the last
    convolutional layer."""

    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, inp, out):
            self.activations = out.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate(self, input_tensor, class_idx=None):
        self.model.zero_grad()
        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()

        score = output[:, class_idx]
        score.backward()

        gradients = self.gradients[0]          # (C, H, W)
        activations = self.activations[0]       # (C, H, W)
        weights = gradients.mean(dim=(1, 2))     # (C,)

        cam = torch.zeros(activations.shape[1:], dtype=torch.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i]

        cam = F.relu(cam)
        cam = cam - cam.min()
        if cam.max() > 0:
            cam = cam / cam.max()
        return cam.cpu().numpy(), class_idx, F.softmax(output, dim=1)[0].detach().cpu().numpy()


def find_last_conv_layer(model):
    """Walks the model to find the last nn.Conv2d layer (works for both
    resnet18 and the custom architecture in train.py)."""
    last_conv = None
    for module in model.modules():
        if isinstance(module, torch.nn.Conv2d):
            last_conv = module
    if last_conv is None:
        raise ValueError("No Conv2d layer found in model.")
    return last_conv


def preprocess_image(pil_image: Image.Image, img_size: int = 224):
    tf = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225]),
    ])
    tensor = tf(pil_image).unsqueeze(0)
    return tensor


def overlay_heatmap(pil_image: Image.Image, cam: np.ndarray, img_size: int = 224, alpha: float = 0.45):
    """Returns (heatmap_rgb, overlay_rgb) as PIL Images, both resized to img_size."""
    base = pil_image.convert("RGB").resize((img_size, img_size))
    base_np = np.array(base)

    cam_resized = cv2.resize(cam, (img_size, img_size))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    overlay = (heatmap * alpha + base_np * (1 - alpha)).astype(np.uint8)

    return Image.fromarray(heatmap), Image.fromarray(overlay)


def run_gradcam(model, pil_image: Image.Image, img_size: int = 224, class_idx=None):
    """High-level convenience function used by the FastAPI backend.

    Returns dict with: predicted_class_idx, probabilities, heatmap_img,
    overlay_img, disclaimer.
    """
    model.eval()
    target_layer = find_last_conv_layer(model)
    cam_engine = GradCAM(model, target_layer)

    input_tensor = preprocess_image(pil_image, img_size)
    input_tensor.requires_grad_(True)

    cam, pred_idx, probs = cam_engine.generate(input_tensor, class_idx=class_idx)
    heatmap_img, overlay_img = overlay_heatmap(pil_image, cam, img_size)

    return {
        "predicted_class_idx": pred_idx,
        "probabilities": probs,
        "heatmap_img": heatmap_img,
        "overlay_img": overlay_img,
        "disclaimer": DISCLAIMER_TEXT,
    }
