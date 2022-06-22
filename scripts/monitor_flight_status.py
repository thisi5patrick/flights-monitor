import datetime
from typing import Union

import requests
from constants.open_sky_api import OPEN_SKY_ENDPOINT, ALL_STATE_VECTORS
import urllib.parse
from utils.open_sky_api_dataclasses import AllStateVectorsResponse
import orjson
from database.db import Session
from database.tables import FlightTable, FlightStatusTable, FleetTable
from global_land_mask import globe


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

    def __save_flight(self, flight_id: int, fleet_id: int) -> None:
        flight_status = FlightStatusTable(flight_id=flight_id, flight_status_flag_id=1, fleet_id=fleet_id)
        with self.session() as session:
            session.add(flight_status)
            session.commit()

    def __save_departure(self, flight_id: int, fleet_id: int = None) -> None:
        departure_timestamp = int(datetime.datetime.utcnow().timestamp())
        with self.session() as session:
            flight_status: FlightStatusTable = (
                session.query(FlightStatusTable).filter(FlightStatusTable.flight_id == flight_id).first()
            )
            flight_status.departure_timestamp = departure_timestamp
            flight_status.flight_status_flag_id = 0
            if fleet_id:
                flight_status.fleet_id = fleet_id
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

    def __get_fleet_id(self, transpoder_icao: str) -> Union[int, None]:
        with self.session() as session:
            result = session.query(FleetTable.id).filter(FleetTable.transpoder_icao == transpoder_icao).first()
        if not result:
            return None
        return result[0]

    def loop(self):
        while True:
            print(f"Start: {datetime.datetime.now()}")
            response = requests.get(self.endpoint)
            response = orjson.loads(response.text)

            for current_status in response["states"]:
                current_status = AllStateVectorsResponse(*current_status)
                if current_status.callsign not in self.all_call_signs_with_ids:
                    continue
                flight_id = self.all_call_signs_with_ids.get(current_status.callsign)
                if not flight_id:
                    continue
                fleet_id = self.__get_fleet_id(current_status.icao24)
                if not fleet_id:
                    continue
                previous_status = self.__get_current_flight_status(flight_id)
                if not previous_status:
                    self.__save_flight(flight_id, fleet_id)
                    continue
                """
                IN_AIR = 0
                ON_GROUND = 1
                ARRIVED = 2
                """
                if (
                    current_status.latitude is None
                    or current_status.longitude is None
                    or current_status.velocity is None
                ):
                    continue
                if current_status.velocity > 20:
                    if previous_status.flight_status_flag_id == 1 and current_status.on_ground is False:
                        self.__save_departure(flight_id, fleet_id)
                    elif previous_status.flight_status_flag_id == 2 and current_status.on_ground is False:
                        self.__save_departure(flight_id, fleet_id)
                    elif previous_status.flight_status_flag_id == 2 and current_status.on_ground is True:
                        self.__save_departure(flight_id, fleet_id)
                    elif previous_status.flight_status_flag_id == 1 and current_status.on_ground is True:
                        self.__save_departure(flight_id, fleet_id)
                    elif previous_status.flight_status_flag_id == 0 and current_status.on_ground is True:
                        continue
                    elif previous_status.flight_status_flag_id == 0 and current_status.on_ground is False:
                        continue
                    elif previous_status.flight_status_flag_id == 2 and current_status.on_ground is True:
                        continue
                    else:
                        raise Exception(f"{previous_status.flight_status_flag_id=} ----- {current_status.on_ground=}")
                else:
                    if previous_status.flight_status_flag_id == 0 and current_status.on_ground is True:
                        self.__save_arrival(flight_id)
                    elif previous_status.flight_status_flag_id == 1 and current_status.on_ground is True:
                        continue
                    elif previous_status.flight_status_flag_id == 2 and current_status.on_ground is True:
                        continue
                    elif previous_status.flight_status_flag_id == 2 and current_status.on_ground is False:
                        continue
                    elif globe.is_ocean(current_status.latitude, current_status.longitude):
                        continue
                    elif previous_status.flight_status_flag_id == 0 and current_status.on_ground is False:
                        continue
                    elif previous_status.flight_status_flag_id == 1 and current_status.on_ground is False:
                        continue
                    else:
                        raise Exception(f"{previous_status.flight_status_flag_id=} ----- {current_status.on_ground=}")
            print(f"End: {datetime.datetime.now()}")


monitor = Monitor()
monitor.loop()
