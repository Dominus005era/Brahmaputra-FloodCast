import pandas as pd
import os

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = r"D:\document\Brahmaputra-FloodCast"

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "darrang_api1_raw.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "darrang_api1_clean.csv"
)

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"

# Maximum consecutive missing records to interpolate
INTERPOLATION_LIMIT = 9


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("LOADING API 1 RAW DATA")
print("=" * 70)

print("Input file:", INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print("Raw records:", len(df))


# ============================================================
# COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("COLUMN CHECK")
print("=" * 70)

required_columns = [
    "Station",
    "District",
    DATE_COL,
    LEVEL_COL
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("ERROR: Missing columns:")
    print(missing_columns)
    raise SystemExit

print("All required columns found.")


# ============================================================
# DATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("DATE VALIDATION")
print("=" * 70)

df[DATE_COL] = pd.to_datetime(
    df[DATE_COL],
    errors="coerce"
)

invalid_dates = df[DATE_COL].isna().sum()

print("Invalid dates:", invalid_dates)

if invalid_dates > 0:
    print("WARNING: Invalid date rows will be removed.")

    df = df.dropna(
        subset=[DATE_COL]
    ).copy()

print("Valid date records:", len(df))


# ============================================================
# WATER LEVEL NUMERIC CONVERSION
# ============================================================

print("\n" + "=" * 70)
print("WATER LEVEL CHECK")
print("=" * 70)

df[LEVEL_COL] = pd.to_numeric(
    df[LEVEL_COL],
    errors="coerce"
)

missing_before = df[LEVEL_COL].isna().sum()

print("Missing water-level values:", missing_before)


# ============================================================
# SORT BY TIMESTAMP
# ============================================================

print("\n" + "=" * 70)
print("SORTING DATA")
print("=" * 70)

df = df.sort_values(
    DATE_COL
).reset_index(drop=True)

print("API 1 data sorted chronologically.")


# ============================================================
# DUPLICATE TIMESTAMP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE TIMESTAMP ANALYSIS")
print("=" * 70)

duplicate_rows = df.duplicated(
    subset=[DATE_COL],
    keep=False
).sum()

extra_duplicates = df.duplicated(
    subset=[DATE_COL],
    keep="first"
).sum()

print("Rows involved in duplicate timestamps:", duplicate_rows)
print("Extra duplicate rows:", extra_duplicates)


# ============================================================
# CLEAN DUPLICATE TIMESTAMPS
# ============================================================

if extra_duplicates > 0:

    print("\nCleaning API 1 duplicate timestamps...")

    # Keep the last observation for every timestamp
    df = df.drop_duplicates(
        subset=[DATE_COL],
        keep="last"
    ).copy()

    print(
        "Records after duplicate cleaning:",
        len(df)
    )

else:

    print("No duplicate timestamps found.")


# ============================================================
# CREATE DATETIME INDEX
# ============================================================

df = df.set_index(
    DATE_COL
)


# ============================================================
# MISSING WATER LEVEL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING WATER LEVEL ANALYSIS")
print("=" * 70)

missing_count = df[LEVEL_COL].isna().sum()

print(
    "Missing water-level values:",
    missing_count
)


# ============================================================
# IDENTIFY LONG MISSING GAPS
# ============================================================

print("\n" + "=" * 70)
print("IDENTIFYING LONG MISSING GAPS")
print("=" * 70)

missing_mask = df[LEVEL_COL].isna()

groups = (
    missing_mask
    .ne(missing_mask.shift())
    .cumsum()
)

gap_sizes = (
    missing_mask
    .groupby(groups)
    .sum()
)

long_gap_groups = gap_sizes[
    gap_sizes >= 10
]

print(
    "Long missing gaps (>=10 records):",
    len(long_gap_groups)
)

if len(long_gap_groups) > 0:

    print("\nLong gaps:")

    for group_id, gap_size in long_gap_groups.items():

        gap_rows = df[
            groups == group_id
        ]

        print(
            f"{gap_rows.index.min()} → "
            f"{gap_rows.index.max()} "
            f"({int(gap_size)} missing records)"
        )


# ============================================================
# INTERPOLATION
# ============================================================

print("\n" + "=" * 70)
print("INTERPOLATION")
print("=" * 70)

before_interpolation = df[LEVEL_COL].isna().sum()

# Time interpolation only for short gaps.
# Maximum 9 consecutive missing records.
interpolated = df[LEVEL_COL].interpolate(
    method="time",
    limit=INTERPOLATION_LIMIT,
    limit_direction="both"
)

df[LEVEL_COL] = interpolated

after_interpolation = df[LEVEL_COL].isna().sum()

values_interpolated = (
    before_interpolation -
    after_interpolation
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
    "Long gaps (10+ records) preserved as NaN."
)


# ============================================================
# RESET INDEX
# ============================================================

df = df.reset_index()


# ============================================================
# FINAL SORT
# ============================================================

df = df.sort_values(
    DATE_COL
).reset_index(drop=True)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET VALIDATION")
print("=" * 70)

print(
    "Final records:",
    len(df)
)

print(
    "Missing dates:",
    df[DATE_COL].isna().sum()
)

print(
    "Duplicate timestamps:",
    df.duplicated(
        subset=[DATE_COL]
    ).sum()
)

print(
    "Missing water levels:",
    df[LEVEL_COL].isna().sum()
)

print(
    "Start date:",
    df[DATE_COL].min()
)

print(
    "End date:",
    df[DATE_COL].max()
)

print(
    "Stations:",
    df["Station"].nunique()
)

print(
    "Districts:",
    df["District"].unique()
)


# ============================================================
# WATER LEVEL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("WATER LEVEL STATISTICS")
print("=" * 70)

print(
    df[LEVEL_COL].describe()
)


# ============================================================
# SAVE
# ============================================================

print("\n" + "=" * 70)
print("SAVING CLEAN API 1")
print("=" * 70)

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "API 1 CLEANING COMPLETE"
)

print("\nOutput file:")
print(OUTPUT_FILE)

print(
    "\nFinal records saved:",
    len(df)
)

print(
    "\nShort missing gaps were interpolated."
)

print(
    "Long gaps (10+ records) were preserved as NaN."
)

print(
    "Duplicate timestamps were removed."
)

print("=" * 70)