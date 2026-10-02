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

def _sync_ingest_job():
    try:
        db = SessionLocal()
        try:
            logger.info("Executing background live telemetry sync for TODAY...")
            ingest_live_prediction(db)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in background ingestion job: {e}")

async def periodic_ingestion_worker():
    logger.info("Background Telemetry Ingestion Worker started.")
    # Small pause allows Uvicorn to complete port binding and respond to health checks instantly
    await asyncio.sleep(0.5)
    while True:
        try:
            await asyncio.to_thread(_sync_ingest_job)
        except Exception as e:
            logger.error(f"Error in background ingestion loop: {e}")
        
        await asyncio.sleep(settings.POLLING_INTERVAL_SECONDS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FloodSense FastAPI Server & Worker...")
    worker_task = asyncio.create_task(periodic_ingestion_worker())
    yield
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass
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