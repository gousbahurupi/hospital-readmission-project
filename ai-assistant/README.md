# Explainable AI Assistant for Hospital Readmission Risk

A FastAPI API-only service that explains a readmission-risk prediction in plain language. Your backend sends it the model output plus a question, and it answers from a reviewed knowledge base. It provides decision support and does not provide a medical diagnosis.

The assistant is rule-based on purpose: every sentence it can say lives in `app/agent/knowledge_base.json`, so clinicians can review the wording and the service never invents medical content.

## Quick start

The service has no user-facing frontend. It accepts server-to-server requests from your backend and returns JSON responses. `/health` remains public for hosting health checks.

### Docker

```bash
cp .env.example .env        # set API_KEY
docker compose up --build
```

### Local Python (3.10+)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Then open:

| URL | What |
|---|---|
| `http://localhost:8000/docs` | API documentation when explicitly enabled |
| `http://localhost:8000/health` | Health check for load balancers |

## API

Every `/agent/*` endpoint requires the `X-API-Key` header when `API_KEY` is set. Set `API_KEY` in production so only your backend can call the agent. The `/health` endpoint does not require a key.

### `POST /agent/ask`

```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "question": "Why is the risk high and what should be monitored?",
    "prediction": {
      "readmission_prediction": "LIKELY",
      "risk_probability": 72,
      "risk_level": "HIGH",
      "top_contributing_factors": ["A1C result", "Number of diagnoses", "Time in hospital", "Medication-related factors"]
    }
  }'
```

Response:

```json
{
  "answer": "The model estimates a 72% probability ...",
  "intent": "risk_explanation",
  "intents": ["risk_explanation", "monitoring"],
  "suggested_questions": ["How can the risk be reduced?", "..."],
  "prediction": { "...": "normalised copy of what you sent" },
  "disclaimer": "This system provides decision support and does not provide a medical diagnosis."
}
```

Input rules: `risk_probability` is a percentage from 0 to 100 (send `72`, not `0.72`); `risk_level` is `LOW`, `MEDIUM` (or `MODERATE`) or `HIGH`; 1 to 15 factors; the question is at most 500 characters. Extra fields in `prediction` are ignored and never echoed back.

The service is stateless: send the prediction with every question.

### Other endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/agent/report` | Standard text summary of a prediction |
| GET | `/agent/questions` | Example questions grouped by topic (for building suggestion chips) |
| GET | `/agent/sample-prediction` | A ready-made prediction for testing |
| GET | `/health` | Liveness check (no key needed) |

## What users can ask

The assistant understands these topics, in many phrasings. Two questions joined by "and" are both answered.

| Topic | Examples |
|---|---|
| The result | "Give me a summary", "What is the readmission risk?", "Will this patient be readmitted?", "What does 72% mean?", "What does HIGH risk mean?", "What does readmission mean?" |
| Why | "Why is the risk high?", "Explain the prediction", "What is driving this score?" |
| Factors | "What are the top contributing factors?", "What is the most important factor?", "What does A1C mean?", "Why does time in hospital matter?", "How do medications affect the risk?" |
| Follow-up | "What should be monitored after discharge?", "How can the risk be reduced?", "What are the next steps?" |
| The model | "How does the model work?", "How are the factors identified?", "What data does the model use?", "Can I trust this prediction?", "What are the limitations?", "What if the A1C were lower?" |
| The assistant | "What can you do?", "Who are you?", "Is patient data stored?", "Does this replace a clinician?" |

It knows A1C, number of diagnoses, time in hospital, medication-related factors, prior hospital visits, lab procedures, age, discharge destination and admission type. For any other factor your model returns, it still answers "is this one of the top factors" and says honestly that it has no further background.

### Safety behaviour

- Requests for diagnosis, treatment, medication or dosing advice, or whether a patient is ready for discharge, get a clear refusal that points to the care team.
- Emergency phrases (for example chest pain) get an instruction to contact local emergency services.
- Monitoring and care-planning answers are general considerations and say so.
- Questions it cannot match get the prediction summary instead of a guess.

## Connecting your real model

`app/ml/prediction.py` only holds a sample. Call your model in your own backend, then post its output to `/agent/ask`. If your model returns different field names, map them to the four fields above before calling.

## Extending the assistant

1. **New wording or a new factor**: edit `app/agent/knowledge_base.json` (`factor_details` needs `label`, `aliases`, `short`, `description`, `monitoring`).
2. **New phrasing for an existing topic**: add a `(regex, weight)` pattern under that intent in `app/agent/rules.py`. Patterns run on lower-case text with punctuation removed ("follow-up" becomes "follow up", "72%" becomes "72 percent").
3. **New topic**: add the intent to `INTENT_PATTERNS` and `PRIORITY` in `rules.py`, a handler in `_HANDLERS` in `agent_service.py`, its text in the knowledge base, and follow-ups under `follow_ups`.
4. Add the question to `tests/test_rules.py` and run the tests.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/test_rules.py` checks about 70 phrasings against their intended topic. It also checks that every example in the knowledge base and every suggested follow-up is understood by the rules.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `API_KEY` | empty | If set, required in the `X-API-Key` header for `/agent/*` |
| `CORS_ORIGINS` | empty | Comma-separated browser origins allowed to call the API |
| `ENABLE_DOCS` | `false` | Serve `/docs` and `/openapi.json` |
| `LOG_LEVEL` | `INFO` | Python log level |
| `PORT` | `8000` | Port the container listens on (hosts like Render, Railway and Cloud Run set this) |
| `WEB_CONCURRENCY` | `1` | Number of uvicorn workers |

## Deploying

The Docker image works on any container host: Render, Railway, Fly.io, Google Cloud Run, AWS App Runner or ECS, Azure Container Apps, or your own server.

1. Build and push the image, or connect the repository so the host builds the `Dockerfile`.
2. Set `API_KEY` to a long random value (`python -c "import secrets; print(secrets.token_urlsafe(32))"`).
3. Set the health check path to `/health`.
4. Serve it over HTTPS (the hosts above do this for you).

### Before going live in a clinical setting

- Keep `API_KEY` set and call the service from your backend, so the key never reaches a browser. Rotate it if it leaks.
- Keep `ENABLE_DOCS=false` in production unless you need interactive API documentation.
- Run behind your organisation's gateway if you need rate limiting, SSO or audit logs. This service does not include them.
- The application logs only the detected topic and status, never the question or the prediction. Your proxy or host may log request bodies, so check that too.
- Have a clinician review `knowledge_base.json` and confirm the risk-level wording matches how your model defines its levels.
- This project has not been clinically validated and is not a medical device. Check the regulatory position for your region before using it with patients.

## Project layout

```
app/
  main.py                FastAPI app, /health, security headers
  api/agent.py           /agent/* routes
  api/schemas.py         request and response validation
  agent/rules.py         intent detection (weighted patterns)
  agent/agent_service.py answer generation
  agent/knowledge.py     knowledge base loader and factor lookup
  agent/knowledge_base.json  all assistant wording
  agent/text.py          text normalisation
  core/config.py         environment settings
  core/security.py       optional API-key check
  ml/prediction.py       sample prediction (replace with your model)
tests/                   pytest suite
Dockerfile, docker-compose.yml, requirements*.txt, .env.example
```
