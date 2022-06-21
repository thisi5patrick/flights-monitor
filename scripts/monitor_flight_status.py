import datetime
from typing import Union

import requests
from constants.open_sky_api import OPEN_SKY_ENDPOINT, ALL_STATE_VECTORS
import urllib.parse
from utils.open_sky_api_dataclasses import AllStateVectorsResponse
import orjson
from database.db import Session
from database.tables import FlightTable, FlightStatusTable


class Monitor:
    def __init__(self):
        self.endpoint = urllib.parse.urljoin(OPEN_SKY_ENDPOINT, ALL_STATE_VECTORS)
        self.session = Session
        self.all_call_signs_with_ids = self.__get_all_call_signs_with_ids()

    def __get_all_call_signs_with_ids(self) -> dict:
        with self.session() as session:
            result = (session.query(FlightTable.call_sign, FlightTable.id)).all()
        return {item.call_sign: item.id for item in result}

    def __get_current_flight_status(self, flight_id: int) -> Union[None, FlightStatusTable]:
        with self.session() as session:
            result = (session.query(FlightStatusTable).filter(FlightStatusTable.flight_id == flight_id)).first()
        return result

    def __save_flight(self, flight_id: int) -> None:
        flight_status = FlightStatusTable(flight_id=flight_id, flight_status_flag_id=0)
        with self.session() as session:
            session.add(flight_status)
            session.commit()

    def __save_departure(self, flight_id: int) -> None:
        departure_timestamp = int(datetime.datetime.utcnow().timestamp())
        with self.session() as session:
            flight_status: FlightStatusTable = (
                session.query(FlightStatusTable).filter(FlightStatusTable.flight_id == flight_id).first()
            )
            flight_status.departure_timestamp = departure_timestamp
            flight_status.flight_status_flag_id = 1
            session.commit()

    def __save_arrival(self, flight_id: int) -> None:
        arrival_timestamp = int(datetime.datetime.utcnow().timestamp())
        with self.session() as session:
            flight_status: FlightStatusTable = (
                session.query(FlightStatusTable).filter(FlightStatusTable.flight_id == flight_id).first()
            )
            flight_status.arrival_timestamp = arrival_timestamp
            flight_status.flight_status_flag_id = 2
            session.commit()

    def loop(self):
        while True:
            response = requests.get(self.endpoint)
            response = orjson.loads(response.text)

            for item in response["states"]:
                item = AllStateVectorsResponse(*item)
                if item.callsign not in self.all_call_signs_with_ids:
                    continue
                flight_id = self.all_call_signs_with_ids.get(item.callsign)
                if not flight_id:
                    continue
                current_status = self.__get_current_flight_status(flight_id)
                if not current_status:
                    self.__save_flight(flight_id)
                    continue
                if current_status.flight_status_flag_id == 0 and item.on_ground is False:
                    self.__save_departure(flight_id)
                elif current_status.flight_status_flag_id == 1 and item.on_ground is True:
                    self.__save_arrival(flight_id)
                elif current_status.flight_status_flag_id == 0 and item.on_ground is True:
                    continue
                else:
                    raise Exception(f"{current_status.flight_status_flag_id=} ----- {item.on_ground=}")


monitor = Monitor()
monitor.loop()
