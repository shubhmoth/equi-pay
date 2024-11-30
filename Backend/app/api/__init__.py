from pathlib import Path
import importlib
from fastapi import APIRouter

# Base API router to gather all sub-routers
api_router = APIRouter()

# Path to this directory
ROUTER_DIR = Path(__file__).parent

# Automatically discover and include all routers
for router_file in ROUTER_DIR.glob("*.py"):
    if router_file.name == "__init__.py" or router_file.name.startswith("_"):
        continue  # Skip __init__.py and private files
    module_name = f"app.api.{router_file.stem}"
    module = importlib.import_module(module_name)

    # Check if the module defines a "router"
    if hasattr(module, "router"):
        api_router.include_router(
            module.router,
            prefix="",  # Prefix can be customized if needed
            tags=[router_file.stem.capitalize()]  # Tags derived from filename
        )
