from datetime import datetime, timedelta

import pytz
from timezonefinder import TimezoneFinder

from database.db import Session
from database.tables import AirlineTable, AirportTable, FlightScheduleTable

tzfinder = TimezoneFinder()


def get_airline_id(airline_name: str) -> int:
    """
    Get airline ID based on given airline_name
    :param airline_name: long name of the airline
    :return: ID of the airline
    """
    with Session() as session:
        result = session.query(AirlineTable.id).filter(AirlineTable.long_name == airline_name).first()[0]
    return result


def flight_exists(dep_airport_id: int, dest_airport_id: int, dep_time: int, arr_time: int) -> bool:
    """
    Check if provided flight already exists in the database
    :param dep_airport_id: departing airport ID
    :param dest_airport_id: destination airport ID
    :param dep_time: departure timestamp in UTC
    :param arr_time: arriving timestamp in UTC
    :return: bool if flight exists
    """
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


def get_airport_by_iata(iata: str) -> AirportTable:
    """
    Get airport table row based on IATA code
    :param iata: IATA code
    :return: AirportTable object
    """
    with Session() as session:
        result = session.query(AirportTable).filter(AirportTable.iata == iata).first()
    return result


def parse_time(day: datetime, time: str, timezone: pytz) -> int:
    """
    Parse time and return the timestamp in UTC
    :param day: day to parse
    :param time: time to parse as string of "XXXX", ex. "0830"
    :param timezone: timezone string
    :return: timestamp in UTC
    """
    hour = int(time[:2])
    minute = int(time[-2:])
    day = day.replace(hour=hour, minute=minute)
    return int(timezone.localize(day).astimezone(pytz.utc).timestamp())


def save_schedule(
    airline_id: int,
    departing_airport_iata: str,
    destination_airport_iata: str,
    departure_time: str,
    arrival_time: str,
    departure_day: datetime,
    flight_no: str = None,
) -> None:
    """
    Save schedule function to save provided schedule information.
    The function will parse the airport and select the correct timezone, while also parsing the flight arrival and departure time to the UTC time
    :param airline_id: ID from the database of the airline
    :param departing_airport_iata: IATA code of the departing airport
    :param destination_airport_iata: IATA code of the destination airport
    :param departure_time: departure time given as string of "XXXX", ex. "0830"
    :param arrival_time: arrival time given as string of "XXXX", ex. "1200"
    :param departure_day: day of the departure as datetime type
    :param flight_no: flight_no, without spaces
    """
    departing_airport = get_airport_by_iata(departing_airport_iata)
    destination_airport = get_airport_by_iata(destination_airport_iata)

    dep_timezone_str = tzfinder.timezone_at(lat=departing_airport.latitude, lng=departing_airport.longitude)
    dep_timezone = pytz.timezone(dep_timezone_str)

    dest_timezone_str = tzfinder.timezone_at(lat=destination_airport.latitude, lng=destination_airport.longitude)
    dest_timezone = pytz.timezone(dest_timezone_str)

    if departure_time > arrival_time:
        arrival_day = departure_day + timedelta(days=1)
    else:
        arrival_day = departure_day

    arrival_timestamp = parse_time(arrival_day, arrival_time, dest_timezone)
    departure_timestamp = parse_time(departure_day, departure_time, dep_timezone)

    if flight_exists(departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp):
        return

    with Session() as session:
        result = FlightScheduleTable(
            airline_id, departing_airport.id, destination_airport.id, departure_timestamp, arrival_timestamp, flight_no
        )
        session.add(result)
        session.commit()
