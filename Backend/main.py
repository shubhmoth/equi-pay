# main.py
from app.core.tools.import_manager import *

settings = safe_execute(get_settings, "Error loading settings")

app = safe_execute(
    lambda: FastAPI(**settings.get_api_config),
    "Error initializing FastAPI app"
)

safe_execute(
    lambda: app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins,
        allow_credentials=True,
        allow_methods=settings.get_cors_methods,
        allow_headers=settings.get_cors_headers
    ),
    "Error setting up CORS middleware"
)

safe_execute(
    lambda: app.include_router(api_router, prefix=settings.API_V1_STR),
    "Error including API router"
)

@app.get("/")
async def root():
    try:
        return {
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "docs_url": "/docs"
        }
    except Exception as e:
        raise RuntimeError(f"Error in root endpoint: {e}")
    
@app.get("/health")
async def health_check(client: Client = Depends(get_clickhouse_client)):
    try:
        client.execute("SELECT 1")  #query to check connection
        return {"status": "success", "message": "Database connection is healthy!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connectivity failed: {str(e)}")


if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.is_development
        )
    except Exception as e:
        raise SystemExit(f"Error starting the server: {e}")
