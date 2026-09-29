import os
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    APP_NAME: str = "FloodSense AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # SQL Server connection string
    # Default uses Windows Trusted Authentication to local SQLEXPRESS
    DB_SERVER: str = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
    DB_NAME: str = os.getenv("DB_NAME", "FloodSenseDB")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    
    @property
    def DATABASE_URL(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
        import urllib.parse
        params = urllib.parse.quote_plus(
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return f"mssql+pyodbc:///?odbc_connect={params}"

    POLLING_INTERVAL_SECONDS: int = 60
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()