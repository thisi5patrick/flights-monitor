import time
from datetime import datetime, timedelta

import orjson
import pytz
import requests
from database.db import Session
from database.tables import AirportTable, AirlineTable, FlightScheduleTable
from itertools import chain, product
from timezonefinder import TimezoneFinder

from utils.time_to_seconds import time_to_seconds

AIRLINE = "Aer Lingus"
tzfinder = TimezoneFinder()


def get_airline_id() -> int:
    with Session() as session:
        result = session.query(AirlineTable.id).filter(AirlineTable.long_name == AIRLINE).first()[0]
    return result


AIRLINE_ID = get_airline_id()
URL = "https://www.aerlingus.com/api/timetables"
PARAMS = {"arrivalAirport": "", "departureAirport": "", "month": ""}
MONTHS = list(range(1, 13))


def get_airports():
    with Session() as session:
        result = session.query(AirportTable.iata).all()
    return list(chain.from_iterable(result))


def get_airport_by_iata(iata: str) -> AirportTable:
    with Session() as session:
        result = session.query(AirportTable).filter(AirportTable.iata == iata).first()
    return result


def parse_days(days: list, valid_from: int, valid_to: int) -> list[datetime]:
    valid_from = datetime.fromtimestamp(valid_from // 1000)
    valid_to = datetime.fromtimestamp(valid_to // 1000)
    delta = valid_to - valid_from
    days_operational = []
    for day in range(delta.days + 1):
        day = valid_from + timedelta(days=day)
        if days[day.weekday()] != "-":
            days_operational.append(day)
    return days_operational


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
    departing_airport: str,
    destination_airport: str,
    departure_time: str,
    arrival_time: str,
    departure_day: datetime,
    flight_no: str,
) -> None:
    departing_airport = get_airport_by_iata(departing_airport)
    destination_airport = get_airport_by_iata(destination_airport)

    dep_timezone_str = tzfinder.timezone_at(lat=departing_airport.latitude, lng=departing_airport.longitude)
    dep_timezone = pytz.timezone(dep_timezone_str)

    dest_timezone_str = tzfinder.timezone_at(lat=destination_airport.latitude, lng=destination_airport.longitude)
    dest_timezone = pytz.timezone(dest_timezone_str)

    if departure_time <= "2359" and arrival_time > "0000":
        arrival_day = departure_day + timedelta(days=1)
    else:
        arrival_day = departure_day

    arrival_timestamp = parse_time(arrival_day, arrival_time, dest_timezone)
    departure_timestamp = parse_time(departure_day, departure_time, dep_timezone)

    if flight_exists(departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp):
        return

    flight_no = flight_no.replace(" ", "")

    with Session() as session:
        result = FlightScheduleTable(
            AIRLINE_ID, departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp, flight_no
        )
        session.add(result)
        session.commit()


def schedule():
    airports = get_airports()
    for dep_airport, dest_airport in product(airports, airports):
        PARAMS["arrivalAirport"] = dest_airport
        PARAMS["departureAirport"] = dep_airport
        for month in MONTHS:
            PARAMS["month"] = month
            try:
                response = requests.get(URL, params=PARAMS)
            except requests.exceptions.ConnectionError:
                time.sleep(time_to_seconds(minutes=10))
                continue
            if response.status_code != 200:
                time.sleep(time_to_seconds(minutes=10))
                continue
            data = orjson.loads(response.text)
            if (
                not data["data"]["timeTableList"][0]["timeTableEntries"]
                and not data["data"]["timeTableList"][1]["timeTableEntries"]
            ):
                continue
            to_flights = data["data"]["timeTableList"][0]["timeTableEntries"]
            try:
                return_flights = data["data"]["timeTableList"][1]["timeTableEntries"]
            except IndexError:
                return_flights = None
            for flight in to_flights:
                operation_days = flight["daysOfService"].split(" ")
                operation_days = parse_days(operation_days, flight["validFrom"], flight["validTo"])
                for day in operation_days:
                    save_schedule(
                        dep_airport,
                        dest_airport,
                        flight["departureTime"],
                        flight["arrivalTime"],
                        day,
                        flight["flightNo"],
                    )
            if not return_flights:
                continue
            for flight in return_flights:
                operation_days = flight["daysOfService"].split(" ")
                operation_days = parse_days(operation_days, flight["validFrom"], flight["validTo"])
                for day in operation_days:
                    save_schedule(
                        dep_airport,
                        dest_airport,
                        flight["departureTime"],
                        flight["arrivalTime"],
                        day,
                        flight["flightNo"],
                    )


if __name__ == "__main__":
    schedule()
