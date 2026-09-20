# Standalone Hospital Readmission ML API

This service loads the trained artifacts from `ml-training/models/` and exposes
the model independently from the main backend.

## Local run

From the repository root:

```powershell
cd D:\hospital-readmission-project\ml-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Render deployment

Configure a Render Web Service with:

```text
Root Directory: .
Build Command: pip install -r ml-api/requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The repository root must be used so the service can access:

```text
ml-training/models/model_bundle.pkl
ml-training/models/preprocessor.pkl
```

## Endpoints

```text
GET  /health
GET  /model-info
POST /predict
```

The `/predict` endpoint accepts the raw 18-feature input used by the saved
preprocessor and returns the model-estimated probability, saved threshold,
prediction, and label.
