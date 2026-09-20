"""Runtime settings, read from environment variables.

Nothing here is secret by default. Set API_KEY to require an X-API-Key header
on every /agent/* request.
"""

import os
from dataclasses import dataclass


def _flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    version: str
    api_key: str | None
    cors_origins: list[str]
    enable_docs: bool
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
        return cls(
            app_name="Explainable AI Assistant",
            version="2.0",
            api_key=(os.getenv("API_KEY") or "").strip() or None,
            cors_origins=origins,
            enable_docs=_flag("ENABLE_DOCS", False),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


def get_settings() -> Settings:
    # Read on every call so tests and container restarts pick up changes.
    return Settings.from_env()
