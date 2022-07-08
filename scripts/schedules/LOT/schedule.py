import time
from copy import deepcopy
from datetime import date, datetime, timedelta

import orjson
import requests

from scripts.schedules import common
from scripts.schedules.LOT.secrets import *
from utils.time_to_seconds import time_to_seconds

AIRLINE = "LOT - Polish Airlines"

AIRLINE_ID = common.get_airline_id(AIRLINE)
URL = "https://www.lot.com/api/us/en/flightstatus.airport.json"
PARAMS = {
    "date": "",
}
HEADERS = {"X-CSRF-TOKEN": X_CSRF_TOKEN, "Cookie": COOKIE}


def get_airports() -> list:
    airports_url = "https://www.lot.com/api/be/en/airports.json"
    response = requests.get(airports_url)
    response = orjson.loads(response.text)
    airports = []
    for country in response["countries"]:
        for city in country["cities"]:
            for airport in city["airports"]:
                airports.append(airport["IATAcode"])
    return airports


def run_loop_with_parameter(parameter: str, airports: list):
    params = deepcopy(PARAMS)
    for airport in airports:
        params[parameter] = airport
        day = date.today()
        days_counter = 0
        while days_counter < 200:
            params["date"] = day.strftime("%Y-%m-%d")
            request = requests.post(URL, json=params, headers=HEADERS)
            if request.status_code != 200:
                time.sleep(time_to_seconds(minutes=10))
                request = requests.post(URL, json=params, headers=HEADERS)
            request = orjson.loads(request.text)
            for flight_day in request["flightStatuses"].values():
                for flight in flight_day:
                    departure_airport = flight["departureIATASched"]
                    destination_airport = flight["arrivalIATASched"]
                    departure = datetime.strptime(flight["departureSchedDtUtc"][:-6], "%Y-%m-%dT%H:%M:%S")
                    arrival = datetime.strptime(flight["arrivalSchedDtUtc"][:-6], "%Y-%m-%dT%H:%M:%S")
                    departure_time = departure.strftime("%H%M")
                    arrival_time = arrival.strftime("%H%M")
                    flight_no = flight["carrierCode"] + str(flight["flightNumber"])
                    common.save_schedule(
                        AIRLINE_ID,
                        departure_airport,
                        destination_airport,
                        departure_time,
                        arrival_time,
                        departure,
                        flight_no,
                    )
            day += timedelta(days=7)
            days_counter += 7


def schedule():
    airports = get_airports()
    parameters = ["departureIATA", "arrivalIATA"]
    run_loop_with_parameter(parameters[0], airports)
    run_loop_with_parameter(parameters[1], airports)


if __name__ == "__main__":
    schedule()
