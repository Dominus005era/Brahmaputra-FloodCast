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

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "final",
    "darrang_water_level_final.csv"
)

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("COMBINING DARRANG API 1 + API 2")
print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING CLEANED DATA")
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
# COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("COLUMN CHECK")
print("=" * 70)

if set(api1.columns) != set(api2.columns):

    print("ERROR: API 1 and API 2 columns do not match.")

    print("\nOnly in API 1:")
    print(set(api1.columns) - set(api2.columns))

    print("\nOnly in API 2:")
    print(set(api2.columns) - set(api1.columns))

    raise SystemExit

print("API 1 and API 2 columns match.")


# ============================================================
# COMBINE
# ============================================================

print("\n" + "=" * 70)
print("COMBINING DATASETS")
print("=" * 70)

combined = pd.concat(
    [api1, api2],
    ignore_index=True
)

print(
    "Records after concatenation:",
    len(combined)
)


# ============================================================
# CROSS-API DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("CROSS-API DUPLICATE CHECK")
print("=" * 70)

duplicates = combined.duplicated(
    subset=[DATE_COL],
    keep=False
)

duplicate_count = duplicates.sum()

print(
    "Rows involved in duplicate timestamps:",
    duplicate_count
)

if duplicate_count > 0:

    print("\nWARNING: Duplicate timestamps found.")

    print(
        combined.loc[
            duplicates,
            [DATE_COL, "Station", LEVEL_COL]
        ].head(20)
    )

    print("\nRemoving duplicate timestamps...")

    combined = combined.drop_duplicates(
        subset=[DATE_COL],
        keep="first"
    ).copy()

else:

    print("No cross-API duplicate timestamps found.")


# ============================================================
# SORT CHRONOLOGICALLY
# ============================================================

print("\n" + "=" * 70)
print("SORTING FINAL DATASET")
print("=" * 70)

combined = combined.sort_values(
    DATE_COL
).reset_index(drop=True)

print("Final dataset sorted chronologically.")


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
    "Invalid dates:",
    combined[DATE_COL].isna().sum()
)

print(
    "Duplicate timestamps:",
    combined.duplicated(
        subset=[DATE_COL]
    ).sum()
)

print(
    "Missing water levels:",
    combined[LEVEL_COL].isna().sum()
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


# ============================================================
# YEAR DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("RECORDS BY YEAR")
print("=" * 70)

print(
    combined[DATE_COL]
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

print(
    combined[LEVEL_COL].describe()
)


# ============================================================
# SAVE FINAL DATASET
# ============================================================

print("\n" + "=" * 70)
print("SAVING FINAL DATASET")
print("=" * 70)

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

combined.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFINAL DATASET SAVED SUCCESSFULLY")

print("\nFile:")
print(OUTPUT_FILE)

print(
    "\nFinal records saved:",
    len(combined)
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

print("\n" + "=" * 70)
print("COMBINATION COMPLETE")
print("=" * 70)