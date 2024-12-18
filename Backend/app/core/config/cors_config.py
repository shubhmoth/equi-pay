# app/core/config/cors_config.py
from typing import List
import os

class CORSConfig:
    @property
    def get_cors_origins(self) -> List[str]:
        environment = os.getenv("ENVIRONMENT", "development")
        if not isinstance(environment, str) or not environment.strip():
            raise ValueError("Environment variable 'ENVIRONMENT' must be a non-empty string.")
        return ["*"]

    @property
    def get_cors_methods(self) -> List[str]:
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        if not all(isinstance(method, str) and method.strip() for method in methods):
            raise ValueError("CORS methods must be a list of non-empty strings.")
        return methods

    @property
    def get_cors_headers(self) -> List[str]:
        headers = ["Content-Type", "Authorization", "Accept"]
        if not all(isinstance(header, str) and header.strip() for header in headers):
            raise ValueError("CORS headers must be a list of non-empty strings.")
        return headers