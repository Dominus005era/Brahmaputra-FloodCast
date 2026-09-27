import pandas as pd


# =========================
# FILE PATHS
# =========================

API1_FILE = "data/darrang_api1_raw.csv"
API2_FILE = "data/darrang_api2_raw.csv"


# =========================
# LOAD DATA
# =========================

api1 = pd.read_csv(API1_FILE)
api2 = pd.read_csv(API2_FILE)


# =========================
# BASIC INFORMATION
# =========================

print("=" * 60)
print("API 1")
print("=" * 60)

print("Records:", len(api1))
print("Columns:", len(api1.columns))

print("\nColumns:")
print(list(api1.columns))


print("\n" + "=" * 60)
print("API 2")
print("=" * 60)

print("Records:", len(api2))
print("Columns:", len(api2.columns))

print("\nColumns:")
print(list(api2.columns))


# =========================
# DATE CONVERSION
# =========================

DATE_COL = "Data Acquisition Time"

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


# =========================
# DATE RANGE
# =========================

print("\n" + "=" * 60)
print("DATE RANGE")
print("=" * 60)

print("\nAPI 1")
print("Start:", api1[DATE_COL].min())
print("End  :", api1[DATE_COL].max())

print("\nAPI 2")
print("Start:", api2[DATE_COL].min())
print("End  :", api2[DATE_COL].max())


# =========================
# STATION + DISTRICT
# =========================

print("\n" + "=" * 60)
print("STATION & DISTRICT")
print("=" * 60)

print("\nAPI 1:")
print(api1[["Station", "District"]].drop_duplicates().to_string(index=False))

print("\nAPI 2:")
print(api2[["Station", "District"]].drop_duplicates().to_string(index=False))


# =========================
# MISSING VALUES
# =========================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print("\nAPI 1 missing values:")
print(api1.isnull().sum())

print("\nAPI 2 missing values:")
print(api2.isnull().sum())


# =========================
# DUPLICATE TIMESTAMPS
# =========================

print("\n" + "=" * 60)
print("DUPLICATES")
print("=" * 60)

api1_duplicates = api1.duplicated(
    subset=["Station", DATE_COL]
).sum()

api2_duplicates = api2.duplicated(
    subset=["Station", DATE_COL]
).sum()

print("API 1 duplicate timestamps:", api1_duplicates)
print("API 2 duplicate timestamps:", api2_duplicates)


# =========================
# OVERLAPPING DATES
# =========================

print("\n" + "=" * 60)
print("OVERLAPPING TIMESTAMPS")
print("=" * 60)

api1_dates = set(api1[DATE_COL].dropna())
api2_dates = set(api2[DATE_COL].dropna())

overlap = api1_dates.intersection(api2_dates)

print("Common timestamps:", len(overlap))

if len(overlap) > 0:
    print("\nFirst few common timestamps:")
    for date in sorted(overlap)[:10]:
        print(date)


# =========================
# WATER LEVEL COLUMN
# =========================

WATER_LEVEL_COL = "River Water Level Telemetry Hourly (meter)"

print("\n" + "=" * 60)
print("WATER LEVEL DATA")
print("=" * 60)

print("\nAPI 1:")
print(api1[WATER_LEVEL_COL].describe())

print("\nAPI 2:")
print(api2[WATER_LEVEL_COL].describe())


print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)




# =========================
# INSPECT API 1 DUPLICATES
# =========================

print("\n" + "=" * 60)
print("API 1 DUPLICATE TIMESTAMP EXAMPLES")
print("=" * 60)

duplicates = api1[
    api1.duplicated(
        subset=["Station", DATE_COL],
        keep=False
    )
].sort_values(["Data Acquisition Time", "_id"])

print("\nTotal duplicate rows:", len(duplicates))

print("\nFirst 20 duplicate rows:")

print(
    duplicates[
        [
            "_id",
            "Station",
            "District",
            "Data Acquisition Time",
            "River Water Level Telemetry Hourly (meter)"
        ]
    ].head(20).to_string(index=False)
)