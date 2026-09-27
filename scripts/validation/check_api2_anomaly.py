import pandas as pd

# ============================================================
# CONFIG
# ============================================================

API2_FILE = "data/raw/darrang_api2_raw.csv"

DATE_COL = "Data Acquisition Time"
LEVEL_COL = "River Water Level Telemetry Hourly (meter)"

# ============================================================
# LOAD RAW DATA
# ============================================================

print("=" * 70)
print("API 2 RAW DATA INVESTIGATION")
print("=" * 70)

df = pd.read_csv(API2_FILE)

print("Total records:", len(df))

# ============================================================
# SHOW RAW DATE COLUMN
# ============================================================

print("\n" + "=" * 70)
print("RAW DATE VALUES")
print("=" * 70)

print("Original datatype:")
print(df[DATE_COL].dtype)

# Keep original date values
df["Original_Date"] = df[DATE_COL]

# Parse date
df["Parsed_Date"] = pd.to_datetime(
    df[DATE_COL],
    errors="coerce"
)

# ============================================================
# INVALID DATE ANALYSIS
# ============================================================

invalid = df[df["Parsed_Date"].isna()].copy()

print("\n" + "=" * 70)
print("INVALID DATE ANALYSIS")
print("=" * 70)

print("Invalid date records:", len(invalid))

if len(invalid) > 0:

    print("\nFirst 50 invalid date records:")

    print(
        invalid[
            [
                "_id",
                "Station",
                "District",
                "Original_Date",
                LEVEL_COL
            ]
        ]
        .head(50)
        .to_string(index=False)
    )

# ============================================================
# VALID DATE ANALYSIS
# ============================================================

valid = df[df["Parsed_Date"].notna()].copy()

print("\n" + "=" * 70)
print("VALID DATE ANALYSIS")
print("=" * 70)

print("Valid date records:", len(valid))
print("Unique valid timestamps:", valid["Parsed_Date"].nunique())

print("Minimum:", valid["Parsed_Date"].min())
print("Maximum:", valid["Parsed_Date"].max())

# ============================================================
# DUPLICATE TIMESTAMP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE TIMESTAMP ANALYSIS")
print("=" * 70)

duplicate_mask = (
    valid["Parsed_Date"]
    .duplicated(keep=False)
)

duplicates = valid[duplicate_mask].copy()

print("Rows involved in duplicate timestamps:", len(duplicates))

print(
    "Extra duplicate rows:",
    valid["Parsed_Date"].duplicated().sum()
)

if len(duplicates) > 0:

    print("\nFirst 50 duplicate timestamp rows:")

    print(
        duplicates[
            [
                "_id",
                "Station",
                "District",
                "Original_Date",
                "Parsed_Date",
                LEVEL_COL
            ]
        ]
        .sort_values("Parsed_Date")
        .head(50)
        .to_string(index=False)
    )

# ============================================================
# DUPLICATE GROUP EXAMPLES
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE TIMESTAMP GROUP EXAMPLES")
print("=" * 70)

duplicate_counts = (
    valid
    .groupby("Parsed_Date")
    .size()
    .sort_values(ascending=False)
)

print(
    duplicate_counts
    .head(20)
    .to_string()
)

# ============================================================
# FUTURE DATE CHECK
# ============================================================

today = pd.Timestamp.today().normalize()

future = valid[
    valid["Parsed_Date"] > today
].copy()

print("\n" + "=" * 70)
print("FUTURE DATE ANALYSIS")
print("=" * 70)

print("Today:", today)

print(
    "Future-dated valid records:",
    len(future)
)

if len(future) > 0:

    print("\nFirst 50 future records:")

    print(
        future[
            [
                "_id",
                "Parsed_Date",
                LEVEL_COL
            ]
        ]
        .sort_values("Parsed_Date")
        .head(50)
        .to_string(index=False)
    )

# ============================================================
# YEAR DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("YEAR DISTRIBUTION")
print("=" * 70)

print(
    valid["Parsed_Date"]
    .dt.year
    .value_counts()
    .sort_index()
)

# ============================================================
# MONTH DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("MONTH DISTRIBUTION")
print("=" * 70)

print(
    valid["Parsed_Date"]
    .dt.to_period("M")
    .value_counts()
    .sort_index()
)

# ============================================================
# STATION / DISTRICT
# ============================================================

print("\n" + "=" * 70)
print("STATION / DISTRICT")
print("=" * 70)

print(
    df[
        ["Station", "District"]
    ]
    .drop_duplicates()
    .to_string(index=False)
)

# ============================================================
# WATER LEVEL
# ============================================================

print("\n" + "=" * 70)
print("WATER LEVEL CHECK")
print("=" * 70)

print(
    df[LEVEL_COL]
    .describe()
)

print("\nMissing water levels:")
print(
    df[LEVEL_COL].isna().sum()
)

# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("INVESTIGATION COMPLETE")
print("=" * 70)

print(
    "NO DATA WAS MODIFIED OR DELETED."
)