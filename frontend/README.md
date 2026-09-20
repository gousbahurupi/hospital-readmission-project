
# Hospital Readmission Risk Prediction

An Explainable AI-powered Hospital Readmission Risk Prediction System.

The project uses Machine Learning to predict hospital readmission risk and an Explainable AI Agent to provide understandable explanations and guidance.

---

## Project Structure

```text
hospital-readmission-project/
│
├── frontend/          # React + Vite frontend
├── backend/           # FastAPI backend
├── ml-training/       # ML model training and evaluation
└── README.md
```

---

## Technology Stack

### Frontend
- React
- Vite
- JavaScript
- Tailwind CSS (planned)
- Axios / Fetch API

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn

### Explainable AI Agent
- Rule-based explanation engine
- Q&A knowledge base

---

## Prerequisites

Install the following software:

1. Node.js and npm
2. Python 3.11 or compatible Python version
3. Git
4. Visual Studio Code

Verify the installation:

```bash
node --version
npm --version
python --version
git --version
```

---

# Frontend Setup

## 1. Navigate to the frontend folder

```powershell
cd frontend
```

## 2. Install dependencies

Run this command if dependencies have not been installed:

```powershell
npm install
```

## 3. Start the frontend development server

```powershell
npm run dev
```

Frontend URL:

http://localhost:5173/

## 4. Stop the frontend server

Press:

```text
Ctrl + C
```

---

# Backend Setup

## 1. Navigate to the backend folder

From the project root:

```powershell
cd backend
```

## 2. Create a Python virtual environment

```powershell
python -m venv venv
```

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

## 4. Install backend dependencies

```powershell
pip install -r requirements.txt
```

## 5. Start the backend server

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend URL:

http://127.0.0.1:8000/

API documentation:

http://127.0.0.1:8000/docs

## 6. Stop the backend server

Press:

```text
Ctrl + C
```

---

# Running Frontend and Backend Together

Open two separate terminals in VS Code.

### Terminal 1 — Frontend

```powershell
cd frontend
npm run dev
```

Frontend:

http://localhost:5173/

### Terminal 2 — Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Backend:

http://127.0.0.1:8000/

---

# Development Workflow

## Step 1: Pull the latest changes

```powershell
git pull origin main
```

## Step 2: Create a new branch

```powershell
git checkout -b feature/your-feature-name
```

Example:

```powershell
git checkout -b feature/patient-form
```

## Step 3: Make your changes

Work only on your assigned feature.

## Step 4: Check your changes

```powershell
git status
```

## Step 5: Stage changes

```powershell
git add .
```

## Step 6: Commit changes

```powershell
git commit -m "Add patient input form"
```

## Step 7: Push your branch

```powershell
git push -u origin feature/your-feature-name
```

## Step 8: Create a Pull Request

Open GitHub and create a Pull Request from your feature branch into `main`.

---

# Team Development Rules

1. Pull the latest code before starting work.
2. Create a separate branch for each feature.
3. Do not directly modify another team member's work without discussion.
4. Do not commit passwords, API keys, or `.env` files.
5. Test your changes before pushing.
6. Use meaningful commit messages.
7. Inform the team before changing shared files or APIs.

---

# Important Commands

| Purpose | Command |
|---|---|
| Install frontend dependencies | `npm install` |
| Start frontend | `npm run dev` |
| Create backend environment | `python -m venv venv` |
| Activate environment | `.\venv\Scripts\Activate.ps1` |
| Install backend dependencies | `pip install -r requirements.txt` |
| Start backend | `uvicorn app.main:app --reload --port 8000` |
| Check Git status | `git status` |
| Pull changes | `git pull origin main` |
| Create branch | `git checkout -b feature/name` |
| Commit changes | `git commit -m "message"` |
| Push branch | `git push -u origin branch-name` |

---

# Project Modules

- Frontend Dashboard
- Patient Data Input
- Readmission Risk Prediction
- Explainable AI Agent
- Model Evaluation
- API Integration
- Testing and Deployment

---

# Team Collaboration

Before starting a new feature:

1. Discuss the feature with the team.
2. Assign responsibility.
3. Create a feature branch.
4. Implement and test the feature.
5. Push the changes.
6. Review and merge the Pull Request.

---

## Project Status

Current Phase: Initial Project Setup

- [x] Frontend Vite setup
- [ ] Backend FastAPI setup
- [ ] ML model integration
- [ ] Explainable AI Agent
- [ ] Frontend-backend integration
- [ ] Testing
- [ ] Deployment
