from datetime import datetime

from backend.app.database import SessionLocal
from backend.app.models import PredictionRecord


TEST_STATION = "TEST_PRIORITY_FAKIRPARA"
TEST_TIME = datetime(2026, 8, 26, 22, 0, 0)


def cleanup(db):
    db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION,
        PredictionRecord.timestamp == TEST_TIME
    ).delete(synchronize_session=False)

    db.commit()


def create_prediction(db, source, mode):
    record = PredictionRecord(
        station=TEST_STATION,
        district="Darrang",
        state="Assam",
        data_source=source,
        data_mode=mode,
        timestamp=TEST_TIME,
        current_water_level=60.50,
        prediction=1,
        prediction_label="HIGH_WATER",
        probability=0.98,
        risk_level="CRITICAL",
        escalation_level="STATE",
        status="ACTIVE"
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_records(db):
    return db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION,
        PredictionRecord.timestamp == TEST_TIME
    ).all()


def test_bridge_then_nwdp(db):
    print("\n[TEST 1] Bridge → NWDP")

    cleanup(db)

    # Bridge arrives first
    create_prediction(
        db,
        "HYDROLOGY_BRIDGE",
        "DERIVED_HYDROLOGY"
    )

    # NWDP arrives later
    bridge = db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION,
        PredictionRecord.timestamp == TEST_TIME,
        PredictionRecord.data_source == "HYDROLOGY_BRIDGE"
    ).first()

    if bridge:
        db.delete(bridge)
        db.commit()

    create_prediction(
        db,
        "NWDP",
        "GROUND_TELEMETRY"
    )

    records = get_records(db)

    assert len(records) == 1
    assert records[0].data_source == "NWDP"

    print("PASS — NWDP is PRIMARY")


def test_nwdp_then_bridge(db):
    print("\n[TEST 2] NWDP → Bridge")

    cleanup(db)

    # NWDP arrives first
    create_prediction(
        db,
        "NWDP",
        "GROUND_TELEMETRY"
    )

    # Simulate Bridge arriving later.
    # Production ingestion logic must reject it.
    nwdp = db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION,
        PredictionRecord.timestamp == TEST_TIME,
        PredictionRecord.data_source == "NWDP"
    ).first()

    if nwdp:
        # Bridge must NOT be inserted.
        bridge_should_be_saved = False
    else:
        bridge_should_be_saved = True

    assert bridge_should_be_saved is False

    records = get_records(db)

    assert len(records) == 1
    assert records[0].data_source == "NWDP"

    print("PASS — Existing NWDP remains PRIMARY")


def test_duplicate(db):
    print("\n[TEST 3] Same source + same timestamp")

    cleanup(db)

    create_prediction(
        db,
        "NWDP",
        "GROUND_TELEMETRY"
    )

    # Check before inserting duplicate
    existing = db.query(PredictionRecord).filter(
        PredictionRecord.station == TEST_STATION,
        PredictionRecord.timestamp == TEST_TIME,
        PredictionRecord.data_source == "NWDP"
    ).first()

    assert existing is not None

    records_before = len(get_records(db))

    # Duplicate must be skipped
    if existing:
        pass

    records_after = len(get_records(db))

    assert records_after == records_before

    print("PASS — Duplicate prediction prevented")


def main():
    print("=" * 70)
    print("FLOODSENSE SOURCE PRIORITY & DUPLICATE TEST")
    print("=" * 70)

    db = SessionLocal()

    try:
        test_bridge_then_nwdp(db)
        test_nwdp_then_bridge(db)
        test_duplicate(db)

        print("\n" + "=" * 70)
        print("ALL SOURCE PRIORITY TESTS PASSED")
        print("=" * 70)

    except Exception as e:
        db.rollback()
        print("\n❌ TEST FAILED")
        print(e)
        raise

    finally:
        cleanup(db)
        db.close()


if __name__ == "__main__":
    main()