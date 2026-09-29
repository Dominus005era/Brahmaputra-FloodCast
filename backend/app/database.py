import logging
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings

logger = logging.getLogger("FloodSenseDB")

def init_database_engine():
    # 1. If explicit DATABASE_URL provided via environment (e.g. Render / Cloud)
    env_url = settings.DATABASE_URL
    if env_url.startswith("sqlite"):
        logger.info(f"Using SQLite database: {env_url}")
        return create_engine(env_url, connect_args={"check_same_thread": False})
    elif env_url.startswith("postgresql"):
        logger.info("Using PostgreSQL database")
        return create_engine(env_url, pool_pre_ping=True)

    # 2. Try Microsoft SQL Server (Default for local development)
    try:
        import pyodbc
        master_conn_str = (
            f"DRIVER={{{settings.DB_DRIVER}}};"
            f"SERVER={settings.DB_SERVER};"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(master_conn_str, autocommit=True, timeout=3)
        cursor = conn.cursor()
        cursor.execute(f"IF DB_ID('{settings.DB_NAME}') IS NULL CREATE DATABASE [{settings.DB_NAME}];")
        conn.close()
        logger.info(f"SQL Server Database '{settings.DB_NAME}' verified on {settings.DB_SERVER}.")
        return create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
    except Exception as e:
        logger.warning(f"Microsoft SQL Server not reachable or pyodbc unavailable ({e}).")
        logger.info("Falling back to local SQLite database (floodsense.db) for zero-setup cloud execution.")
        sqlite_file = settings.PROJECT_ROOT / "floodsense.db"
        return create_engine(f"sqlite:///{sqlite_file}", connect_args={"check_same_thread": False})

engine = init_database_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()