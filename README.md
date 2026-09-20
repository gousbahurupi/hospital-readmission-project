# Hospital Readmission Risk Prediction

A hackathon project for predicting hospital readmission risk among
chronic disease patients using Machine Learning, a separate Backend API,
a React Frontend, and a rule-based Explainable AI Agent.

## Project Overview

This project is divided into four major modules:

1.  **Frontend** -- User interface and dashboard
2.  **Backend** -- REST API and integration layer
3.  **ML Model** -- Data preprocessing, model training, and risk
    prediction
4.  **Explainable AI Agent** -- Rule-based question answering and
    prediction explanation using a previously prepared Q&A knowledge
    base

> **Important:** The readmission target must be confirmed with the
> hackathon organizers before final model training. The mandatory
> healthcare dataset may not contain a directly documented readmission
> outcome. Do not create an artificial target without proper
> documentation and approval.

------------------------------------------------------------------------

## Main Features

-   Patient information input
-   Readmission risk prediction
-   Risk-level display
-   Model-based explanation
-   Rule-based AI question-answering agent
-   Knowledge base containing previously prepared questions and answers
-   Backend REST APIs
-   Dashboard and report presentation
-   Model evaluation and documentation of limitations

------------------------------------------------------------------------

## Technology Stack

  -----------------------------------------------------------------------
  Module                              Technology
  ----------------------------------- -----------------------------------
  Frontend                            React, Vite, JavaScript, Tailwind
                                      CSS or CSS

  Backend                             FastAPI, Python

  Machine Learning                    Pandas, NumPy, Scikit-learn

  Explainable AI Agent                Python rules, keyword/similarity
                                      matching, JSON knowledge base

  API Communication                   REST API, JSON, Axios

  Version Control                     Git and GitHub

  Database                            To be finalized based on project
                                      requirements
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Project Structure

``` text
hospital-readmission-project/
│
├── ml-training/
│   ├── dataset/
│   │   ├── raw/
│   │   └── processed/
│   ├── notebooks/
│   ├── src/
│   ├── models/
│   ├── reports/
│   ├── requirements.txt
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   └── agent/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   └── package.json
│
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## Responsibilities by Module

### 1. Frontend

The frontend team is responsible for:

-   Designing the user interface
-   Creating the patient information form
-   Displaying prediction results
-   Showing risk level and explanation
-   Creating the AI agent chat interface
-   Connecting to backend APIs
-   Making the application responsive

The frontend must use the backend URL from an environment variable.

Example:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Do not hardcode production URLs directly inside components.

------------------------------------------------------------------------

### 2. Backend

The backend team is responsible for:

-   Creating REST API endpoints
-   Validating input data
-   Connecting the frontend with the ML model
-   Integrating the Explainable AI Agent
-   Managing errors and API responses
-   Configuring CORS
-   Writing API and integration tests

Planned endpoints:

  Method   Endpoint            Purpose
  -------- ------------------- ------------------------------------------
  GET      `/api/health`       Check whether the backend is running
  POST     `/api/predict`      Generate readmission risk prediction
  POST     `/api/explain`      Generate a prediction explanation
  POST     `/api/agent/ask`    Ask a question to the AI agent
  GET      `/api/model-info`   Return model information and limitations

The endpoint names may be updated after the team finalizes the API
contract.

------------------------------------------------------------------------

### 3. ML Model

The ML team is responsible for:

-   Inspecting and validating the mandatory dataset
-   Checking missing values and duplicate records
-   Performing exploratory data analysis
-   Confirming the actual prediction target
-   Preparing the preprocessing pipeline
-   Training and comparing models
-   Evaluating the model
-   Saving the final model and preprocessing pipeline
-   Providing feature importance or other explanation data

Recommended evaluation metrics:

-   Precision
-   Recall
-   F1-score
-   ROC-AUC
-   Confusion matrix

The model must not be trained until the target variable and its meaning
are confirmed.

------------------------------------------------------------------------

### 4. Explainable AI Agent

The Explainable AI Agent is a **rule-based system**, not a free-form
generative medical chatbot.

The agent will:

-   Store previously prepared questions and answers
-   Match a user's question with the knowledge base
-   Use keyword matching or similarity-based retrieval
-   Apply predefined rules to explain prediction results
-   Provide information about risk factors and model limitations
-   Return a safe fallback when no reliable answer is found
-   Avoid making diagnoses or unsupported medical recommendations

Example knowledge base format:

``` json
[
  {
    "question": "What does high readmission risk mean?",
    "keywords": ["high risk", "readmission risk"],
    "answer": "A high predicted risk indicates that the model identified patterns associated with increased readmission risk. It is not a medical diagnosis.",
    "category": "prediction_explanation"
  }
]
```

All medical or clinical statements must be reviewed and approved by the
team before being added to the knowledge base.

------------------------------------------------------------------------

## Local Setup

### Prerequisites

Install the following tools:

-   Git
-   Python 3.11 or a compatible supported version
-   Node.js and npm
-   VS Code
-   A Kaggle account for downloading the mandatory dataset

------------------------------------------------------------------------

## Backend Setup

Open a terminal in the `backend` folder.

### 1. Create a virtual environment

Windows PowerShell:

``` powershell
python -m venv .venv
```

### 2. Activate the environment

``` powershell
.venv\Scripts\activate
```

### 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

### 4. Run the backend

``` powershell
uvicorn app.main:app --reload
```

The API will normally be available at:

``` text
http://127.0.0.1:8000
```

Swagger API documentation:

``` text
http://127.0.0.1:8000/docs
```

If PowerShell blocks `npm` or another script, use the appropriate
Windows command wrapper or update the execution policy only for the
current user after reviewing the security implications.

------------------------------------------------------------------------

## Frontend Setup

Open a terminal in the `frontend` folder.

### 1. Install dependencies

``` powershell
npm.cmd install
```

### 2. Start the frontend

``` powershell
npm.cmd run dev
```

The frontend will normally be available at:

``` text
http://localhost:5173
```

### 3. Configure the backend URL

Create a `.env` file in the frontend folder:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart the frontend development server after changing environment
variables.

------------------------------------------------------------------------

## ML Training Setup

Open a terminal in the `ml-training` folder.

### 1. Create a virtual environment

``` powershell
python -m venv .venv
```

### 2. Activate the environment

``` powershell
.venv\Scripts\activate
```

### 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

### 4. Dataset location

Place the downloaded dataset in:

``` text
ml-training/dataset/raw/
```

Do not upload the raw dataset, virtual environment, secrets, or private
credentials to GitHub unless the team has verified that sharing is
permitted.

------------------------------------------------------------------------

## Git Collaboration Workflow

Before starting work:

``` bash
git pull origin main
```

Create a separate branch for your task:

``` bash
git checkout -b feature/your-task-name
```

Examples:

``` bash
git checkout -b feature/frontend-dashboard
git checkout -b feature/backend-prediction-api
git checkout -b feature/ml-preprocessing
git checkout -b feature/rule-based-agent
```

After making changes:

``` bash
git status
git add .
git commit -m "Add clear description of changes"
git push -u origin feature/your-task-name
```

Create a Pull Request on GitHub and ask another team member to review
the changes before merging.

### Recommended Commit Messages

``` text
feat: add patient input form
feat: add prediction API
feat: add preprocessing pipeline
feat: add rule-based agent matching
fix: handle missing patient fields
docs: update setup instructions
test: add prediction endpoint tests
```

### Collaboration Rules

-   Do not work directly on the `main` branch unless the team agrees.
-   Pull the latest changes before starting work.
-   Keep commits small and meaningful.
-   Do not commit `.env` files containing secrets.
-   Do not commit virtual environments.
-   Communicate before modifying shared API contracts.
-   Update the README when setup instructions change.
-   Test your module before creating a Pull Request.

------------------------------------------------------------------------

## API Contract

Before frontend-backend integration, agree on request and response
formats.

### Example Prediction Request

``` json
{
  "age": 55,
  "gender": "Male",
  "medical_condition": "Diabetes",
  "admission_type": "Emergency"
}
```

This is only an example structure. The final fields must match the
verified dataset and trained model.

### Example Prediction Response

``` json
{
  "risk_level": "High",
  "risk_score": 0.78,
  "prediction": "High readmission risk",
  "important_factors": [
    "Example factor 1",
    "Example factor 2"
  ]
}
```

The actual response must be based on the trained model and finalized API
design. Do not use example values as real clinical predictions.

------------------------------------------------------------------------

## Development Workflow

``` text
Dataset Validation
        |
        v
