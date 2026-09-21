# Hospital Readmission Risk Prediction

An Explainable AI-powered Hospital Readmission Risk Prediction System. The
application predicts 30-day readmission risk and provides rule-based
explanations through a protected AI Assistant service.

## Architecture

```text
Frontend → Backend → ML API
                    → AI Assistant
```

The frontend calls only the backend. The backend validates patient inputs,
requests the model prediction, and requests an explanation from the AI
Assistant. The AI Assistant API key remains server-side.

## Project structure

```text
frontend/          React + Vite web application
backend/           FastAPI orchestration API
ml-api/            Standalone model prediction API
ai-assistant/      Rule-based explanation API
ml-training/       Training notebooks and model artifacts
```

## Deployed services

| Service | URL | Purpose |
|---|---|---|
| Frontend | https://hospital-readmission-frontend.onrender.com | Patient form and results UI |
| Backend | https://hospital-readmission-backend.onrender.com | API used by the frontend |
| ML API | https://readmission-ml-api.onrender.com | Loads the trained model |
| AI Assistant | https://reedmission-ai-assistant.onrender.com | Returns explanations |

## Backend API

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Backend health check |
| POST | `/api/predict` | Model prediction only |
| POST | `/api/assess` | Prediction plus AI explanation |
| POST | `/api/agent/ask` | Question proxy to the AI Assistant |

The ML API exposes:

```text
GET  /health
GET  /model-info
POST /predict
```

The AI Assistant exposes:

```text
GET  /health
POST /agent/ask
```

Every `/agent/*` request requires the `X-API-Key` header when `API_KEY` is
configured.

## Local development

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Install backend dependencies:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the four services in separate terminals from the repository root:

### AI Assistant

```powershell
cd ai-assistant
$env:API_KEY="local-test-key"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### ML API

```powershell
python -m uvicorn app.main:app --app-dir ml-api --host 127.0.0.1 --port 8002
```

### Backend

```powershell
cd backend
$env:ML_API_URL="http://127.0.0.1:8002"
$env:AI_ASSISTANT_API_URL="http://127.0.0.1:8001"
$env:AI_ASSISTANT_API_KEY="local-test-key"
$env:FRONTEND_ORIGINS="http://127.0.0.1:5173"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```powershell
cd frontend
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173/
```

Local health checks:

```text
http://127.0.0.1:8000/api/health
http://127.0.0.1:8001/health
http://127.0.0.1:8002/health
```

## Render environment variables

### Frontend service

```text
VITE_API_BASE_URL=https://hospital-readmission-backend.onrender.com
```

This is a Vite build-time variable. Redeploy the frontend after changing it.

### Backend service

```text
ML_API_URL=https://readmission-ml-api.onrender.com
AI_ASSISTANT_API_URL=https://reedmission-ai-assistant.onrender.com
AI_ASSISTANT_API_KEY=<same value as the AI Assistant API_KEY>
FRONTEND_ORIGINS=https://hospital-readmission-frontend.onrender.com
```

### AI Assistant service

```text
API_KEY=<long random secret>
```

`API_KEY` and `AI_ASSISTANT_API_KEY` must have exactly the same value. Generate
a new value locally with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

The ML API requires no custom environment variables when deployed from the
repository root.

Never commit `.env` files or API keys. Do not put the AI Assistant key in the
frontend or in a `VITE_*` variable.

## Render start commands

Backend:

```text
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
```

ML API:

```text
uvicorn app.main:app --app-dir ml-api --host 0.0.0.0 --port $PORT
```

The AI Assistant uses its Docker deployment configuration. Deploy the AI
Assistant before the backend when changing the shared API key. Redeploy the
frontend whenever `VITE_API_BASE_URL` changes.

## Validation

```powershell
cd frontend
npm run lint
npm run build

cd ..\ai-assistant
pytest
```

The model artifacts used by the ML API are stored in:

```text
ml-training/models/model_bundle.pkl
ml-training/models/preprocessor.pkl
ml-training/models/model_metadata.json
```

## Project status

- [x] Frontend assessment UI
- [x] Backend orchestration API
- [x] Standalone ML prediction API
- [x] Protected rule-based AI Assistant API
- [x] Frontend-backend integration
- [x] Local end-to-end testing
- [x] Render deployment