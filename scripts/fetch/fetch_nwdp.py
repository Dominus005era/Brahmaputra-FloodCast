import requests
import csv
import os

URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

RESOURCE_ID = "51640870-5961-4696-b986-b744231f1c9f"

LIMIT = 5000
offset = 0

all_records = []

while True:

    params = {
        "resource_id": RESOURCE_ID,
        "limit": LIMIT,
        "offset": offset
    }

    response = requests.get(URL, params=params)

    print("Status:", response.status_code, "Offset:", offset)

    data = response.json()

    if not data["success"]:
        print("API Error:")
        print(data)
        break

    records = data["result"]["records"]

    if not records:
        break

    all_records.extend(records)

    print("Records received:", len(records))
    print("Total collected:", len(all_records))

    offset += LIMIT

    if len(all_records) >= data["result"]["total"]:
        break


print("\nTotal records collected:", len(all_records))


# Create folder
output_folder = "data/raw"
os.makedirs(output_folder, exist_ok=True)

# CSV file
output_file = os.path.join(
    output_folder,
    "assam_water_level_2021_2025.csv"
)


# Save data
with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=all_records[0].keys()
    )

    writer.writeheader()
    writer.writerows(all_records)


print("\nCSV SAVED SUCCESSFULLY!")
print(output_file)