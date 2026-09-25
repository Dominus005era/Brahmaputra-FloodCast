
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "raw" / "darrang_api2_raw.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned" / "darrang_api2_clean.csv"

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"
STATION_COL = "Station"
DISTRICT_COL = "District"


# ============================================================
# HELPER FUNCTION
# ============================================================

def print_separator(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# LOAD RAW DATA
# ============================================================

print_separator("LOADING API 2 RAW DATA")

if not INPUT_FILE.exists():
    print("ERROR: API 2 raw file not found!")
    print(f"Expected file: {INPUT_FILE}")
    raise FileNotFoundError(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(f"Input file: {INPUT_FILE}")
print(f"Raw records: {len(df)}")


# ============================================================
# COLUMN CHECK
# ============================================================

print_separator("COLUMN CHECK")

required_columns = [
    DATE_COL,
    LEVEL_COL,
    STATION_COL,
    DISTRICT_COL
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("Missing required columns:")
    for col in missing_columns:
        print(f" - {col}")

    raise ValueError("Required columns are missing.")

print("All required columns found.")


# ============================================================
# ORIGINAL DATE INFORMATION
# ============================================================

print_separator("ORIGINAL DATE CHECK")

print(f"Original date datatype: {df[DATE_COL].dtype}")

# Keep original date values for investigation
df["Original_Date"] = df[DATE_COL].astype(str)


# ============================================================
# DATE PARSING
# ============================================================

print_separator("DATE PARSING")

print("Parsing API 2 dates...")

# API 2 contains values such as:
#
# 13-05-2026 00:00
#
# which require day-first parsing.
#
# We first parse normally.
# Then we retry any values that failed using dayfirst=True.

parsed_dates = pd.to_datetime(
    df[DATE_COL],
    errors="coerce"
)

failed_normal = parsed_dates.isna()

print(f"Failed with normal parsing: {failed_normal.sum()}")

if failed_normal.sum() > 0:

    parsed_dayfirst = pd.to_datetime(
        df.loc[failed_normal, DATE_COL],
        errors="coerce",
        dayfirst=True
    )

    parsed_dates.loc[failed_normal] = parsed_dayfirst

df[DATE_COL] = parsed_dates


# ============================================================
# INVALID DATE CHECK
# ============================================================

print_separator("DATE VALIDATION")

invalid_dates = df[DATE_COL].isna()

print(f"Invalid dates after recovery: {invalid_dates.sum()}")

if invalid_dates.sum() > 0:

    print()
    print("WARNING: Some dates could not be parsed.")

    print()
    print("Invalid records:")

    print(
        df.loc[
            invalid_dates,
            [
                "Original_Date",
                LEVEL_COL
            ]
        ].head(20).to_string(index=False)
    )

else:
    print("All API 2 dates successfully parsed.")


# ============================================================
# DROP ONLY UNPARSEABLE DATE RECORDS
# ============================================================

if invalid_dates.sum() > 0:

    print()
    print("Removing records with completely unparseable dates...")

    df = df.loc[~invalid_dates].copy()

    print(f"Records remaining: {len(df)}")


# ============================================================
# DUPLICATE TIMESTAMP ANALYSIS
# ============================================================

print_separator("DUPLICATE TIMESTAMP CHECK")

duplicate_mask = df[DATE_COL].duplicated(keep=False)

duplicate_rows = duplicate_mask.sum()

extra_duplicates = df[DATE_COL].duplicated(keep="first").sum()

print(f"Rows involved in duplicate timestamps: {duplicate_rows}")
print(f"Extra duplicate rows: {extra_duplicates}")


# ============================================================
# REMOVE DUPLICATE TIMESTAMPS
# ============================================================

if extra_duplicates > 0:

    print()
    print("Removing duplicate timestamps...")

    # Keep first occurrence
    df = df.drop_duplicates(
        subset=[DATE_COL],
        keep="first"
    ).copy()

    print(f"Records after duplicate cleaning: {len(df)}")

else:

    print("No duplicate timestamps found.")


# ============================================================
# SORT BY DATE
# ============================================================

print_separator("SORTING DATA")

df = df.sort_values(
    by=DATE_COL
).reset_index(drop=True)

print("API 2 data sorted chronologically.")


# ============================================================
# WATER LEVEL CHECK
# ============================================================

print_separator("WATER LEVEL CHECK")

# Convert water level to numeric.
# This does NOT interpolate or modify missing values.

df[LEVEL_COL] = pd.to_numeric(
    df[LEVEL_COL],
    errors="coerce"
)

missing_levels = df[LEVEL_COL].isna().sum()

print(f"Missing water levels: {missing_levels}")

if missing_levels > 0:
    print("WARNING: Missing water-level values exist.")
else:
    print("No missing water-level values.")


# ============================================================
# DATE RANGE
# ============================================================

print_separator("DATE RANGE")

print(f"Minimum date: {df[DATE_COL].min()}")
print(f"Maximum date: {df[DATE_COL].max()}")


# ============================================================
# DATE GAP CHECK
# ============================================================

print_separator("DATE GAP CHECK")

time_difference = df[DATE_COL].diff()

large_gaps = time_difference[
    time_difference > pd.Timedelta(hours=2)
]

print(
    f"Number of gaps greater than 2 hours: "
    f"{len(large_gaps)}"
)

if len(large_gaps) > 0:

    print()
    print("Large gaps:")

    gap_indices = large_gaps.index

    for idx in gap_indices:

        previous_time = df.loc[idx - 1, DATE_COL]
        current_time = df.loc[idx, DATE_COL]

        gap = current_time - previous_time

        print(
            f"{previous_time} → "
            f"{current_time} "
            f"({gap})"
        )


# ============================================================
# FUTURE DATE CHECK
# ============================================================

print_separator("FUTURE DATE CHECK")

today = pd.Timestamp.today().normalize()

future_mask = df[DATE_COL] > today

future_count = future_mask.sum()

print(f"Today: {today}")
print(f"Future-dated records: {future_count}")

if future_count > 0:

    print()
    print("WARNING: Future-dated records detected.")

    print(
        df.loc[
            future_mask,
            [
                DATE_COL,
                LEVEL_COL
            ]
        ].head(20).to_string(index=False)
    )

    print()
    print("IMPORTANT:")
    print("Future records are NOT deleted in this cleaning step.")

else:

    print("No future-dated records found.")


# ============================================================
# STATION / DISTRICT CHECK
# ============================================================

print_separator("STATION / DISTRICT CHECK")

print("Stations:")
print(df[STATION_COL].dropna().unique())

print()
print("Districts:")
print(df[DISTRICT_COL].dropna().unique())


# ============================================================
# YEAR DISTRIBUTION
# ============================================================

print_separator("YEAR DISTRIBUTION")

print(
    df[DATE_COL]
    .dt.year
    .value_counts()
    .sort_index()
)


# ============================================================
# MONTH DISTRIBUTION
# ============================================================

print_separator("MONTH DISTRIBUTION")

print(
    df[DATE_COL]
    .dt.to_period("M")
    .value_counts()
    .sort_index()
)


# ============================================================
# WATER LEVEL STATISTICS
# ============================================================

print_separator("WATER LEVEL STATISTICS")

print(
    df[LEVEL_COL].describe()
)


# ============================================================
# FINAL DUPLICATE CHECK
# ============================================================

print_separator("FINAL VALIDATION")

final_duplicate_count = df[DATE_COL].duplicated().sum()

final_missing_dates = df[DATE_COL].isna().sum()

final_missing_levels = df[LEVEL_COL].isna().sum()

print(f"Final records: {len(df)}")
print(f"Missing dates: {final_missing_dates}")
print(f"Duplicate timestamps: {final_duplicate_count}")
print(f"Missing water levels: {final_missing_levels}")


# ============================================================
# REMOVE TEMPORARY COLUMN
# ============================================================

# Original_Date was only needed during investigation.
# It is not required in the cleaned dataset.

df = df.drop(
    columns=["Original_Date"],
    errors="ignore"
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SAVE CLEANED DATA
# ============================================================

print_separator("SAVING CLEAN API 2")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("API 2 CLEANING COMPLETE")
print()
print(f"Output file:")
print(OUTPUT_FILE)
print()
print(f"Final records saved: {len(df)}")
print()
print("No interpolation was performed.")
print("No future records were deleted.")
print("No water-level values were modified.")