Data Preprocessing
        |
        v
ML Model Training and Evaluation
        |
        v
Export Model and Preprocessing Pipeline
        |
        v
Backend Prediction API
        |
        v
Rule-Based Explainable AI Agent
        |
        v
Frontend Integration
        |
        v
Testing and Deployment
```

------------------------------------------------------------------------

## Definition of Done

A module is considered complete when:

-   Its code is committed to a separate Git branch.
-   It follows the agreed folder structure.
-   It has basic error handling.
-   It has been tested locally.
-   It does not expose secrets or private data.
-   Its API or module interface is documented.
-   A Pull Request has been reviewed.
-   It works with the other modules after integration testing.

------------------------------------------------------------------------

## Responsible AI and Limitations

This project is intended as a hackathon prototype and decision-support
demonstration.

-   The prediction is not a medical diagnosis.
-   The model may contain dataset bias and limitations.
-   Predictions must not replace professional medical judgment.
-   The model's target variable must be clearly defined.
-   Explanations must not claim causal relationships unless supported by
    evidence.
-   The rule-based agent must use reviewed and documented information.
-   Uncertain or unsupported questions should receive a safe fallback
    response.

------------------------------------------------------------------------

## Team Notes

Before implementation, the team must finalize:

-   The readmission target variable
-   Required patient input fields
-   Final ML algorithm
-   Model evaluation metrics
-   Backend API contract
-   Q&A knowledge base format
-   Explanation rules
-   Deployment platforms
-   Data privacy and security practices

------------------------------------------------------------------------

## Project Status

**Current status:** Initial project setup and folder structure.

Next priorities:

1.  Validate the mandatory dataset.
2.  Confirm the readmission target with the organizers.
3.  Set up the backend health endpoint.
4.  Set up the frontend application.
5.  Define the API request and response formats.
6.  Build and evaluate the ML pipeline.
7.  Develop the rule-based Explainable AI Agent.
8.  Integrate and test all modules.
