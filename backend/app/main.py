import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.routes import flood, stations
from backend.app.services.ingestion import ingest_live_prediction

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("FloodSenseApp")

# Create tables if not exists
Base.metadata.create_all(bind=engine)

async def periodic_ingestion_worker():
    logger.info("Background Telemetry Ingestion Worker started.")
    while True:
        try:
            db = SessionLocal()
            try:
                ingest_live_prediction(db)
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error in background ingestion loop: {e}")
        
        await asyncio.sleep(settings.POLLING_INTERVAL_SECONDS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FloodSense FastAPI Server & SQL Server Sync...")
    # Perform immediate synchronous live ingestion on startup so DB is never stale or showing past dates!
    try:
        db = SessionLocal()
        try:
            logger.info("Executing initial live telemetry sync for TODAY...")
            ingest_live_prediction(db)
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"Initial startup ingestion warning: {e}")

    worker_task = asyncio.create_task(periodic_ingestion_worker())
    yield
    worker_task.cancel()
    logger.info("FloodSense Server shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-Time AI Flood Forecasting & Early Warning Backend for Brahmaputra Basin.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(flood.router)
app.include_router(stations.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": settings.DB_NAME,
        "server": settings.DB_SERVER
    }

# Mount Frontend UI Static Files
from fastapi.staticfiles import StaticFiles
from pathlib import Path

FRONTEND_PATH = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_PATH.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_PATH), html=True), name="frontend")