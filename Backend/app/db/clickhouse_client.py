from clickhouse_driver import Client
from app.core.config import get_settings
from fastapi import HTTPException
from app.core.utils.utils import safe_execute

# Fetch the settings once using the safe_execute function
settings = safe_execute(get_settings, "Error loading settings")

def get_clickhouse_client():
    try:
        # Correctly access the settings with the correct attribute names
        if not settings.CLICKHOUSE_HOST or not settings.CLICKHOUSE_PORT or not settings.CLICKHOUSE_DATABASE:
            raise ValueError("Incomplete database configuration")

        # Create the ClickHouse client using the correct values from the settings
        client = Client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DATABASE
        )
        return client
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce:
        raise HTTPException(status_code=503, detail=f"Connection to database failed: {str(ce)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
