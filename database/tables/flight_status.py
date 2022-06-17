from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER

from ..db import Base
from . import FlightTable, FlightStatusFlagTable


class FlightStatusTable(Base):
    __tablename__ = "flight_status"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    flights_id = Column(INTEGER, ForeignKey(FlightTable.id))
    departure_timestamp = Column(INTEGER)
    arrival_timestamp = Column(INTEGER)
    flight_status_flag_id = Column(INTEGER, ForeignKey(FlightStatusFlagTable.id))

    def __init__(self, flights_id: str, departure_timestamp: int, arrival_timestamp: str, flight_status_flag_id: str):
        self.flights_id = flights_id
        self.departure_timestamp = departure_timestamp
        self.arrival_timestamp = arrival_timestamp
        self.flight_status_flag_id = flight_status_flag_id
