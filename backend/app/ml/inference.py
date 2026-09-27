"""
Loads the trained CNN (produced by ml/train.py) and runs prediction +
Grad-CAM for the API.

If no trained model checkpoint exists yet (ml/models/best_model.pth), this
module falls back to an UNTRAINED randomly-initialized network so the rest
of the application (upload -> predict -> explain -> report -> history) can
be demonstrated end-to-end without requiring training to finish first.
Every response in that fallback mode is explicitly flagged
`"is_placeholder": true` and the confidence/class values must be treated
as non-meaningful -- per the "do not use fake accuracy values" and
"clearly label demo/placeholder" requirements. Train a real model
(python ml/train.py) and this flag flips to false automatically.
"""
import json
import sys
from pathlib import Path

import torch
from PIL import Image

# Make ml/ importable (train.py, gradcam.py live there, one level up from backend/)
ML_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ml"
sys.path.insert(0, str(ML_DIR))

from train import build_model, CLASSES, IMG_SIZE  # noqa: E402
from gradcam import run_gradcam, DISCLAIMER_TEXT   # noqa: E402

from app.core.config import settings

_model = None
_is_placeholder = True
_arch = "resnet18"


def _load_model():
    global _model, _is_placeholder, _arch
    if _model is not None:
        return _model

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if settings.MODEL_PATH.exists():
        checkpoint = torch.load(settings.MODEL_PATH, map_location=device)
        _arch = checkpoint.get("arch", "resnet18")
        model = build_model(_arch, len(CLASSES))
        model.load_state_dict(checkpoint["model_state_dict"])
        _is_placeholder = False
        print(f"[inference] Loaded trained model from {settings.MODEL_PATH}")
    else:
        model = build_model(_arch, len(CLASSES))
        _is_placeholder = True
        print("[inference] WARNING: no trained checkpoint found -- serving "
              "UNTRAINED placeholder model. Run ml/train.py to train a real one.")

    model.to(device)
    model.eval()
    _model = model
    return _model


def get_model_status() -> dict:
    _load_model()
    metrics = None
    if settings.METRICS_PATH.exists():
        with open(settings.METRICS_PATH) as f:
            metrics = json.load(f)
    return {
        "is_placeholder": _is_placeholder,
        "architecture": _arch,
        "classes": CLASSES,
        "metrics": metrics,
    }


def predict_with_explanation(image_path: str, save_heatmap_to: str, save_overlay_to: str) -> dict:
    model = _load_model()
    pil_image = Image.open(image_path).convert("RGB")

    result = run_gradcam(model, pil_image, img_size=IMG_SIZE)

    heatmap_img = result["heatmap_img"]
    overlay_img = result["overlay_img"]
    heatmap_img.save(save_heatmap_to)
    overlay_img.save(save_overlay_to)

    probs = result["probabilities"]
    class_probs = {cls: float(p) for cls, p in zip(CLASSES, probs)}
    predicted_class = CLASSES[result["predicted_class_idx"]]
    confidence = float(probs[result["predicted_class_idx"]])

    return {
        "predicted_class": predicted_class,
        "confidence_score": confidence,
        "all_class_probabilities": class_probs,
        "is_placeholder": _is_placeholder,
        "disclaimer": DISCLAIMER_TEXT,
    }
