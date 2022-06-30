import datetime
import time
from datetime import date, timedelta
from urllib.parse import urljoin

import orjson
import pytz
import requests
import requests.exceptions
from lxml import html
from timezonefinder import TimezoneFinder

from database.db import Session
from database.tables import AirlineTable, AirportTable, FlightScheduleTable
from utils.time_to_seconds import time_to_seconds

AIRLINE = "Aegean Airlines"


def get_airline_id() -> int:
    with Session() as session:
        result = session.query(AirlineTable.id).filter(AirlineTable.long_name == AIRLINE).first()[0]
    return result


URL = "https://en.aegeanair.com/sys/Timetable/ShowMaskMainResults"
AIRPORTS_URL = "https://en.aegeanair.com/sys/flights/airports"
PARAMS = {
    "AirportFrom": "",
    "AirportTo": "",
    "TravelType": "O",
    "DateDeparture": "",
    "DateReturn": "",
    "DirectFlight": "true",
}
AIRLINE_ID = get_airline_id()
tzfinder = TimezoneFinder()


def get_departure_airports() -> list[str]:
    response = requests.get(AIRPORTS_URL)
    airports = orjson.loads(response.text)

    return [item["value"] for item in airports]


def get_destination_airports(airport: str) -> list[str]:
    url = urljoin(AIRPORTS_URL, f"?airport={airport}")

    response = requests.get(url)
    airports = orjson.loads(response.text)
    return [item["value"] for item in airports]


def get_airport_by_iata(iata: str) -> AirportTable:
    with Session() as session:
        result = session.query(AirportTable).filter(AirportTable.iata == iata).first()
    return result


def parse_time(day: datetime, time: str, timezone: pytz) -> int:
    hour = int(time[:2])
    minute = int(time[-2:])
    day = day.replace(hour=hour, minute=minute)
    return int(timezone.localize(day).astimezone(pytz.utc).timestamp())


def flight_exists(dep_airport_id: int, dest_airport_id: int, dep_time: int, arr_time: int) -> bool:
    with Session() as session:
        result = (
            session.query(FlightScheduleTable)
            .filter(FlightScheduleTable.departure_airport_id == dep_airport_id)
            .filter(FlightScheduleTable.destination_airport_id == dest_airport_id)
            .filter(FlightScheduleTable.departure_timestamp_utc == dep_time)
            .filter(FlightScheduleTable.destination_timestamp_utc == arr_time)
            .first()
        )
    if result:
        return True
    return False


def save_schedule(
    departing_airport: str, destination_airport: str, departure_time: str, arrival_time: str, departure_day: str
) -> None:
    departing_airport = get_airport_by_iata(departing_airport)
    destination_airport = get_airport_by_iata(destination_airport)

    dep_timezone_str = tzfinder.timezone_at(lat=departing_airport.latitude, lng=departing_airport.longitude)
    dep_timezone = pytz.timezone(dep_timezone_str)

    dest_timezone_str = tzfinder.timezone_at(lat=destination_airport.latitude, lng=destination_airport.longitude)
    dest_timezone = pytz.timezone(dest_timezone_str)

    departure_day = datetime.datetime.strptime(departure_day, "%Y-%m-%d")

    if departure_time <= "2359" and arrival_time > "0000":
        arrival_day = departure_day + datetime.timedelta(days=1)
    else:
        arrival_day = departure_day

    arrival_timestamp = parse_time(arrival_day, arrival_time, dest_timezone)
    departure_timestamp = parse_time(departure_day, departure_time, dep_timezone)

    if flight_exists(departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp):
        return

    with Session() as session:
        result = FlightScheduleTable(
            AIRLINE_ID, departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp
        )
        session.add(result)
        session.commit()


def schedule():
    departure_airports = get_departure_airports()

    for dep_airport in departure_airports:
        destination_airports = get_destination_airports(dep_airport)
        for dest_airport in destination_airports:
            day = date.today()
            days_counter = 0
            PARAMS["AirportFrom"] = dep_airport
            PARAMS["AirportTo"] = dest_airport

            while days_counter < 200:
                PARAMS["DateDeparture"] = day.strftime("%d/%m/%Y")

                try:
                    response = requests.post(URL, json=PARAMS)
                except requests.exceptions.ConnectionError:
                    time.sleep(time_to_seconds(minutes=10))
                    continue
                if response.status_code != 200:
                    time.sleep(time_to_seconds(minutes=10))
                    continue
                tree = html.fromstring(response.text)

                flights = tree.xpath("//td[contains(@data-flight, 'direct')]/ancestor::tr")
                if not flights:
                    break

                response = requests.post(URL, json=PARAMS)
                tree = html.fromstring(response.text)

                flights = tree.xpath("//td[contains(@data-flight, 'direct')]/ancestor::tr")
                for flight in flights:
                    flight_departure_time = flight.attrib["departuredt"]
                    flight_arrival_time = flight.attrib["arrivaldt"]
                    for validation_day in flight.findall("td"):
                        if not validation_day.attrib:
                            continue
                        flight_departure = validation_day.attrib["data-for-validation-date"]
                        save_schedule(dep_airport, dest_airport, flight_departure_time, flight_arrival_time, flight_departure)
                day += timedelta(days=7)
                days_counter += 7


if __name__ == '__main__':
    schedule()
