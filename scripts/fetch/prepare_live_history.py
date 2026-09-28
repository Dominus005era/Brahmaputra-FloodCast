import requests
import pandas as pd


# ==============================================================
# CONFIGURATION
# ==============================================================

URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

API1_RESOURCE_ID = "51640870-5961-4696-b986-b744231f1c9f"
API2_RESOURCE_ID = "847f5630-f231-46c0-922d-0f2f379a5cb8"

STATION = "NH15 Crossing Fakirpara Tangni"

WATER_COL = "River Water Level Telemetry Hourly (meter)"


# ==============================================================
# FETCH FUNCTION
# ==============================================================

def fetch_api_data(resource_id, limit=5000):

    all_records = []
    offset = 0

    while True:

        params = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
            "q": STATION
        }

        response = requests.get(URL, params=params)

        print(
            "Status:",
            response.status_code,
            "| Offset:",
            offset
        )

        data = response.json()

        if not data["success"]:
            print("API Error:")
            print(data)
            raise SystemExit

        records = data["result"]["records"]

        if not records:
            break

        all_records.extend(records)

        total = data["result"]["total"]

        print(
            "Records received:",
            len(records),
            "| Total collected:",
            len(all_records),
            "| API total:",
            total
        )

        offset += limit

        if len(all_records) >= total:
            break

    return pd.DataFrame(all_records)


# ==============================================================
# FETCH API 1
# ==============================================================

print("=" * 70)
print("FETCHING API 1")
print("=" * 70)

df_api1 = fetch_api_data(API1_RESOURCE_ID)

print("\nAPI 1 records:", len(df_api1))


# ==============================================================
# FETCH API 2
# ==============================================================

print("\n" + "=" * 70)
print("FETCHING API 2")
print("=" * 70)

df_api2 = fetch_api_data(API2_RESOURCE_ID)

print("\nAPI 2 records:", len(df_api2))


# ==============================================================
# COMBINE API 1 + API 2
# ==============================================================

print("\n" + "=" * 70)
print("COMBINING API 1 + API 2")
print("=" * 70)

df = pd.concat(
    [df_api1, df_api2],
    ignore_index=True
)

print("Rows before duplicate removal:", len(df))


# ==============================================================
# TIMESTAMP CONVERSION
# ==============================================================

