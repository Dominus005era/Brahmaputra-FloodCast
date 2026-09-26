import pandas as pd
import os


# ============================================================
# FILE PATHS
# ============================================================

API1_FILE = "data/darrang_api1_raw.csv"
API2_FILE = "data/darrang_api2_raw.csv"

OUTPUT_FILE = "data/darrang_water_level_final.csv"

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"


# ============================================================
# LOAD RAW DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING RAW DATA")
print("=" * 70)

api1 = pd.read_csv(API1_FILE)
api2 = pd.read_csv(API2_FILE)

print("API 1 records:", len(api1))
print("API 2 records:", len(api2))


# ============================================================
# DATE CONVERSION
# ============================================================

api1[DATE_COL] = pd.to_datetime(
    api1[DATE_COL],
    errors="coerce"
)

api2[DATE_COL] = pd.to_datetime(
    api2[DATE_COL],
    errors="coerce"
)


# ============================================================
# SORT BY TIME
# ============================================================

api1 = api1.sort_values(DATE_COL).reset_index(drop=True)
api2 = api2.sort_values(DATE_COL).reset_index(drop=True)


# ============================================================
# API 1 DUPLICATE TIMESTAMP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("API 1 DUPLICATE TIMESTAMP ANALYSIS")
print("=" * 70)

api1_duplicate_count = api1.duplicated(
    subset=[DATE_COL]
).sum()

print(
    "Duplicate timestamp rows:",
    api1_duplicate_count
)


# ============================================================
# API 1 DUPLICATE CLEANING
# ============================================================

print("\nCleaning API 1 duplicate timestamps...")

# Prefer row having a valid water level
api1["_has_level"] = api1[LEVEL_COL].notna()

api1 = (
    api1
    .sort_values(
        [DATE_COL, "_has_level"],
        ascending=[True, False]
    )
    .drop_duplicates(
        subset=[DATE_COL],
        keep="first"
    )
    .drop(columns=["_has_level"])
    .sort_values(DATE_COL)
    .reset_index(drop=True)
)

print(
    "API 1 records after duplicate cleaning:",
    len(api1)
)


# ============================================================
# API 1 MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("API 1 MISSING WATER LEVEL")
print("=" * 70)

missing_before = api1[LEVEL_COL].isna().sum()

print(
    "Missing water-level values:",
    missing_before
)


# ============================================================
# IDENTIFY LONG GAPS
# ============================================================

print("\nIdentifying long missing gaps...")

missing_mask = api1[LEVEL_COL].isna()

# Give every continuous missing section a group number
gap_group = (
    missing_mask
    .ne(missing_mask.shift())
    .cumsum()
)

long_gap_groups = []

for group_id, group in api1.groupby(gap_group):

    if not group[LEVEL_COL].isna().all():
        continue

    missing_count = len(group)

    if missing_count >= 10:
        long_gap_groups.append(group_id)


print(
    "Long gaps (>=10 missing records):",
    len(long_gap_groups)
)


# ============================================================
# SAVE LONG-GAP MASK
# ============================================================

api1["_long_gap"] = gap_group.isin(long_gap_groups)


# ============================================================
# INTERPOLATION
# ============================================================

print("\n" + "=" * 70)
print("INTERPOLATION")
print("=" * 70)

# Time-based interpolation
api1 = api1.set_index(DATE_COL)

before_interpolation = api1[LEVEL_COL].isna().sum()

# Interpolate only short gaps
interpolated = api1[LEVEL_COL].interpolate(
    method="time",
    limit=9,
    limit_direction="both"
)

# Restore long gaps as NaN
interpolated[api1["_long_gap"]] = pd.NA

api1[LEVEL_COL] = interpolated

api1 = api1.reset_index()


# ============================================================
# INTERPOLATION RESULT
# ============================================================

after_interpolation = api1[LEVEL_COL].isna().sum()

values_interpolated = (
    before_interpolation - after_interpolation
)

print(
    "Values interpolated:",
    values_interpolated
)

print(
    "Remaining missing values:",
    after_interpolation
)

print(
    "Long gaps preserved as NaN:",
    len(long_gap_groups)
)


# Remove helper column
api1 = api1.drop(columns=["_long_gap"])


# ============================================================
# API 2 CLEANING
# ============================================================

print("\n" + "=" * 70)
print("API 2 CLEANING")
print("=" * 70)

# IMPORTANT:
# API 2 previously had ZERO duplicate timestamps.
# Therefore we do NOT remove rows unnecessarily.

api2_duplicate_count = api2.duplicated(
    subset=[DATE_COL]
).sum()

print(
    "API 2 duplicate timestamps:",
    api2_duplicate_count
)

if api2_duplicate_count > 0:

    api2["_has_level"] = api2[LEVEL_COL].notna()

    api2 = (
        api2
        .sort_values(
            [DATE_COL, "_has_level"],
            ascending=[True, False]
        )
        .drop_duplicates(
            subset=[DATE_COL],
            keep="first"
        )
        .drop(columns=["_has_level"])
    )

print(
    "API 2 records after cleaning:",
    len(api2)
)

print(
    "API 2 missing water-level values:",
    api2[LEVEL_COL].isna().sum()
)


# ============================================================
# COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("COLUMN CHECK")
print("=" * 70)

print(
    "API 1 and API 2 columns match:",
    list(api1.columns) == list(api2.columns)
)


# ============================================================
# COMBINE API 1 + API 2
# ============================================================

print("\n" + "=" * 70)
print("COMBINING API 1 + API 2")
print("=" * 70)

combined = pd.concat(
    [api1, api2],
    ignore_index=True
)


# ============================================================
# CROSS-API DUPLICATE CHECK
# ============================================================

before_cross_duplicate = len(combined)

combined = (
    combined
    .sort_values(DATE_COL)
    .drop_duplicates(
        subset=[DATE_COL],
        keep="first"
    )
    .reset_index(drop=True)
)

cross_api_duplicates = (
    before_cross_duplicate - len(combined)
)

print(
    "Cross-API duplicate timestamps removed:",
    cross_api_duplicates
)


# ============================================================
# FINAL SORT
# ============================================================

combined = combined.sort_values(
    DATE_COL
).reset_index(drop=True)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET VALIDATION")
print("=" * 70)

print(
    "Total records:",
    len(combined)
)

print(
    "Stations:",
    combined["Station"].nunique()
)

print(
    "Districts:",
    combined["District"].unique()
)

print(
    "Start date:",
    combined[DATE_COL].min()
)

print(
    "End date:",
    combined[DATE_COL].max()
)

print(
    "Missing water levels:",
    combined[LEVEL_COL].isna().sum()
)

print(
    "Duplicate timestamps:",
    combined.duplicated(
        subset=[DATE_COL]
    ).sum()
)


# ============================================================
# WATER LEVEL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("WATER LEVEL STATISTICS")
print("=" * 70)

print(
    combined[LEVEL_COL].describe()
)


# ============================================================
# SAVE FINAL DATASET
# ============================================================

combined.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("SAVED SUCCESSFULLY")
print("=" * 70)

print(
    "File:",
    OUTPUT_FILE
)