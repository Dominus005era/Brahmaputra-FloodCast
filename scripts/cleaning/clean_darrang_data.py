import pandas as pd
import os


# ============================================================
# FILE PATHS
# ============================================================

API1_FILE = "data/darrang_api1_raw.csv"
API2_FILE = "data/darrang_api2_raw.csv"

OUTPUT_FILE = "data/darrang_water_level_clean.csv"


# ============================================================
# COLUMN NAMES
# ============================================================

DATE_COL = "Data Acquisition Time"

WATER_LEVEL_COL = "River Water Level Telemetry Hourly (meter)"

STATION_COL = "Station"

DISTRICT_COL = "District"


# ============================================================
# LOAD RAW DATA
# ============================================================

print("=" * 60)
print("LOADING RAW DATA")
print("=" * 60)

api1 = pd.read_csv(API1_FILE)
api2 = pd.read_csv(API2_FILE)

print("API 1 records:", len(api1))
print("API 2 records:", len(api2))


# ============================================================
# CONVERT DATE/TIME
# ============================================================

api1[DATE_COL] = pd.to_datetime(
    api1[DATE_COL],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

api2[DATE_COL] = pd.to_datetime(
    api2[DATE_COL],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)


# ============================================================
# CONVERT WATER LEVEL TO NUMERIC
# ============================================================

api1[WATER_LEVEL_COL] = pd.to_numeric(
    api1[WATER_LEVEL_COL],
    errors="coerce"
)

api2[WATER_LEVEL_COL] = pd.to_numeric(
    api2[WATER_LEVEL_COL],
    errors="coerce"
)


# ============================================================
# API 1 — DUPLICATE TIMESTAMP ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("API 1 DUPLICATE ANALYSIS")
print("=" * 60)

duplicate_rows = api1.duplicated(
    subset=[STATION_COL, DATE_COL],
    keep=False
).sum()

duplicate_timestamps = api1.duplicated(
    subset=[STATION_COL, DATE_COL],
    keep="first"
).sum()

print("Duplicate rows involved:", duplicate_rows)
print("Extra duplicate rows:", duplicate_timestamps)


# ============================================================
# API 1 — HANDLE DUPLICATES
# ============================================================
#
# If the same Station + Timestamp appears multiple times:
#
# - Keep the valid water-level value if available.
# - If multiple valid values exist, take their mean.
# - Other metadata is taken from the first row.
#
# ============================================================

print("\nCleaning API 1 duplicate timestamps...")

metadata_columns = [
    col for col in api1.columns
    if col not in [WATER_LEVEL_COL]
]

api1_clean = (
    api1
    .groupby(
        [STATION_COL, DATE_COL],
        as_index=False,
        dropna=False
    )
    .agg({
        **{
            col: "first"
            for col in metadata_columns
            if col not in [STATION_COL, DATE_COL]
        },
        WATER_LEVEL_COL: "mean"
    })
)


print("API 1 records after duplicate cleaning:", len(api1_clean))


# ============================================================
# API 1 — MISSING WATER LEVEL CHECK
# ============================================================

print("\n" + "=" * 60)
print("API 1 MISSING WATER LEVEL")
print("=" * 60)

missing_api1 = api1_clean[WATER_LEVEL_COL].isna().sum()

print("Missing water-level values after duplicate cleaning:",
      missing_api1)


# ============================================================
# API 1 — INTERPOLATE MISSING VALUES
# ============================================================
#
# We DO NOT blindly fill missing values.
#
# Since water level is a time-series measurement,
# interpolation can estimate a missing value between
# two known observations.
#
# ============================================================

print("\nInterpolating remaining missing API 1 values...")

api1_clean = api1_clean.sort_values(
    [STATION_COL, DATE_COL]
).reset_index(drop=True)

api1_clean[WATER_LEVEL_COL] = (
    api1_clean
    .groupby(STATION_COL)[WATER_LEVEL_COL]
    .transform(
        lambda x: x.interpolate(
            method="linear",
            limit_direction="both"
        )
    )
)


missing_after_interpolation = api1_clean[
    WATER_LEVEL_COL
].isna().sum()

print(
    "Missing water-level values after interpolation:",
    missing_after_interpolation
)


# ============================================================
# API 2 CLEANING
# ============================================================

print("\n" + "=" * 60)
print("API 2 CLEANING")
print("=" * 60)

api2_clean = api2.copy()

# Remove exact duplicate rows if any
api2_clean = api2_clean.drop_duplicates()

# Remove duplicate Station + Timestamp combinations
api2_clean = (
    api2_clean
    .sort_values([STATION_COL, DATE_COL])
    .drop_duplicates(
        subset=[STATION_COL, DATE_COL],
        keep="first"
    )
    .reset_index(drop=True)
)

print("API 2 records after cleaning:", len(api2_clean))

print(
    "API 2 missing water-level values:",
    api2_clean[WATER_LEVEL_COL].isna().sum()
)


# ============================================================
# CHECK COLUMN COMPATIBILITY
# ============================================================

print("\n" + "=" * 60)
print("COLUMN CHECK")
print("=" * 60)

api1_columns = list(api1_clean.columns)
api2_columns = list(api2_clean.columns)

if set(api1_columns) == set(api2_columns):
    print("API 1 and API 2 columns match: YES")
else:
    print("API 1 and API 2 columns match: NO")

    print("\nColumns only in API 1:")
    print(set(api1_columns) - set(api2_columns))

    print("\nColumns only in API 2:")
    print(set(api2_columns) - set(api1_columns))


# ============================================================
# ADD SOURCE COLUMN
# ============================================================

api1_clean["Source"] = "API 1"
api2_clean["Source"] = "API 2"


# ============================================================
# COMBINE API 1 + API 2
# ============================================================

print("\n" + "=" * 60)
print("COMBINING API 1 + API 2")
print("=" * 60)

final_data = pd.concat(
    [api1_clean, api2_clean],
    ignore_index=True
)


print("Records after combining:", len(final_data))


# ============================================================
# REMOVE CROSS-API DUPLICATES
# ============================================================

before_duplicate_removal = len(final_data)

final_data = (
    final_data
    .sort_values([STATION_COL, DATE_COL])
    .drop_duplicates(
        subset=[STATION_COL, DATE_COL],
        keep="first"
    )
    .reset_index(drop=True)
)

after_duplicate_removal = len(final_data)

print(
    "Cross-API duplicate rows removed:",
    before_duplicate_removal - after_duplicate_removal
)


# ============================================================
# FINAL SORT
# ============================================================

final_data = final_data.sort_values(
    [STATION_COL, DATE_COL]
).reset_index(drop=True)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATASET")
print("=" * 60)

print("Total records:", len(final_data))

print(
    "Stations:",
    final_data[STATION_COL].nunique()
)

print(
    "Districts:",
    final_data[DISTRICT_COL].unique()
)

print(
    "Start date:",
    final_data[DATE_COL].min()
)

print(
    "End date:",
    final_data[DATE_COL].max()
)

print(
    "Missing water levels:",
    final_data[WATER_LEVEL_COL].isna().sum()
)

print(
    "Duplicate timestamps:",
    final_data.duplicated(
        subset=[STATION_COL, DATE_COL]
    ).sum()
)


# ============================================================
# SAVE FINAL DATASET
# ============================================================

os.makedirs("data", exist_ok=True)

final_data.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("SAVED SUCCESSFULLY")
print("=" * 60)

print("File:", OUTPUT_FILE)


# ============================================================
# CHECK INTERPOLATED VALUES
# ============================================================

print("\n" + "=" * 60)
print("INTERPOLATION VERIFICATION")
print("=" * 60)

raw_api1 = pd.read_csv(API1_FILE)

raw_api1[DATE_COL] = pd.to_datetime(
    raw_api1[DATE_COL],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

raw_api1[WATER_LEVEL_COL] = pd.to_numeric(
    raw_api1[WATER_LEVEL_COL],
    errors="coerce"
)

original_missing = raw_api1[WATER_LEVEL_COL].isna().sum()

print("Original missing API 1 values:", original_missing)

print("\nFinal missing values:")
print(
    final_data[WATER_LEVEL_COL].isna().sum()
)

print("\nFinal records:")
print(len(final_data))

print("\nFinal duplicate timestamps:")
print(
    final_data.duplicated(
        subset=[STATION_COL, DATE_COL]
    ).sum()
)