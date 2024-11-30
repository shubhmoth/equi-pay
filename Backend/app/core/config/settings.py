# app/core/config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from .api_config import APIConfig
from .auth_config import AuthConfig
from .cors_config import CORSConfig
from .database_config import DatabaseConfig

class Settings(BaseSettings, APIConfig, AuthConfig, CORSConfig, DatabaseConfig):
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    CLICKHOUSE_HOST: str = 'localhost'
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_USER: str = 'default'
    CLICKHOUSE_PASSWORD: str = ''
    CLICKHOUSE_DATABASE: str = 'test'
    
    SECRET_KEY: str = "e0497ccaca7506a33b549dc77dbd9b605a66316d305b2463a442f375734bbe44"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        if not isinstance(self.ENVIRONMENT, str) or not self.ENVIRONMENT.strip():
            raise ValueError("Environment must be a non-empty string.")
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        if not isinstance(self.ENVIRONMENT, str) or not self.ENVIRONMENT.strip():
            raise ValueError("Environment must be a non-empty string.")
        return self.ENVIRONMENT == "production"

    def get_db_url(self) -> str:
        if not all([self.CLICKHOUSE_HOST, self.CLICKHOUSE_PORT, self.CLICKHOUSE_USER, self.CLICKHOUSE_PASSWORD, self.CLICKHOUSE_DATABASE]):
            raise ValueError("All database connection parameters must be provided.")
        return self.get_database_url(
            self.CLICKHOUSE_HOST,
            self.CLICKHOUSE_PORT,
            self.CLICKHOUSE_USER,
            self.CLICKHOUSE_PASSWORD,
            self.CLICKHOUSE_DATABASE
        )


# Create settings instance
@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    
    try:
        get_settings.cache_clear()  # Clear cache if needed after changes
        settings = Settings()
        if not isinstance(settings, Settings):
            raise TypeError("Failed to create a valid Settings instance.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while initializing the settings: {e}")
    
    """ Note: If any changes are made to the Settings or its dependent values 
    (e.g., environment variables), you must clear the cache by calling  the above function get_settings.cache_clear() 
    to ensure the updates are reflected. """
    
    return settings

