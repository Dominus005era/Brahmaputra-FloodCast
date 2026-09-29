from datetime import datetime
from unittest.mock import patch

from backend.app.database import SessionLocal
from backend.app.models import PredictionRecord
from backend.app.services.ingestion import ingest_live_prediction


TEST_STATION = "TEST_INGESTION_PRIORITY"
TEST_TIME = "2026-08-26T22:00:00"


def cleanup(db):
    db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION
    ).delete(synchronize_session=False)
    db.commit()


def mock_prediction(source, mode):
    return {
        "station": TEST_STATION,
        "district": "Darrang",
        "state": "Assam",
        "data_source": source,
        "data_mode": mode,
        "timestamp": TEST_TIME,
        "current_water_level": 60.50,
        "prediction": 1,
        "prediction_label": "HIGH_WATER",
        "probability": 0.98,
        "risk_level": "CRITICAL",
        "escalation_level": "STATE",
        "status": "ACTIVE",
    }


def get_records(db):
    return db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION
    ).all()


def main():

    print("=" * 70)
    print("FLOODSENSE ACTUAL INGESTION PRIORITY TEST")
    print("=" * 70)

    db = SessionLocal()

    try:

        # =====================================================
        # TEST 1: BRIDGE → NWDP
        # =====================================================

        print("\n[TEST 1] Bridge arrives first → NWDP arrives later")

        cleanup(db)

        bridge_result = mock_prediction(
            "HYDROLOGY_BRIDGE",
            "DERIVED_HYDROLOGY"
        )

        nwdp_result = mock_prediction(
            "NWDP",
            "GROUND_TELEMETRY"
        )

        with patch(
            "backend.app.services.ingestion.get_live_flood_prediction",
            return_value=bridge_result
        ):
            ingest_live_prediction(db)

        with patch(
            "backend.app.services.ingestion.get_live_flood_prediction",
            return_value=nwdp_result
        ):
            ingest_live_prediction(db)

        records = get_records(db)

        assert len(records) == 1, (
            f"Expected 1 record, found {len(records)}"
        )

        assert records[0].data_source == "NWDP", (
            f"Expected NWDP, found {records[0].data_source}"
        )

        print("PASS — NWDP replaced Bridge and remains PRIMARY")

        # =====================================================
        # TEST 2: NWDP → BRIDGE
        # =====================================================

        print("\n[TEST 2] NWDP arrives first → Bridge arrives later")

        cleanup(db)

        with patch(
            "backend.app.services.ingestion.get_live_flood_prediction",
            return_value=nwdp_result
        ):
            ingest_live_prediction(db)

        with patch(
            "backend.app.services.ingestion.get_live_flood_prediction",
            return_value=bridge_result
        ):
            ingest_live_prediction(db)

        records = get_records(db)

        assert len(records) == 1, (
            f"Expected 1 record, found {len(records)}"
        )

        assert records[0].data_source == "NWDP", (
            f"Expected NWDP, found {records[0].data_source}"
        )

        print("PASS — Bridge skipped; existing NWDP remains PRIMARY")

        # =====================================================
        # TEST 3: SAME SOURCE + SAME TIMESTAMP
        # =====================================================

        print("\n[TEST 3] Same source + same timestamp")

        cleanup(db)

        with patch(
            "backend.app.services.ingestion.get_live_flood_prediction",
            return_value=nwdp_result
        ):
            ingest_live_prediction(db)
            ingest_live_prediction(db)

        records = get_records(db)

        assert len(records) == 1, (
            f"Expected 1 record, found {len(records)}"
        )

        print("PASS — Duplicate prediction skipped")

        # =====================================================
        # FINAL
        # =====================================================

        print("\n" + "=" * 70)
        print("ALL ACTUAL INGESTION TESTS PASSED")
        print("=" * 70)

    except Exception as e:

        db.rollback()

        print("\n" + "=" * 70)
        print("❌ INGESTION TEST FAILED")
        print("=" * 70)
        print(f"Error: {e}")

        raise

    finally:
        cleanup(db)
        db.close()


if __name__ == "__main__":
    main()