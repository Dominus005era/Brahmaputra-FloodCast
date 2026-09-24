import requests

URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

RESOURCE_ID = "847f5630-f231-46c0-922d-0f2f379a5cb8"

params = {
    "resource_id": RESOURCE_ID,
    "limit": 1000
}

response = requests.get(URL, params=params)

print("Status Code:", response.status_code)

data = response.json()

if not data["success"]:
    print("API Error:")
    print(data)
    exit()

records = data["result"]["records"]

stations = {}

for record in records:

    station = record.get("Station")
    latitude = record.get("Latitude")
    longitude = record.get("Longitude")

    if station not in stations:
        stations[station] = {
            "latitude": latitude,
            "longitude": longitude
        }

print("\nUNIQUE STATIONS IN API 2:\n")

for station, location in stations.items():

    print(
        station,
        "| Latitude:", location["latitude"],
        "| Longitude:", location["longitude"]
    )

print("\nTotal unique stations:", len(stations))

print("Total records in API 2:", data["result"]["total"])


# ==============================================================
# API 2 RECORD STRUCTURE
# ==============================================================

print("\n" + "=" * 70)
print("API 2 RECORD STRUCTURE")
print("=" * 70)

if records:

    print("\nFirst API 2 record:")
    print(records[0])

    print("\nAPI 2 columns:")
    print(records[0].keys())

else:

    print("No records returned from API 2.")


# ==============================================================
# API 2 DATE / TIME CHECK
# ==============================================================

print("\n" + "=" * 70)
print("API 2 DATE / TIME AVAILABILITY")
print("=" * 70)

time_columns = [
    column
    for column in records[0].keys()
    if "time" in column.lower()
    or "date" in column.lower()
]

print("\nPossible date/time columns:")
print(time_columns)

for column in time_columns:

    print("\nColumn:", column)

    values = [
        record.get(column)
        for record in records
        if record.get(column) is not None
    ]

    if values:
        print("First value:", values[0])
        print("Last value :", values[-1])

print("\n" + "=" * 70)
print("API 2 DIAGNOSTIC CHECK COMPLETE")
print("=" * 70)