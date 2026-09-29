from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas import FloodPredictionResponse, FloodHistoryResponse, CustomPredictionRequest
from backend.app.services.ingestion import get_latest_prediction_from_db, get_history_from_db, ingest_live_prediction
from scripts.fetch.live_service import get_live_flood_prediction

router = APIRouter(prefix="/api/flood", tags=["Flood Prediction & Telemetry"])

@router.get("/current", response_model=FloodPredictionResponse)
def get_current_flood_prediction(db: Session = Depends(get_db)):
    """
    Returns the latest authoritative flood prediction for NH15 Crossing Fakirpara Tangni.
    Always ensures real-time freshness for today.
    """
    latest = get_latest_prediction_from_db(db)
    now = datetime.now()
    
    # If no record exists or if the latest record is older than 30 minutes, ingest fresh prediction immediately
    if not latest or (now - latest.timestamp).total_seconds() > 1800:
        result = ingest_live_prediction(db)
        return FloodPredictionResponse(**result)

    return FloodPredictionResponse(
        station=latest.station,
        district=latest.district,
        state=latest.state,
        data_source=latest.data_source,
        data_mode=latest.data_mode,
        timestamp=latest.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
        current_water_level=latest.current_water_level,
        prediction=latest.prediction,
        prediction_label=latest.prediction_label,
        probability=latest.probability,
        risk_level=latest.risk_level,
        escalation_level=latest.escalation_level,
        status=latest.status
    )

@router.get("/history", response_model=FloodHistoryResponse)
def get_flood_history(
    station: str = Query("NH15 Crossing Fakirpara Tangni", description="Station name"),
    limit: int = Query(24, ge=1, le=168, description="Number of past hourly records to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Returns chronological prediction and water-level history for frontend graphs.
    """
    records = get_history_from_db(db, station=station, limit=limit)
    now = datetime.now()
    
    if not records or (now - records[-1].timestamp).total_seconds() > 3600:
        ingest_live_prediction(db)
        records = get_history_from_db(db, station=station, limit=limit)

    history_items = []
    for r in records:
        history_items.append(
            FloodPredictionResponse(
                station=r.station,
                district=r.district,
                state=r.state,
                data_source=r.data_source,
                data_mode=r.data_mode,
                timestamp=r.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                current_water_level=r.current_water_level,
                prediction=r.prediction,
                prediction_label=r.prediction_label,
                probability=r.probability,
                risk_level=r.risk_level,
                escalation_level=r.escalation_level,
                status=r.status
            )
        )

    return FloodHistoryResponse(
        station=station,
        total_records=len(history_items),
        history=history_items
    )

@router.post("/predict-custom", response_model=FloodPredictionResponse)
def predict_custom_scenario(payload: CustomPredictionRequest):
    """
    Operator / Simulation Mode: Evaluates flood risk for a custom user-supplied gauge height.
    """
    res = get_live_flood_prediction(custom_water_level=payload.water_level)
    return FloodPredictionResponse(**res)