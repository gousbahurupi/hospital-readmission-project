from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_prediction import router as prediction_router


app = FastAPI(
    title="Hospital Readmission Risk API",
    version="1.0.0",
    description="Model-estimated 30-day hospital readmission risk.",
)

app.include_router(health_router)
app.include_router(prediction_router)