from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import HTTPException

from app.core.config import settings
from app.core.database import Base, engine
from app.models import models  # noqa: F401 -- ensures models are registered before create_all
from app.routers import auth, cases, predictions, reports, models_router, health

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Research/educational MRI decision-support system: CNN prediction, "
                "Grad-CAM explainability, and an AI-assisted draft report reviewed by a "
                "doctor/researcher before being finalized. NOT an autonomous diagnostic tool.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(predictions.router)
app.include_router(reports.router)
app.include_router(models_router.router)


@app.get("/api/files/{file_path:path}")
def serve_file(file_path: str):
    """Serves uploaded MRI images and generated Grad-CAM heatmaps/overlays.
    file_path is the absolute path stored on the Prediction/MRIImage rows."""
    path = Path("/" + file_path) if not file_path.startswith("/") else Path(file_path)
    if not path.exists() or not str(path).startswith(str(settings.UPLOAD_DIR)):
        raise HTTPException(404, "File not found")
    return FileResponse(path)


@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "docs": "/docs",
        "disclaimer": "Research and educational decision-support tool only. Not an "
                       "autonomous diagnostic device.",
    }
