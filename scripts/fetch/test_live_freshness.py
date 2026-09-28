import requests
import pandas as pd
from datetime import datetime

RESOURCE_ID = "847f5630-f231-46c0-922d-0f2f379a5cb8"

URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

params = {
    "resource_id": RESOURCE_ID,
    "limit": 100,
    "sort": "Data Acquisition Time desc"
}

response = requests.get(URL, params=params, timeout=30)

print("=" * 70)
print("FLOODSENSE — TRUE LIVE DATA VERIFICATION")
print("=" * 70)

print("HTTP Status:", response.status_code)

data = response.json()

records = data.get("result", {}).get("records", [])

print("Records received:", len(records))

df = pd.DataFrame(records)

if df.empty:
    print("NO DATA")
    raise SystemExit

TIME_COL = "Data Acquisition Time"
STATION_COL = "Station"
WATER_COL = "River Water Level Telemetry Hourly (meter)"

df[TIME_COL] = pd.to_datetime(
    df[TIME_COL],
    errors="coerce"
)

df = df.dropna(subset=[TIME_COL])

df = df[
    df[STATION_COL].astype(str).str.strip()
    == "NH15 Crossing Fakirpara Tangni"
]

df = df.sort_values(TIME_COL)

if df.empty:
    print("TARGET STATION NOT FOUND")
    raise SystemExit

latest = df.iloc[-1]

latest_time = latest[TIME_COL]
system_time = datetime.now()

age = system_time - latest_time

print()
print("-" * 70)
print("LIVE FRESHNESS RESULT")
print("-" * 70)

print("System time        :", system_time)
print("Latest API time    :", latest_time)
print("Data age           :", age)

print()
print("Latest station     :", latest[STATION_COL])
print("Latest water level :", latest[WATER_COL])

print()
print("-" * 70)

MAX_ALLOWED_HOURS = 2

if age.total_seconds() <= MAX_ALLOWED_HOURS * 3600:
    print("STATUS             : FRESH / LIVE")
    print("LIVE PREDICTION    : ALLOWED")
else:
    print("STATUS             : STALE")
    print("LIVE PREDICTION    : BLOCKED")

print("=" * 70)