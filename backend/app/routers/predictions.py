import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.audit import log_action
from app.models.models import MRIImage, Prediction, ModelVersion, User
from app.schemas.schemas import PredictionOut
from app.ml.inference import predict_with_explanation, DISCLAIMER_TEXT

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


class PredictRequest(BaseModel):
    image_id: str


def _get_or_create_model_version(db: Session) -> ModelVersion:
    """Registers the currently loaded model as a ModelVersion row the
    first time it's used, so predictions always reference a model_version_id
    (required for the audit trail / Admin > Model Management module)."""
    from app.ml.inference import get_model_status
    status_info = get_model_status()
    tag = f"{status_info['architecture']}-{'placeholder' if status_info['is_placeholder'] else 'trained'}"

    mv = db.query(ModelVersion).filter(ModelVersion.version_tag == tag).first()
    if mv:
        return mv

    metrics = status_info.get("metrics") or {}
    test_metrics = metrics.get("test_metrics", {})
    mv = ModelVersion(
        version_tag=tag,
        architecture=status_info["architecture"],
        dataset_info="Kaggle Brain Tumor MRI Dataset (Nickparvar) - glioma/meningioma/pituitary/notumor",
        accuracy=test_metrics.get("accuracy"),
        precision_macro=test_metrics.get("precision_macro"),
        recall_macro=test_metrics.get("recall_macro"),
        f1_macro=test_metrics.get("f1_macro"),
        is_placeholder=status_info["is_placeholder"],
        deployment_status="active",
    )
    db.add(mv)
    db.commit()
    db.refresh(mv)
    return mv


@router.post("", response_model=PredictionOut, status_code=201)
def create_prediction(payload: PredictRequest, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    image = db.query(MRIImage).filter(MRIImage.id == payload.image_id).first()
    if not image:
        raise HTTPException(404, "MRI image not found")

    model_version = _get_or_create_model_version(db)

    heatmap_path = image.file_path.rsplit(".", 1)[0] + "_heatmap.png"
    overlay_path = image.file_path.rsplit(".", 1)[0] + "_overlay.png"

    result = predict_with_explanation(image.file_path, heatmap_path, overlay_path)

    prediction = Prediction(
        case_id=image.case_id,
        image_id=image.id,
        model_version_id=model_version.id,
        predicted_class=result["predicted_class"],
        confidence_score=result["confidence_score"],
        all_class_probabilities=json.dumps(result["all_class_probabilities"]),
        heatmap_path=heatmap_path,
        overlay_path=overlay_path,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    log_action(db, current_user.id, "RUN_PREDICTION", "Prediction", prediction.id,
               details=f"placeholder_model={result['is_placeholder']}")

    return _to_prediction_out(prediction, result["disclaimer"], model_version.version_tag)


@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(prediction_id: str, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(404, "Prediction not found")
    return _to_prediction_out(prediction, DISCLAIMER_TEXT, prediction.model_version.version_tag)


@router.get("/{prediction_id}/explanation")
def get_explanation(prediction_id: str, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(404, "Prediction not found")
    return {
        "prediction_id": prediction.id,
        "predicted_class": prediction.predicted_class,
        "confidence_score": prediction.confidence_score,
        "heatmap_url": f"/api/files/{prediction.heatmap_path}",
        "overlay_url": f"/api/files/{prediction.overlay_path}",
        "disclaimer": DISCLAIMER_TEXT,
    }


def _to_prediction_out(prediction: Prediction, disclaimer: str, model_tag: str) -> PredictionOut:
    return PredictionOut(
        id=prediction.id,
        case_id=prediction.case_id,
        predicted_class=prediction.predicted_class,
        confidence_score=prediction.confidence_score,
        all_class_probabilities=json.loads(prediction.all_class_probabilities),
        heatmap_url=f"/api/files/{prediction.heatmap_path}" if prediction.heatmap_path else None,
        overlay_url=f"/api/files/{prediction.overlay_path}" if prediction.overlay_path else None,
        disclaimer=disclaimer,
        model_version=model_tag,
        predicted_at=prediction.predicted_at,
    )
