# app/core/config/database_config.py
class DatabaseConfig:
    @staticmethod
    def get_database_url(host: str, port: int, user: str, password: str, database: str) -> str:
        if not all([host, port, user, password, database]):
            raise ValueError("All database connection parameters must be provided.")
        if not isinstance(port, int) or port <= 0:
            raise ValueError("Port must be a positive integer.")
        return f"clickhouse://{user}:{password}@{host}:{port}/{database}"
