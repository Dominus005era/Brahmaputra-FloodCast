import requests
import csv
import os


URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

RESOURCE_ID = "51640870-5961-4696-b986-b744231f1c9f"

TARGET_STATION = "NH15 Crossing Fakirpara Tangni"

LIMIT = 1000

all_records = []
offset = 0


print("Fetching API 1 data...")


while True:

    params = {
        "resource_id": RESOURCE_ID,
        "limit": LIMIT,
        "offset": offset
    }

    response = requests.get(URL, params=params)

    data = response.json()

    if not data["success"]:
        print("API ERROR")
        break

    records = data["result"]["records"]

    for row in records:

        if row.get("Station") == TARGET_STATION:
            all_records.append(row)

    print(
        f"Checked {offset + len(records)} / "
        f"{data['result']['total']} records",
        end="\r"
    )

    if len(records) < LIMIT:
        break

    offset += LIMIT


print("\n")
print("Target station:", TARGET_STATION)
print("Records found:", len(all_records))


# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)


# Save CSV
if all_records:

    file_path = "data/darrang_api1_raw.csv"

    fieldnames = all_records[0].keys()

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(all_records)


    print("Saved:", file_path)

else:

    print("No records found.")