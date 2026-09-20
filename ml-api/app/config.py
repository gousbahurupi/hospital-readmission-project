from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = REPOSITORY_ROOT / "ml-training" / "models"
MODEL_BUNDLE_PATH = MODEL_DIR / "model_bundle.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.json"
