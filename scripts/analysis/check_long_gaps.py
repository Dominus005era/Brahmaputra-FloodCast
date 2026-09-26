import pandas as pd

FILE = "data/darrang_api1_raw.csv"

DATE_COL = "Data Acquisition Time"
WATER_COL = "River Water Level Telemetry Hourly (meter)"

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

# Remove duplicate timestamps
df = df.drop_duplicates(
    subset=[DATE_COL],
    keep="first"
).reset_index(drop=True)

# Find missing values
missing = df[WATER_COL].isna()

groups = (missing != missing.shift()).cumsum()

results = []

for group_id, group in df[missing].groupby(groups[missing]):

    start_idx = group.index.min()
    end_idx = group.index.max()

    before_idx = start_idx - 1
    after_idx = end_idx + 1

    if before_idx >= 0 and after_idx < len(df):

        results.append({
            "missing_records": end_idx - start_idx + 1,
            "missing_start": df.loc[start_idx, DATE_COL],
            "missing_end": df.loc[end_idx, DATE_COL],
            "previous_time": df.loc[before_idx, DATE_COL],
            "next_time": df.loc[after_idx, DATE_COL],
            "previous_level": df.loc[before_idx, WATER_COL],
            "next_level": df.loc[after_idx, WATER_COL]
        })

gaps = pd.DataFrame(results)

# Show only long gaps
long_gaps = gaps[
    gaps["missing_records"] >= 10
].sort_values(
    "missing_records",
    ascending=False
)

print("=" * 70)
print("LONG MISSING WATER-LEVEL GAPS")
print("=" * 70)

print("\nNumber of gaps >= 10 missing records:",
      len(long_gaps))

print("\n")

print(
    long_gaps.to_string(index=False)
)

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)