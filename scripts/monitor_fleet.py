"""
This script extracts the fleet using the OpenSky API.
Every 15 minutes a call is made to the API to extract all aircrafts currently picked by the sensors of the OpenSky.
From this call, the transpoder icao and flight call sign is extracted.
The transpoder icao is unique to every airplane.
To determine the flight airline, the first 3 characters of the flight call sign is extracted, since those 3 characters
correspond to one or child/parent airline.
Doing so, we are able to join each airplane to their airline.
The aircraft is extracted from the AdsExchange site. Doing a proper url call, the aircraft acronym can be returned.

If any of the 3 extracted items (transpoder icao, airline, aircraft type) is None, that means that the aircraft
may be private, or the aircraft does not belong to an airline.
"""

import sqlite3
from typing import Union

from constants import *
import requests
import time
import urllib.parse
import orjson


class Monitor:
    def __init__(self):
        self.con = sqlite3.connect("../database.db")
        self.endpoint = urllib.parse.urljoin(OPEN_SKY_ENDPOINT, ALL_STATE_VECTORS)

    def __check_if_transpoder_saved(self, transpoder_icao: str) -> bool:
        exists = self.con.execute(f"select id from fleet where transpoder_icao=?", (transpoder_icao,)).fetchone()
        if exists:
            return True
        return False

    def __get_airline_id(self, callsign: str) -> Union[int, None]:
        airline_icao_upper = callsign[:3].upper()
        airline_id = self.con.execute("select id from airline where call_sign=?", (airline_icao_upper,)).fetchone()
        if airline_id:
            return airline_id[0]
        return None

    def __get_aircraft_type_id(self, transpoder_icao: str) -> Union[int, None]:
        icao_last_digits = transpoder_icao[-2:]
        headers = {"Referer": ADSBEXCHANGE_ICAO % transpoder_icao}
        response = requests.get(ADSBEXCHANGE_AIRCRAFT_INFO % (icao_last_digits, transpoder_icao), headers=headers)
        if response.status_code != 200:
            return None
        data = orjson.loads(response.text)
        aircraft_type = data.get("t")
        aircraft_type_id = self.con.execute(
            "select id from aircraft where model_acronym=?", (aircraft_type,)
        ).fetchone()
        if aircraft_type_id:
            return aircraft_type_id[0]
        return None

    def monitor(self):
        while True:
            response = requests.get(self.endpoint)
            data = orjson.loads(response.text)
            for flight in data["states"]:
                transpoder_icao = flight[0]
                if self.__check_if_transpoder_saved(transpoder_icao):
                    continue
                airline_id = self.__get_airline_id(flight[1])
                aircraft_type_id = self.__get_aircraft_type_id(transpoder_icao)
                if airline_id is None or aircraft_type_id is None or transpoder_icao is None:
                    continue
                self.con.execute(
                    "insert into fleet(transpoder_icao, airline_id, aircraft_id) values (?,?,?)",
                    (transpoder_icao, airline_id, aircraft_type_id),
                )
                self.con.commit()
            time.sleep(900)


monitor_fleet = Monitor()
monitor_fleet.monitor()
