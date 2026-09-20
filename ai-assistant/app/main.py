import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router
from app.core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title=settings.app_name,
    description="AI assistant for hospital readmission risk explanation",
    version=settings.version,
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-API-Key"],
    )


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.url.path.startswith("/agent"):
        response.headers["Cache-Control"] = "no-store"
    return response


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Explainable AI Assistant API is running",
        "version": settings.version,
        "docs": "/docs" if settings.enable_docs else None,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
