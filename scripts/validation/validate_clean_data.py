import pandas as pd
import os

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = r"D:\document\Brahmaputra-FloodCast"

API1_FILE = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "darrang_api1_clean.csv"
)

API2_FILE = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "darrang_api2_clean.csv"
)

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING CLEANED DATA")
print("=" * 70)

print("API 1:", API1_FILE)
print("API 2:", API2_FILE)

api1 = pd.read_csv(API1_FILE)
api2 = pd.read_csv(API2_FILE)

api1[DATE_COL] = pd.to_datetime(api1[DATE_COL], errors="coerce")
api2[DATE_COL] = pd.to_datetime(api2[DATE_COL], errors="coerce")

print("\nAPI 1 records:", len(api1))
print("API 2 records:", len(api2))


# ============================================================
# COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("COLUMN CHECK")
print("=" * 70)

print("API 1 columns:")
print(list(api1.columns))

print("\nAPI 2 columns:")
print(list(api2.columns))

if set(api1.columns) == set(api2.columns):
    print("\nAPI 1 and API 2 columns match: TRUE")
else:
    print("\nAPI 1 and API 2 columns match: FALSE")

    print("\nOnly in API 1:")
    print(set(api1.columns) - set(api2.columns))

    print("\nOnly in API 2:")
    print(set(api2.columns) - set(api1.columns))


# ============================================================
# DATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("DATE VALIDATION")
print("=" * 70)

print("API 1 invalid dates:", api1[DATE_COL].isna().sum())
print("API 2 invalid dates:", api2[DATE_COL].isna().sum())

print("\nAPI 1 date range:")
print("Start:", api1[DATE_COL].min())
print("End  :", api1[DATE_COL].max())

print("\nAPI 2 date range:")
print("Start:", api2[DATE_COL].min())
print("End  :", api2[DATE_COL].max())


# ============================================================
# DUPLICATE TIMESTAMP CHECK
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE TIMESTAMP CHECK")
print("=" * 70)

api1_duplicates = api1.duplicated(
    subset=[DATE_COL]
).sum()

api2_duplicates = api2.duplicated(
    subset=[DATE_COL]
).sum()

print("API 1 duplicate timestamps:", api1_duplicates)
print("API 2 duplicate timestamps:", api2_duplicates)


# ============================================================
# MISSING WATER LEVEL CHECK
# ============================================================

print("\n" + "=" * 70)
print("MISSING WATER LEVEL CHECK")
print("=" * 70)

api1_missing = api1[LEVEL_COL].isna().sum()
api2_missing = api2[LEVEL_COL].isna().sum()

print("API 1 missing water levels:", api1_missing)
print("API 2 missing water levels:", api2_missing)


# ============================================================
# STATION CHECK
# ============================================================

print("\n" + "=" * 70)
print("STATION CHECK")
print("=" * 70)

print("API 1 stations:")
print(api1["Station"].unique())

print("\nAPI 2 stations:")
print(api2["Station"].unique())


# ============================================================
# DISTRICT CHECK
# ============================================================

print("\n" + "=" * 70)
print("DISTRICT CHECK")
print("=" * 70)

print("API 1 districts:")
print(api1["District"].unique())

print("\nAPI 2 districts:")
print(api2["District"].unique())


# ============================================================
# API 1 → API 2 DATE GAP
# ============================================================

print("\n" + "=" * 70)
print("API 1 → API 2 DATE GAP")
print("=" * 70)

api1_last = api1[DATE_COL].max()
api2_first = api2[DATE_COL].min()

print("API 1 last record :", api1_last)
print("API 2 first record:", api2_first)

if pd.notna(api1_last) and pd.notna(api2_first):

    gap = api2_first - api1_last

    print("Gap:", gap)

    if gap.total_seconds() < 0:
        print("WARNING: API 2 starts before API 1 ends.")
    else:
        print("Chronological order: OK")


# ============================================================
# CROSS-API OVERLAP CHECK
# ============================================================

print("\n" + "=" * 70)
print("CROSS-API TIMESTAMP OVERLAP CHECK")
print("=" * 70)

api1_dates = set(api1[DATE_COL].dropna())
api2_dates = set(api2[DATE_COL].dropna())

overlap = api1_dates.intersection(api2_dates)

print("Overlapping timestamps:", len(overlap))

if len(overlap) > 0:
    print("\nWARNING: Overlapping timestamps found.")

    print("\nFirst 20 overlapping timestamps:")

    for timestamp in sorted(overlap)[:20]:
        print(timestamp)

else:
    print("No overlapping timestamps found.")


# ============================================================
# RECORDS BY YEAR
# ============================================================

print("\n" + "=" * 70)
print("RECORDS BY YEAR")
print("=" * 70)

print("\nAPI 1:")
print(
    api1[DATE_COL]
    .dt.year
    .value_counts()
    .sort_index()
)

print("\nAPI 2:")
print(
    api2[DATE_COL]
    .dt.year
    .value_counts()
    .sort_index()
)


# ============================================================
# WATER LEVEL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("WATER LEVEL STATISTICS")
print("=" * 70)

print("\nAPI 1:")
print(api1[LEVEL_COL].describe())

print("\nAPI 2:")
print(api2[LEVEL_COL].describe())


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION STATUS")
print("=" * 70)

checks = {
    "API 1 invalid dates": api1[DATE_COL].isna().sum() == 0,
    "API 2 invalid dates": api2[DATE_COL].isna().sum() == 0,
    "API 1 duplicate timestamps": api1_duplicates == 0,
    "API 2 duplicate timestamps": api2_duplicates == 0,
    "API 1/API 2 chronological order": api1_last < api2_first,
    "Cross-API overlap": len(overlap) == 0,
}

all_passed = True

for name, result in checks.items():

    status = "PASS" if result else "FAIL"

    print(f"{status}: {name}")

    if not result:
        all_passed = False


print("\n" + "=" * 70)

if all_passed:
    print("ALL CRITICAL VALIDATION CHECKS PASSED")
    print("DATA IS READY FOR COMBINING.")
else:
    print("SOME VALIDATION CHECKS FAILED.")
    print("DO NOT COMBINE DATA YET.")

print("=" * 70)