df["Data Acquisition Time"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

df = df.dropna(
    subset=["Data Acquisition Time"]
).copy()


# ==============================================================
# STATION FILTER
# ==============================================================

df = df[
    df["Station"] == STATION
].copy()


# ==============================================================
# DUPLICATE TIMESTAMP CHECK
# ==============================================================

duplicate_count = df.duplicated(
    subset=["Data Acquisition Time"]
).sum()

print("Duplicate timestamps before removal:", duplicate_count)


df = df.drop_duplicates(
    subset=["Data Acquisition Time"],
    keep="last"
)


# ==============================================================
# SORT CHRONOLOGICALLY
# ==============================================================

df = df.sort_values(
    "Data Acquisition Time"
).reset_index(drop=True)


# ==============================================================
# WATER LEVEL CONVERSION
# ==============================================================

df[WATER_COL] = pd.to_numeric(
    df[WATER_COL],
    errors="coerce"
)


# ==============================================================
# COMBINED LIVE HISTORY SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("COMBINED LIVE HISTORY")
print("=" * 70)

print("Station:", STATION)

print("Final rows:", len(df))

print(
    "Date range:",
    df["Data Acquisition Time"].min(),
    "→",
    df["Data Acquisition Time"].max()
)

print(
    "Missing water-level values:",
    df[WATER_COL].isna().sum()
)


# ==============================================================
# TIME FEATURES
# ==============================================================

df["Year"] = df["Data Acquisition Time"].dt.year
df["Month"] = df["Data Acquisition Time"].dt.month
df["Day"] = df["Data Acquisition Time"].dt.day
df["Hour"] = df["Data Acquisition Time"].dt.hour
df["DayOfYear"] = df["Data Acquisition Time"].dt.dayofyear
df["DayOfWeek"] = df["Data Acquisition Time"].dt.dayofweek


print("\n" + "=" * 70)
print("TIME FEATURES CREATED")
print("=" * 70)

print([
    "Year",
    "Month",
    "Day",
    "Hour",
    "DayOfYear",
    "DayOfWeek"
])


# ==============================================================
# CURRENT WATER LEVEL
# ==============================================================

df["Current_Water_Level"] = df[WATER_COL]


# ==============================================================
# EXACT TIME-BASED WATER LEVEL LAG FEATURES
# ==============================================================

water_level_series = (
    df
    .set_index("Data Acquisition Time")[WATER_COL]
)

df["WaterLevel_Lag_1h"] = (
    water_level_series
    .reindex(
        df["Data Acquisition Time"] - pd.Timedelta(hours=1)
    )
    .to_numpy()
)

df["WaterLevel_Lag_3h"] = (
    water_level_series
    .reindex(
        df["Data Acquisition Time"] - pd.Timedelta(hours=3)
    )
    .to_numpy()
)

df["WaterLevel_Lag_6h"] = (
    water_level_series
    .reindex(
        df["Data Acquisition Time"] - pd.Timedelta(hours=6)
    )
    .to_numpy()
)

df["WaterLevel_Lag_12h"] = (
    water_level_series
    .reindex(
        df["Data Acquisition Time"] - pd.Timedelta(hours=12)
    )
    .to_numpy()
)

df["WaterLevel_Lag_24h"] = (
    water_level_series
    .reindex(
        df["Data Acquisition Time"] - pd.Timedelta(hours=24)
    )
    .to_numpy()
)


# ==============================================================
# TIME-BASED ROLLING WATER LEVEL FEATURES
# ==============================================================

rolling_data = (
    df[
        ["Data Acquisition Time", WATER_COL]
    ]
    .set_index("Data Acquisition Time")
)

df["WaterLevel_RollingMean_6h"] = (
    rolling_data[WATER_COL]
    .rolling("6h")
    .mean()
    .to_numpy()
)

df["WaterLevel_RollingMean_12h"] = (
    rolling_data[WATER_COL]
    .rolling("12h")
    .mean()
    .to_numpy()
)

df["WaterLevel_RollingMean_24h"] = (
    rolling_data[WATER_COL]
    .rolling("24h")
    .mean()
    .to_numpy()
)

df["WaterLevel_RollingMax_24h"] = (
    rolling_data[WATER_COL]
    .rolling("24h")
    .max()
    .to_numpy()
)

df["WaterLevel_RollingMin_24h"] = (
    rolling_data[WATER_COL]
    .rolling("24h")
    .min()
    .to_numpy()
)


# ==============================================================
# WATER LEVEL TREND / RATE-OF-CHANGE FEATURES
# ==============================================================

df["WaterLevel_Change_1h"] = (
    df[WATER_COL] - df["WaterLevel_Lag_1h"]
)

df["WaterLevel_Change_3h"] = (
    df[WATER_COL] - df["WaterLevel_Lag_3h"]
)

df["WaterLevel_Change_6h"] = (
    df[WATER_COL] - df["WaterLevel_Lag_6h"]
)

df["WaterLevel_Change_12h"] = (
    df[WATER_COL] - df["WaterLevel_Lag_12h"]
)

df["WaterLevel_Change_24h"] = (
    df[WATER_COL] - df["WaterLevel_Lag_24h"]
)


# ==============================================================
# FINAL 19 ML FEATURES — LOCKED
# ==============================================================

FINAL_FEATURES = [

    # Current state
    "Current_Water_Level",

    # Time
    "Month",
    "Hour",
    "DayOfYear",

    # Exact-time lag features
    "WaterLevel_Lag_1h",
    "WaterLevel_Lag_3h",
    "WaterLevel_Lag_6h",
    "WaterLevel_Lag_12h",
    "WaterLevel_Lag_24h",

    # Rolling features
    "WaterLevel_RollingMean_6h",
    "WaterLevel_RollingMean_12h",
    "WaterLevel_RollingMean_24h",
    "WaterLevel_RollingMax_24h",
    "WaterLevel_RollingMin_24h",

    # Trend features
    "WaterLevel_Change_1h",
    "WaterLevel_Change_3h",
    "WaterLevel_Change_6h",
    "WaterLevel_Change_12h",
    "WaterLevel_Change_24h"
]

TARGET = "High_Water_6h"


# ==============================================================
# FEATURE VALIDATION
# ==============================================================

print("\n" + "=" * 70)
print("FINAL 19-FEATURE PIPELINE VALIDATION")
print("=" * 70)

print("\nNumber of ML features:", len(FINAL_FEATURES))

print("\nFeatures:")

for i, feature in enumerate(FINAL_FEATURES, 1):
    print(f"{i}. {feature}")

print("\nMissing feature columns:")

missing_features = [
    feature
    for feature in FINAL_FEATURES
    if feature not in df.columns
]

print(missing_features)

print("\nFeature missing-value counts:")

print(
    df[FINAL_FEATURES]
    .isna()
    .sum()
)

print("\nLatest feature rows:")

print(
    df[
        [
            "Data Acquisition Time"
        ] + FINAL_FEATURES
    ]
    .tail(5)
    .to_string(index=False)
)


# ==============================================================
# FINAL SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("LIVE FEATURE PIPELINE READY")
print("=" * 70)

print("Rows:", len(df))
print("ML features:", len(FINAL_FEATURES))
print("Target:", TARGET)

print("\nLatest timestamp:")
print(df["Data Acquisition Time"].max())