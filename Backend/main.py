# main.py
from app.core.tools.import_manager import *
from fastapi.responses import HTMLResponse

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

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Equipay</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #5a67d8;
            }
            p {
                font-size: 18px;
                margin-top: 20px;
            }
            a {
                text-decoration: none;
                color: #5a67d8;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to FastAPI</h1>
        <p>Your FastAPI application Equipay is running successfully!</p>
        <p>Visit the <a href="/docs">API Documentation</a> to explore your endpoints.</p>
    </body>
    </html>
    """
    return html_content

@app.get("/ping")
def ping():
    return {"message": "Pong!"}

    
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
