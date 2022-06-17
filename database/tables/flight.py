from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db import Base
from . import AirportTable, AirlineTable


class FlightTable(Base):
    __tablename__ = "flight"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    call_sign = Column(TEXT)
    airline_id = Column(INTEGER, ForeignKey(AirlineTable.id))
    departure_airport_id = Column(INTEGER, ForeignKey(AirportTable.id))
    arrival_airport_id = Column(INTEGER, ForeignKey(AirportTable.id))

    def __init__(self, call_sign: str, airline_id: int, departure_airport_id: str, arrival_airport_id: str):
        self.call_sign = call_sign
        self.airline_id = airline_id
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
