import time
from datetime import date, datetime, timedelta
from urllib.parse import urljoin

import orjson
import requests
from dateutil.relativedelta import relativedelta

from scripts.schedules import common
from utils.time_to_seconds import time_to_seconds

AIRLINE = "Wizz Air"
AIRLINE_ID = common.get_airline_id(AIRLINE)

API_URL = "https://wizzair.com/static_fe/metadata.json"
DESTINATIONS_URL = "/asset/map?languageCode=en-gb"
SCHEDULE_URL = "/search/timetable"
SEARCH_URL = "/search/search"
PARAMS = {
    "adultCount": 1,
    "flightList": [
        {
            "departureStation": "",
            "arrivalStation": "",
            "from": "",
            "to": "",
        },
        {
            "departureStation": "",
            "arrivalStation": "",
            "from": "",
            "to": "",
        }
    ],
}


def get_api_url() -> str:
    response = requests.get(API_URL)
    response = orjson.loads(response.text)
    return response["apiUrl"]


def get_destinations(api_url: str) -> list:
    destinations = []
    url = f"{api_url}{DESTINATIONS_URL}"
    response = requests.get(url)
    response = orjson.loads(response.text)
    for city in response["cities"]:
        from_ = city["iata"]
        to_ = []
        for connection in city["connections"]:
            to_.append(connection["iata"])
        destinations.append({"from": from_, "to": to_})

    return destinations


def schedule():
    api_url = get_api_url()
    destinations = get_destinations(api_url)
    url = f"{api_url}{SCHEDULE_URL}"
    search_url = f"{api_url}{SEARCH_URL}"
    months = range(9)
    for destination in destinations:
        from_airport = destination["from"]
        for to_airport in destination["to"]:
            for month in months:
                if month == 0:
                    from_date = date.today().strftime("%Y-%m-%d")
                else:
                    from_date = (date.today() + relativedelta(months=month, day=1)).strftime("%Y-%m-%d")
                to_date = (date.today() + relativedelta(months=month, day=31)).strftime("%Y-%m-%d")

                PARAMS["flightList"][0]["from"] = from_date
                PARAMS["flightList"][0]["to"] = to_date
                PARAMS["flightList"][0]["departureStation"] = from_airport
                PARAMS["flightList"][0]["arrivalStation"] = to_airport

                PARAMS["flightList"][1]["from"] = from_date
                PARAMS["flightList"][1]["to"] = to_date
                PARAMS["flightList"][1]["departureStation"] = to_airport
                PARAMS["flightList"][1]["arrivalStation"] = from_airport

                response = requests.post(url, json=PARAMS)
                response = orjson.loads(response.text)
                if response["outboundFlights"]:
                    for flight in response["outboundFlights"]:
                        for departure_date in flight["departureDates"]:
                            search_params = {
                                "adultCount": 1,
                                "flightList": [
                                    {
                                        "arrivalStation": to_airport,
                                        "departureStation": from_airport,
                                        "departureDate": datetime.strptime(departure_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                                    }
                                ]
                            }
                            search_response = requests.post(search_url, json=search_params)
                            ...


                ...
                ...



if __name__ == "__main__":
    schedule()
