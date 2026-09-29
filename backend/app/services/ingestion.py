import logging
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.models import PredictionRecord
from scripts.fetch.live_service import get_live_flood_prediction


logger = logging.getLogger("FloodSenseIngestion")


def ingest_live_prediction(db: Session) -> dict:
    result = get_live_flood_prediction(as_json=False)

    station = result["station"]
    timestamp_str = result["timestamp"]
    data_source = result.get("data_source", "NONE")
    data_mode = result.get("data_mode", "UNAVAILABLE")

    try:
        parsed_time = datetime.fromisoformat(timestamp_str)
    except Exception:
        parsed_time = datetime.now()

    # ---------------------------------------------------------
    # 1. SAME SOURCE + SAME TIMESTAMP = DUPLICATE
    # ---------------------------------------------------------
    existing = db.query(PredictionRecord).filter(
        PredictionRecord.station == station,
        PredictionRecord.timestamp == parsed_time,
        PredictionRecord.data_source == data_source
    ).first()

    if existing:
        logger.info(
            f"[DUPLICATE SKIP] {station} | "
            f"{timestamp_str} | {data_source}"
        )
        return result

    # ---------------------------------------------------------
    # 2. SOURCE PRIORITY
    #
    # NWDP = PRIMARY
    # HYDROLOGY_BRIDGE = FALLBACK
    # ---------------------------------------------------------

    if data_source == "HYDROLOGY_BRIDGE":

        # If NWDP already exists for this station + timestamp,
        # Bridge must NOT be stored.
        nwdp_existing = db.query(PredictionRecord).filter(
            PredictionRecord.station == station,
            PredictionRecord.timestamp == parsed_time,
            PredictionRecord.data_source == "NWDP"
        ).first()

        if nwdp_existing:
            logger.info(
                f"[BRIDGE SKIP] NWDP ground telemetry already exists "
                f"for {station} at {timestamp_str}. "
                f"NWDP remains PRIMARY."
            )
            return result

    elif data_source == "NWDP":

        # If Bridge was stored first for the same timestamp,
        # remove it because fresh NWDP has priority.
        bridge_existing = db.query(PredictionRecord).filter(
            PredictionRecord.station == station,
            PredictionRecord.timestamp == parsed_time,
            PredictionRecord.data_source == "HYDROLOGY_BRIDGE"
        ).first()

        if bridge_existing:
            logger.info(
                f"[NWDP PRIORITY] Replacing Bridge record with "
                f"primary NWDP ground telemetry for {timestamp_str}."
            )

            db.delete(bridge_existing)
            db.flush()

    # ---------------------------------------------------------
    # 3. STALE RESULT PROTECTION
    # ---------------------------------------------------------
    if result.get("status") == "STALE":
        logger.warning(
            f"[STALE] No valid current prediction available "
            f"for {station}."
        )
        return result

    # ---------------------------------------------------------
    # 4. SAVE NEW PREDICTION
    # ---------------------------------------------------------
    new_record = PredictionRecord(
        station=station,
        district=result["district"],
        state=result["state"],
        data_source=data_source,
        data_mode=data_mode,
        timestamp=parsed_time,
        current_water_level=result.get("current_water_level"),
        prediction=result.get("prediction"),
        prediction_label=result.get("prediction_label", "UNKNOWN"),
        probability=result.get("probability", 0.0),
        risk_level=result.get("risk_level", "UNKNOWN"),
        escalation_level=result.get("escalation_level", "NONE"),
        status=result.get("status", "STALE")
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    logger.info(
        f"✅ [SQL SERVER] Saved new prediction ID "
        f"{new_record.prediction_id}: "
        f"{station} at {timestamp_str} "
        f"({new_record.prediction_label}, "
        f"{new_record.risk_level})"
    )

    return result


def get_latest_prediction_from_db(db: Session):
    record = db.query(PredictionRecord).order_by(
        desc(PredictionRecord.timestamp),
        desc(PredictionRecord.prediction_id)
    ).first()

    return record


def get_history_from_db(
    db: Session,
    station: str,
    limit: int = 24
):
    records = db.query(PredictionRecord).filter(
        PredictionRecord.station == station
    ).order_by(
        desc(PredictionRecord.timestamp)
    ).limit(limit).all()

    return list(reversed(records))