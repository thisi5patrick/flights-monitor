from datetime import date, datetime

import orjson
import requests
from dateutil.relativedelta import relativedelta

from scripts.schedules import common

AIRLINE = "Ryanair"
AIRLINE_ID = common.get_airline_id(AIRLINE)


def get_departure_airports() -> list[str]:
    response = requests.get("https://www.ryanair.com/api/locate/v5/airports?fields=code")
    response = orjson.loads(response.text)

    airports = []
    for destination in response:
        airports.append(destination["code"])

    return airports


def get_destination_airports(departure_iata: str) -> list[str]:
    response = requests.get(
        f"https://www.ryanair.com/api/locate/v5/routes?departureAirportCode={departure_iata}&fields=arrivalAirport.code"
    )
    response = orjson.loads(response.text)

    airports = []
    for destination in response:
        airports.append(destination["arrivalAirport"]["code"])

    return airports


def schedule():
    dates = [date.today() + relativedelta(months=i) for i in range(12)]

    departure_airports = get_departure_airports()
    for departure_airport in departure_airports:
        destination_airports = get_destination_airports(departure_airport)
        for destination_airport in destination_airports:
            for date_ in dates:
                response = requests.get(
                    f"https://www.ryanair.com/api/timtbl/3/schedules/{departure_airport}/{destination_airport}/years/{date_.year}/months/{date_.month}"
                )
                response = orjson.loads(response.text)
                for day in response["days"]:
                    for flight in day["flights"]:
                        departure_time = flight["departureTime"].replace(":", "")
                        arrival_time = flight["arrivalTime"].replace(":", "")
                        flight_number = flight["carrierCode"] + str(flight["number"])
                        departure_day = datetime(year=date_.year, month=date_.month, day=day["day"])
                        common.save_schedule(
                            AIRLINE_ID,
                            departure_airport,
                            destination_airport,
                            departure_time,
                            arrival_time,
                            departure_day,
                            flight_number,
                        )


if __name__ == "__main__":
    schedule()
