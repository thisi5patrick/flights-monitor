from typing import Union, Any
from dataclasses import dataclass


@dataclass
class AllStateVectorsResponse:
    icao24: str
    callsign: str
    origin_country: str
    time_position: int
    last_contact: int
    longitude: Union[float, None]
    latitude: Union[float, None]
    baro_attitude: Union[float, None]
    on_ground: bool
    velocity: Union[float, None]
    true_track: Union[float, None]
    vertical_rate: Union[float, None]
    sensors: Union[list[int], None]
    geo_altitude: Union[float, None]
    squawk: Union[str, None]
    spi: bool
    position_source: int
    unknown_item: Any


@dataclass
class FlightsAircraftResponse:
    icao24: str
    first_seen: int
    est_departure_airport: Union[str, None]
    last_seen: int
    est_arrival_airport: Union[str, None]
    call_sign: Union[str, None]
    est_departure_airport_horiz_distance: int
    est_departure_airport_vert_distance: int
    est_arrival_airport_horiz_distance: int
    est_arrival_airport_vert_distance: int
    departure_airport_candidates_count: int
    arrival_airport_candidates_count: int
