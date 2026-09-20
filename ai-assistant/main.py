from fastapi import FastAPI

from app.api.agent import router


app = FastAPI(
    title="Explainable AI Assistant",
    description="AI assistant for hospital readmission risk explanation",
    version="1.0"
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Explainable AI Assistant API is running"
    }