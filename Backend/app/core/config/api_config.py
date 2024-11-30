# app/core/config/api_config.py
from typing import Dict, Any

class APIConfig:
    PROJECT_NAME: str = "Transaction Manager"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing users, accounts, and transactions"
    API_V1_STR: str = "/api/v1"
    RATE_LIMIT_PER_MINUTE: int = 60

    @property
    def get_api_config(self) -> Dict[str, Any]:
        config = {
            "title": self.PROJECT_NAME,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "openapi_url": "/openapi.json",
            "swagger_ui_parameters": {"defaultModelsExpandDepth": -1}
        }
        if not isinstance(config, dict):
            raise ValueError("API configuration must be a dictionary.")
        if not isinstance(config.get("title", ""), str) or not config["title"].strip():
            raise ValueError("Project title must be a non-empty string.")
        if not isinstance(config.get("version", ""), str) or not config["version"].strip():
            raise ValueError("Version must be a non-empty string.")
        return config
