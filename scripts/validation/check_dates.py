import pandas as pd


# ============================================================
# FILE
# ============================================================

API1_FILE = "data/darrang_api1_raw.csv"
API2_FILE = "data/darrang_api2_raw.csv"

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"


# ============================================================
# LOAD DATA
# ============================================================

api1 = pd.read_csv(API1_FILE)
api2 = pd.read_csv(API2_FILE)


# ============================================================
# DATE CONVERSION
# ============================================================

api1[DATE_COL] = pd.to_datetime(
    api1[DATE_COL],
    format="mixed",
    errors="coerce"
)

api2[DATE_COL] = pd.to_datetime(
    api2[DATE_COL],
    format="mixed",
    errors="coerce"
)


# ============================================================
# API 1 DATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("API 1 DATE CHECK")
print("=" * 70)

print("Records:", len(api1))
print("Invalid dates:", api1[DATE_COL].isna().sum())
print("Min:", api1[DATE_COL].min())
print("Max:", api1[DATE_COL].max())


# ============================================================
# API 2 DATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("API 2 DATE CHECK")
print("=" * 70)

print("Records:", len(api2))
print("Invalid dates:", api2[DATE_COL].isna().sum())
print("Min:", api2[DATE_COL].min())
print("Max:", api2[DATE_COL].max())


# ============================================================
# API 1 RECORDS BY YEAR
# ============================================================

print("\n" + "=" * 70)
print("API 1 RECORDS BY YEAR")
print("=" * 70)

api1_year = (
    api1
    .groupby(api1[DATE_COL].dt.year)
    .size()
)

print(api1_year)


# ============================================================
# API 2 RECORDS BY YEAR
# ============================================================

print("\n" + "=" * 70)
print("API 2 RECORDS BY YEAR")
print("=" * 70)

api2_year = (
    api2
    .groupby(api2[DATE_COL].dt.year)
    .size()
)

print(api2_year)


# ============================================================
# API 1 RECORDS BY MONTH
# ============================================================

print("\n" + "=" * 70)
print("API 1 RECORDS BY MONTH")
print("=" * 70)

api1_month = (
    api1
    .groupby(api1[DATE_COL].dt.to_period("M"))
    .size()
)

print(api1_month)


# ============================================================
# API 2 RECORDS BY MONTH
# ============================================================

print("\n" + "=" * 70)
print("API 2 RECORDS BY MONTH")
print("=" * 70)

api2_month = (
    api2
    .groupby(api2[DATE_COL].dt.to_period("M"))
    .size()
)

print(api2_month)


# ============================================================
# API 2 FIRST 10 RECORDS
# ============================================================

print("\n" + "=" * 70)
print("API 2 FIRST 10 RECORDS")
print("=" * 70)

first_10 = (
    api2[
        [
            "_id",
            "Station",
            "District",
            DATE_COL,
            LEVEL_COL
        ]
    ]
    .sort_values(DATE_COL)
    .head(10)
)

print(first_10.to_string(index=False))


# ============================================================
# API 2 LAST 10 RECORDS
# ============================================================

print("\n" + "=" * 70)
print("API 2 LAST 10 RECORDS")
print("=" * 70)

last_10 = (
    api2[
        [
            "_id",
            "Station",
            "District",
            DATE_COL,
            LEVEL_COL
        ]
    ]
    .sort_values(DATE_COL)
    .tail(10)
)

print(last_10.to_string(index=False))


# ============================================================
# API 2 DECEMBER 2026 CHECK
# ============================================================

print("\n" + "=" * 70)
print("API 2 DECEMBER 2026 CHECK")
print("=" * 70)

dec_2026 = api2[
    (api2[DATE_COL].dt.year == 2026) &
    (api2[DATE_COL].dt.month == 12)
].sort_values(DATE_COL)

print("December 2026 records:", len(dec_2026))

if len(dec_2026) > 0:
    print(
        dec_2026[
            [
                DATE_COL,
                LEVEL_COL
            ]
        ].to_string(index=False)
    )
else:
    print("No December 2026 records found.")


# ============================================================
# GAP BETWEEN API 1 AND API 2
# ============================================================

print("\n" + "=" * 70)
print("API 1 → API 2 DATE GAP")
print("=" * 70)

api1_max = api1[DATE_COL].max()
api2_min = api2[DATE_COL].min()

print("API 1 last record :", api1_max)
print("API 2 first record:", api2_min)

print("Gap:")
print(api2_min - api1_max)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print("API 1 records:", len(api1))
print("API 2 records:", len(api2))

print("\nAPI 1:")
print("Start:", api1[DATE_COL].min())
print("End  :", api1[DATE_COL].max())

print("\nAPI 2:")
print("Start:", api2[DATE_COL].min())
print("End  :", api2[DATE_COL].max())

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)