from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db import Base
from . import AirlineTable, AirportTable


class FlightScheduleTable(Base):
    __tablename__ = "flight_schedule"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    airline_id = Column(INTEGER, ForeignKey(AirlineTable.id), nullable=False)
    departure_airport_id = Column(INTEGER, ForeignKey(AirportTable.id), nullable=False)
    destination_airport_id = Column(INTEGER, ForeignKey(AirportTable.id), nullable=False)
    departure_timestamp_utc = Column(INTEGER, nullable=False)
    destination_timestamp_utc = Column(INTEGER)
    flight_call_sign = Column(TEXT)

    def __init__(
        self,
        airline_id: int,
        departure_airport_id: int,
        destination_airport_id: int,
        departure_timestamp_utc: int,
        destination_timestamp_utc: int = None,
        flight_call_sign: str = None,
    ):
        self.airline_id = airline_id
        self.departure_airport_id = departure_airport_id
        self.destination_airport_id = destination_airport_id
        self.departure_timestamp_utc = departure_timestamp_utc
        self.destination_timestamp_utc = destination_timestamp_utc
        self.flight_call_sign = flight_call_sign
