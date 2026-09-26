import pandas as pd

FILE = "data/darrang_api1_raw.csv"

DATE_COL = "Data Acquisition Time"
WATER_COL = "River Water Level Telemetry Hourly (meter)"


# ============================================================
# LOAD RAW API 1 DATA
# ============================================================

df = pd.read_csv(FILE)

df[DATE_COL] = pd.to_datetime(
    df[DATE_COL],
    errors="coerce"
)

df[WATER_COL] = pd.to_numeric(
    df[WATER_COL],
    errors="coerce"
)

# Sort by time
df = df.sort_values(DATE_COL).reset_index(drop=True)


# ============================================================
# REMOVE DUPLICATE TIMESTAMPS
# ============================================================

df = df.drop_duplicates(
    subset=[DATE_COL],
    keep="first"
).reset_index(drop=True)


# ============================================================
# FIND MISSING WATER-LEVEL GAPS
# ============================================================

missing = df[WATER_COL].isna()

missing_groups = (
    missing != missing.shift()
).cumsum()

gaps = []

for group_id, group in df[missing].groupby(missing_groups[missing]):

    start_index = group.index.min()
    end_index = group.index.max()

    before_index = start_index - 1
    after_index = end_index + 1

    if before_index >= 0 and after_index < len(df):

        start_time = df.loc[start_index, DATE_COL]
        end_time = df.loc[end_index, DATE_COL]

        before_time = df.loc[before_index, DATE_COL]
        after_time = df.loc[after_index, DATE_COL]

        duration = after_time - before_time

        missing_count = end_index - start_index + 1

        gaps.append({
            "missing_records": missing_count,
            "start": start_time,
            "end": end_time,
            "gap_duration": duration
        })


gaps_df = pd.DataFrame(gaps)


# ============================================================
# RESULTS
# ============================================================

print("=" * 60)
print("INTERPOLATION GAP ANALYSIS")
print("=" * 60)

print("\nTotal missing values:", missing.sum())

print("Number of missing gaps:", len(gaps_df))


if len(gaps_df) > 0:

    print("\nMissing records per gap:")
    print(gaps_df["missing_records"].describe())

    print("\nGap duration:")
    print(gaps_df["gap_duration"].describe())

    print("\nLargest 20 gaps:")
    print(
        gaps_df
        .sort_values("missing_records", ascending=False)
        .head(20)
        .to_string(index=False)
    )

else:

    print("\nNo missing gaps found.")


print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)