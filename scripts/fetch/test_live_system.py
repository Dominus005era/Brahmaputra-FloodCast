import json
import sys
import os
import time
from datetime import datetime

# ============================================================
# FLOODSENSE AI — LIVE SYSTEM TEST SUITE
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("=" * 75)
print("FLOODSENSE AI — LIVE SYSTEM TEST SUITE")
print("=" * 75)

# ============================================================
# TEST 1 — IMPORT LIVE SERVICE
# ============================================================

print("\n[TEST 1] Import live_service")

try:
    from scripts.fetch.live_service import FloodSenseLiveService

    print("PASS — live_service imported successfully")

except Exception as e:
    print("FAIL — Could not import live_service")
    print("ERROR:", repr(e))
    sys.exit(1)


# ============================================================
# TEST 2 — LOAD SERVICE / MODEL
# ============================================================

print("\n[TEST 2] Initialize FloodSenseLiveService")

try:
    service = FloodSenseLiveService()

    print("PASS — FloodSenseLiveService initialized")

except Exception as e:
    print("FAIL — Service initialization failed")
    print("ERROR:", repr(e))
    sys.exit(1)


# ============================================================
# TEST 3 — RUN LIVE PREDICTION
# ============================================================

print("\n[TEST 3] Run live prediction")

try:
    result = service.get_live_prediction()

    print("PASS — Prediction generated")

except Exception as e:
    print("FAIL — Live prediction failed")
    print("ERROR:", repr(e))
    sys.exit(1)


# ============================================================
# TEST 4 — OUTPUT STRUCTURE
# ============================================================

print("\n[TEST 4] Validate output structure")

required_fields = [
    "station",
    "district",
    "state",
    "timestamp",
    "current_water_level",
    "prediction",
    "prediction_label",
    "probability",
    "risk_level",
    "escalation_level",
    "status",
]

missing_fields = [
    field for field in required_fields
    if field not in result
]

if not missing_fields:
    print("PASS — All required output fields present")

else:
    print("FAIL — Missing fields:")
    for field in missing_fields:
        print("  -", field)


# ============================================================
# TEST 5 — BASIC VALUE VALIDATION
# ============================================================

print("\n[TEST 5] Validate prediction values")

try:
    assert result["prediction"] in [0, 1]

    assert result["prediction_label"] in [
        "NORMAL",
        "HIGH_WATER"
    ]

    assert 0 <= float(result["probability"]) <= 1

    assert isinstance(
        result["current_water_level"],
        (int, float)
    )

    print("PASS — Prediction values are valid")

except Exception as e:
    print("FAIL — Invalid prediction values")
    print("ERROR:", repr(e))


# ============================================================
# TEST 6 — TIMESTAMP VALIDATION
# ============================================================

print("\n[TEST 6] Validate prediction timestamp")

try:
    prediction_time = datetime.fromisoformat(
        str(result["timestamp"])
    )

    print("Prediction timestamp:", prediction_time)

    print("PASS — Timestamp is valid")

except Exception as e:
    print("FAIL — Invalid timestamp")
    print("ERROR:", repr(e))


# ============================================================
# TEST 7 — CURRENT-DATE CHECK
# ============================================================

print("\n[TEST 7] Check whether prediction is current")

try:
    prediction_time = datetime.fromisoformat(
        str(result["timestamp"])
    )

    now = datetime.now()

    age_hours = abs(
        (now - prediction_time).total_seconds()
    ) / 3600

    print("System time :", now)
    print("Prediction  :", prediction_time)
    print("Age hours   :", round(age_hours, 2))

    # We allow up to 3 hours because hydrology
    # sources may publish hourly data with some delay.
    if age_hours <= 3:

        print("PASS — Prediction timestamp is current/recent")

    else:

        print("WARNING — Prediction timestamp is older than 3 hours")
        print("This does NOT automatically mean the system is broken.")
        print("Check the data source and freshness status.")


except Exception as e:
    print("FAIL — Could not validate current timestamp")
    print("ERROR:", repr(e))


# ============================================================
# TEST 8 — PRINT SOURCE / MODE IF AVAILABLE
# ============================================================

print("\n[TEST 8] Check data source transparency")

source_fields = [
    "data_source",
    "data_mode",
    "source",
    "mode",
]

found_source = False

for field in source_fields:

    if field in result:

        print(f"{field}: {result[field]}")
        found_source = True


if found_source:

    print("PASS — Data source/mode is exposed")

else:

    print(
        "WARNING — No explicit data_source/data_mode field found."
    )

    print(
        "Recommendation: distinguish NWDP ground telemetry "
        "from Hydrology Bridge data."
    )


# ============================================================
# TEST 9 — DISPLAY COMPLETE RESULT
# ============================================================

print("\n[TEST 9] Complete prediction output")

print("-" * 75)

print(
    json.dumps(
        result,
        indent=2,
        default=str
    )
)

print("-" * 75)


# ============================================================
# TEST 10 — SECOND CALL
# ============================================================

print("\n[TEST 10] Second prediction call")

try:

    result2 = service.get_live_prediction()

    print("PASS — Second prediction generated")

    print(
        "First timestamp :",
        result["timestamp"]
    )

    print(
        "Second timestamp:",
        result2["timestamp"]
    )

    if result["timestamp"] == result2["timestamp"]:

        print(
            "INFO — Same latest timestamp returned."
        )

        print(
            "This is EXPECTED if no new source record "
            "arrived between the two calls."
        )

    else:

        print(
            "INFO — New timestamp detected."
        )

        print(
            "The source updated between calls."
        )


except Exception as e:

    print("FAIL — Second prediction failed")
    print("ERROR:", repr(e))


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 75)
print("FLOODSENSE AI — TEST SUMMARY")
print("=" * 75)

print("Service initialization : PASS")
print("Prediction generation  : PASS")
print("Output schema          : checked")
print("Prediction values      : checked")
print("Timestamp              : checked")
print("Current-date status    : checked")
print("Source transparency    : checked")
print("Second-call behavior   : checked")

print("=" * 75)
print("LIVE SYSTEM TEST COMPLETE")
print("=" * 75)