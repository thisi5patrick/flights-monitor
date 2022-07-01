import time
from datetime import date, datetime, timedelta

import orjson
import requests

from scripts.schedules.common import get_airline_id, save_schedule
from utils.time_to_seconds import time_to_seconds

AIRLINE = "Aero-K"


CONNECTIONS = {
    0: {"from": "CJJ", "to": "CJU"},
    1: {"from": "CJU", "to": "CJJ"},
}

URL = "https://api-production-aerok-booksecure.ezyflight.se/api/v1/Availability/SearchShop"
HEADERS = {"Tenant-Identifier": "G735CZwKYQqb7DlVTFYuc7TUXD3NMlhIdWMe49ZQ2nhhefLG0IdwXp6TcXKqL01x"}
PARAMS = {"routes": [], "passengers": [{"code": "ADT", "count": 1}], "currency": "KRW"}
AIRLINE_ID = get_airline_id(AIRLINE)


def parse_date(date_: str) -> tuple[datetime, str]:
    date_ = date_.split("T")
    day = date_[0]
    time_ = date_[1]

    day = datetime.strptime(day, "%Y-%m-%d")
    time_ = time_.replace(":", "")[:4]

    return day, time_


def schedule():
    for connection in CONNECTIONS.values():
        from_airport_iata = connection["from"]
        to_airport_iata = connection["to"]

        PARAMS["routes"] = [
            {
                "startDate": date.today().strftime("%Y-%m-%d"),
                "endDate": (date.today() + timedelta(days=200)).strftime("%Y-%m-%d"),
                "fromAirport": from_airport_iata,
                "toAirport": to_airport_iata,
            }
        ]

        try:
            response = requests.post(URL, json=PARAMS, headers=HEADERS)
        except requests.exceptions.ConnectionError:
            time.sleep(time_to_seconds(minutes=10))
            continue
        if response.status_code != 200:
            time.sleep(time_to_seconds(minutes=10))
            continue
        data = orjson.loads(response.text)
        for flight in data["routes"][0]["flights"]:
            flights_no = flight["carrierCode"] + flight["flightNumber"]
            arrival_date = flight["arrivalDate"]
            departure_date = flight["departureDate"]

            departure_day, departure_time = parse_date(departure_date)
            arrival_day, arrival_time = parse_date(arrival_date)

            save_schedule(
                AIRLINE_ID, from_airport_iata, to_airport_iata, departure_time, arrival_time, departure_day, flights_no
            )


if __name__ == "__main__":
    schedule()
