import requests
import pandas as pd


# ==============================================================
# CONFIGURATION
# ==============================================================

URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

RESOURCE_ID = "51640870-5961-4696-b986-b744231f1c9f"

STATION = "NH15 Crossing Fakirpara Tangni"

WATER_COL = "River Water Level Telemetry Hourly (meter)"

LIMIT = 5000


# ==============================================================
# FETCH DATA
# ==============================================================

all_records = []
offset = 0

print("=" * 70)
print("NWDP — FAKIRPARA TANGNI DATA FETCH")
print("=" * 70)

while True:

    params = {
        "resource_id": RESOURCE_ID,
        "limit": LIMIT,
        "offset": offset,
        "q": STATION
    }

    try:

        response = requests.get(
            URL,
            params=params,
            timeout=30
        )

    except requests.RequestException as e:

        print("\nAPI CONNECTION ERROR")
        print(e)
        raise SystemExit

    print(
        "Status Code:",
        response.status_code,
        "| Offset:",
        offset
    )

    if response.status_code != 200:

        print("\nAPI HTTP ERROR")
        print("Status Code:", response.status_code)
        raise SystemExit

    try:

        data = response.json()

    except ValueError:

        print("\nINVALID API RESPONSE")
        print("Response is not valid JSON.")
        raise SystemExit

    if not data.get("success", False):

        print("\nAPI ERROR")
        print(data)
        raise SystemExit

    records = data["result"]["records"]

    if not records:
        break

    all_records.extend(records)

    print(
        "Records received:",
        len(records)
    )

    print(
        "Total collected:",
        len(all_records)
    )

    total = data["result"]["total"]

    offset += LIMIT

    if len(all_records) >= total:
        break


# ==============================================================
# BASIC DATA AVAILABILITY VALIDATION
# ==============================================================

print("\n" + "=" * 70)
print("DATA AVAILABILITY VALIDATION")
print("=" * 70)

if len(all_records) == 0:

    print("API Status       : OK")
    print("Records          : 0")
    print("Prediction       : BLOCKED")
    print("Reason           : No data received from API")

    raise SystemExit

print("API Status       : OK")
print("Records Received :", len(all_records))


# ==============================================================
# DATAFRAME
# ==============================================================

df = pd.DataFrame(all_records)


# ==============================================================
# REQUIRED COLUMN VALIDATION
# ==============================================================

required_columns = [
    "Station",
    "Data Acquisition Time",
    WATER_COL
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print("\nMISSING REQUIRED COLUMNS")
    print(missing_columns)

    raise SystemExit


# ==============================================================
# TIMESTAMP CONVERSION
# ==============================================================

df["Data Acquisition Time"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)


# ==============================================================
# WATER LEVEL CONVERSION
# ==============================================================

df[WATER_COL] = pd.to_numeric(
    df[WATER_COL],
    errors="coerce"
)


# ==============================================================
# INVALID TIMESTAMP VALIDATION
# ==============================================================

invalid_timestamp_count = (
    df["Data Acquisition Time"].isna().sum()
)

print(
    "Invalid timestamps:",
    invalid_timestamp_count
)

if invalid_timestamp_count > 0:

    print(
        "Removing invalid timestamp records..."
    )

    df = df.dropna(
        subset=["Data Acquisition Time"]
    ).copy()


# ==============================================================
# STATION VALIDATION
# ==============================================================

df = df[
    df["Station"] == STATION
].copy()

if df.empty:

    print("\nSTATION DATA NOT FOUND")

    raise SystemExit


# ==============================================================
# DUPLICATE TIMESTAMP CHECK
# ==============================================================

duplicate_count = df.duplicated(
    subset=["Data Acquisition Time"]
).sum()

print(
    "Duplicate timestamps:",
    duplicate_count
)

if duplicate_count > 0:

    df = df.drop_duplicates(
        subset=["Data Acquisition Time"],
        keep="last"
    ).copy()


# ==============================================================
# SORT CHRONOLOGICALLY
# ==============================================================

df = df.sort_values(
    "Data Acquisition Time"
).reset_index(drop=True)


# ==============================================================
# LATEST RECORD VALIDATION
# ==============================================================

latest_timestamp = (
    df["Data Acquisition Time"].max()
)

latest_rows = df[
    df["Data Acquisition Time"] == latest_timestamp
]

latest_water_level = (
    latest_rows[WATER_COL].iloc[-1]
)


# ==============================================================
# LATEST WATER LEVEL VALIDATION
# ==============================================================

print("\n" + "=" * 70)
print("LATEST DATA VALIDATION")
print("=" * 70)

print(
    "Latest Timestamp:",
    latest_timestamp
)

print(
    "Latest Water Level:",
    latest_water_level
)

if pd.isna(latest_water_level):

    print("\nPrediction Status: BLOCKED")
    print("Reason: Latest water-level value is missing.")

    raise SystemExit


# ==============================================================
# NEGATIVE WATER LEVEL CHECK
# ==============================================================

if latest_water_level < 0:

    print("\nPrediction Status: BLOCKED")
    print("Reason: Latest water-level value is invalid.")

    raise SystemExit


# ==============================================================
# FINAL FETCH SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("FETCH VALIDATION PASSED")
print("=" * 70)

print(
    "Station:",
    STATION
)

print(
    "Total Valid Records:",
    len(df)
)

print(
    "Date Range:",
    df["Data Acquisition Time"].min(),
    "→",
    df["Data Acquisition Time"].max()
)

print(
    "Latest Timestamp:",
    latest_timestamp
)

print(
    "Latest Water Level:",
    latest_water_level
)

print(
    "Duplicate Timestamps Removed:",
    duplicate_count
)

print(
    "Data Status: VALID"
)

print("=" * 70)