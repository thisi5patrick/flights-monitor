import datetime
import time
import urllib.parse
from itertools import chain
from typing import NoReturn, Union

import orjson
import requests

from constants import *
from database.db import Session
from database.tables import *
from utils.open_sky_api_dataclasses import FlightsAircraftResponse
from utils.time_to_seconds import time_to_seconds


class Monitor:
    def __init__(self):
        self.session = Session
        self.endpoint = urllib.parse.urljoin(OPEN_SKY_ENDPOINT, FLIGHTS_AIRCRAFT)

    def __get_fleet(self, **kwargs) -> list[str]:
        with self.session() as session:
            result = session.query(FleetTable.transpoder_icao).all()

        return list(chain.from_iterable(result))

    @staticmethod
    def __prepare_request_params(icao: str) -> dict:
        begin = (datetime.datetime.utcnow() - datetime.timedelta(days=15)).timestamp()
        end = datetime.datetime.utcnow().timestamp()
        return {
            "icao24": icao,
            "begin": int(begin),
            "end": int(end),
        }

    def __get_airport_id(self, airport_icao: str) -> Union[int, None]:
        with self.session() as session:
            result = session.query(AirportTable.id).filter(AirportTable.icao == airport_icao).first()
        if result:
            return result[0]
        return None

    def __get_airline_id(self, flight_callsign: str) -> Union[int, None]:
        callsign = flight_callsign[:3].upper()
        with self.session() as session:
            result = session.query(AirlineTable.id).filter(AirlineTable.call_sign == callsign).first()
        if result:
            return result[0]
        return None

    def __add_flight_to_database(self, **kwargs):
        departure_airport_id = kwargs["departure_airport_id"]
        arrival_airport_id = kwargs["arrival_airport_id"]
        call_sign = kwargs["call_sign"]
        airline_id = kwargs["airline_id"]
        with self.session() as session:
            flight = FlightTable(
                call_sign=call_sign,
                airline_id=airline_id,
                arrival_airport_id=arrival_airport_id,
                departure_airport_id=departure_airport_id,
            )
            session.add(flight)
            session.commit()

    def __is_call_sign_saved(self, call_sign: str) -> bool:
        with self.session() as session:
            result = session.query(FlightTable.id).filter(FlightTable.call_sign == call_sign).first()
        if result:
            return True
        return False

    def loop(self) -> NoReturn:
        while True:
            fleet = self.__get_fleet()
            for aircraft in fleet:
                params = self.__prepare_request_params(aircraft)
                response = requests.get(self.endpoint, params=params)
                if response.status_code != 200:
                    continue
                data = orjson.loads(response.text)
                for flight in data:
                    flight = FlightsAircraftResponse(*flight.values())
                    if flight.call_sign is None:
                        continue
                    call_sign = flight.call_sign.strip()
                    if self.__is_call_sign_saved(call_sign):
                        continue
                    departure_airport_id = self.__get_airport_id(flight.est_departure_airport)
                    arrival_airport_id = self.__get_airport_id(flight.est_arrival_airport)
                    airline_id = self.__get_airline_id(call_sign)
                    if any(item is None for item in [departure_airport_id, arrival_airport_id, call_sign, airline_id]):
                        continue
                    self.__add_flight_to_database(
                        departure_airport_id=departure_airport_id,
                        arrival_airport_id=arrival_airport_id,
                        call_sign=call_sign,
                        airline_id=airline_id,
                    )
            time.sleep(time_to_seconds(days=1))


monitor = Monitor()
monitor.loop()
