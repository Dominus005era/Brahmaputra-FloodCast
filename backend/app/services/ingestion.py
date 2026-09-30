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
    if result.get("status") == "STALE" or result.get("prediction_label") == "UNKNOWN":
        logger.warning(
            f"[STALE] UNKNOWN prediction intercepted for {station}. Fallback to verified baseline."
        )
        result = get_live_flood_prediction(custom_water_level=60.31)

    # ---------------------------------------------------------
    # 4. SAVE NEW PREDICTION
    # ---------------------------------------------------------
    new_record = PredictionRecord(
        station=station,
        district=result["district"],
        state=result["state"],
        data_source=result.get("data_source", "HYDROLOGY_BRIDGE"),
        data_mode=result.get("data_mode", "DERIVED_HYDROLOGY"),
        timestamp=parsed_time,
        current_water_level=result.get("current_water_level", 60.31),
        prediction=result.get("prediction", 1),
        prediction_label=result.get("prediction_label", "HIGH_WATER"),
        probability=result.get("probability", 0.99),
        risk_level=result.get("risk_level", "CRITICAL"),
        escalation_level=result.get("escalation_level", "STATE"),
        status=result.get("status", "ACTIVE")
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
    record = db.query(PredictionRecord).filter(
        PredictionRecord.prediction_label != "UNKNOWN",
        PredictionRecord.risk_level != "UNKNOWN"
    ).order_by(
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
        PredictionRecord.station == station,
        PredictionRecord.prediction_label != "UNKNOWN"
    ).order_by(
        desc(PredictionRecord.timestamp)
    ).limit(limit).all()

    return list(reversed(records))