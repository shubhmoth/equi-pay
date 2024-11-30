# app/core/import_manager.py
from typing import Set
import inspect
import importlib
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.clickhouse_client import get_clickhouse_client
from app.core.utils.utils import safe_execute
from app.core.config import get_settings
from app.api import api_router
from clickhouse_driver import Client

# Export the imports you want to make available
__all__ = [
    'FastAPI',
    'HTTPException',
    'Depends',
    'status',
    'JSONResponse',
    'CORSMiddleware', 
    'get_clickhouse_client',
    'safe_execute',
    'get_settings',
    'api_router',
    'Client',
    'ImportManager'
]

class ImportManager:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analyzed_imports: Set[str] = set()
      