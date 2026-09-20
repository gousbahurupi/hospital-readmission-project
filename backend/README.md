# Hospital Readmission Risk Prediction — Backend

## Overview

This is the backend service for the **Hospital Readmission Risk Prediction** project. It provides APIs to connect the frontend application with the Machine Learning model and the Rule-Based Explainable AI Agent.

The backend is responsible for request handling, data validation, prediction integration, explanation generation, and communication between the project modules.

## Project Architecture

The backend is organized into the following modules:

* **API:** Handles HTTP requests and responses.
* **Schemas:** Validates API input and output data.
* **Services:** Contains application business logic.
* **ML:** Handles model prediction and preprocessing.
* **Agent:** Implements the rule-based Explainable AI Agent.
* **Tests:** Contains backend tests.

## Technology Stack

* Python
* FastAPI
* Uvicorn
* Scikit-learn
* Pandas
* NumPy
* Pydantic
* Joblib

## Project Structure

```text
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_health.py
│   │   ├── routes_prediction.py
│   │   └── routes_agent.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── prediction_schema.py
│   │   └── agent_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prediction_service.py
│   │   └── agent_service.py
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── preprocessing.py
│   │
│   └── agent/
│       ├── __init__.py
│       ├── rules.py
│       ├── matcher.py
│       └── knowledge_base.json
│
├── tests/
├── requirements.txt
└── README.md
```

## Planned API Endpoints

| Method | Endpoint          | Purpose                                   |
| ------ | ----------------- | ----------------------------------------- |
| GET    | `/api/health`     | Check backend availability                |
| POST   | `/api/predict`    | Generate readmission risk prediction      |
| POST   | `/api/explain`    | Generate an explanation of the prediction |
| POST   | `/api/agent/ask`  | Ask a question to the rule-based AI agent |
| GET    | `/api/model-info` | Return model information and limitations  |

*Endpoints will be implemented and updated during development.*

## Explainable AI Agent

The Explainable AI Agent will use a **rule-based approach** with a predefined question-and-answer knowledge base.

The agent will:

1. Receive a user's question.
2. Process and match the question with existing questions.
3. Retrieve relevant answers from the knowledge base.
4. Apply predefined rules to explain model predictions.
5. Provide a fallback response when no suitable answer is found.

The agent is intended to provide understandable explanations and educational information. It is not a replacement for professional medical judgment.

## Development Setup

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment on Windows

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend

```bash
uvicorn app.main:app --reload
```

### 5. Open API Documentation

```text
http://127.0.0.1:8000/docs
```

## Model Deployment

The API loads these artifacts from `ml-training/models/` at startup:

```text
model_bundle.pkl
preprocessor.pkl
model_metadata.json
```

From the repository root, install dependencies and start the service:

```powershell
cd D:\hospital-readmission-project\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The prediction endpoint is:

```text
POST http://127.0.0.1:8000/api/predict
```

Example request:

```json
{
  "age": "[70-80)",
  "gender": "Female",
  "admission_type_id": 1,
  "admission_source_id": 7,
  "discharge_disposition_id": 1,
  "diag_1_group": "Circulatory",
  "diag_2_group": "Diabetes",
  "diag_3_group": "Other",
  "A1Cresult": "None",
  "max_glu_serum": "None",
  "diabetesMed": "Yes",
  "change": "No",
  "insulin": "No",
  "time_in_hospital": 4,
  "num_lab_procedures": 40,
  "num_procedures": 1,
  "num_medications": 12,
  "number_diagnoses": 7
}
```

The response includes the model-estimated probability, saved decision threshold,
binary prediction, and human-readable label. The endpoint applies the saved
preprocessor before calling the model; clients must send the raw feature fields
shown above rather than encoded feature columns.

## Environment Configuration

Environment-specific settings should be stored in a `.env` file and should not be committed to the repository.

Examples of configuration values may include:

* Application environment
* Database connection
* Frontend origin
* Model path

## Development Guidelines

* Follow a modular project structure.
* Validate API inputs using schemas.
* Keep model training separate from prediction serving.
* Write reusable service functions.
* Test API endpoints before integration.
* Do not commit credentials, private keys, or sensitive data.
* Document major changes in Git commits.

## Important Project Consideration

The readmission target must be confirmed before developing the final prediction model. The selected healthcare dataset should be inspected to verify that it contains a valid readmission outcome or that an approved target-generation methodology is available.

## Project Status

**Current Status:** Initial backend folder structure created.

Upcoming tasks:

* Configure FastAPI application.
* Implement health-check endpoint.
* Define API schemas.
* Integrate the ML prediction pipeline.
* Implement the rule-based Explainable AI Agent.
* Connect the frontend and backend.
* Add testing and deployment configuration.

## Licensex

This project is developed for educational and hackathon purposes.
