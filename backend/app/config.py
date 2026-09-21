from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "ml-training" / "models"
MODEL_BUNDLE_PATH = MODEL_DIR / "model_bundle.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.json"
ML_API_URL = os.getenv("ML_API_URL", "https://readmission-ml-api.onrender.com").rstrip("/")
AI_ASSISTANT_API_URL = os.getenv(
    "AI_ASSISTANT_API_URL",
    "https://reedmission-ai-assistant.onrender.com",
).rstrip("/")
AI_ASSISTANT_API_KEY = os.getenv("AI_ASSISTANT_API_KEY", "")
FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]