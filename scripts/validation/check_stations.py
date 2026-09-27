import requests
from datetime import datetime


# =========================
# API 1
# =========================
URL = "https://www.nwdp.nwic.gov.in/api/action/datastore_search"

RESOURCE_ID_1 = "51640870-5961-4696-b986-b744231f1c9f"

RESOURCE_ID_2 = "847f5630-f231-46c0-922d-0f2f379a5cb8"


# =========================
# FETCH ALL RECORDS
# =========================

def fetch_all_records(resource_id):

    all_records = []
    offset = 0
    limit = 1000

    while True:

        params = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if not data["success"]:
            print("API ERROR")
            return []

        records = data["result"]["records"]

        all_records.extend(records)

        print(
            f"Fetched {len(all_records)} / "
            f"{data['result']['total']} records",
            end="\r"
        )

        if len(records) < limit:
            break

        offset += limit

    print()

    return all_records


# =========================
# ANALYZE STATIONS
# =========================

def analyze_source(records, source_name):

    stations = {}

    for row in records:

        station = row.get("Station", "Unknown")
        district = row.get("District", "Unknown")

        key = (station, district)

        if key not in stations:
            stations[key] = {
                "records": 0,
                "dates": []
            }

        stations[key]["records"] += 1

        date_text = row.get("Data Acquisition Time")

        if date_text:

            try:

                date_obj = datetime.strptime(
                    date_text,
                    "%d-%m-%Y %H:%M"
                )

                stations[key]["dates"].append(date_obj)

            except ValueError:
                pass


    print("\n")
    print("=" * 60)
    print(source_name)
    print("=" * 60)

    print("Total records:", len(records))

    for (station, district), info in stations.items():

        if info["dates"]:

            start_date = min(info["dates"]).strftime(
                "%d-%m-%Y %H:%M"
            )

            end_date = max(info["dates"]).strftime(
                "%d-%m-%Y %H:%M"
            )

        else:

            start_date = "N/A"
            end_date = "N/A"


        print("\nStation :", station)
        print("District:", district)
        print("Records :", info["records"])
        print("Start   :", start_date)
        print("End     :", end_date)


# =========================
# MAIN
# =========================

print("\nFetching API 1...")

api1_records = fetch_all_records(
    RESOURCE_ID_1
)

analyze_source(
    api1_records,
    "API 1"
)


print("\nFetching API 2...")

api2_records = fetch_all_records(
    RESOURCE_ID_2
)

analyze_source(
    api2_records,
    "API 2"
)