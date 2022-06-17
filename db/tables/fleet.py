from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db_init import Base
from . import AircraftTable, AirlineTable


class FleetTable(Base):
    __tablename__ = "fleet"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    transpoder_icao = Column(TEXT)
    airline_id = Column(INTEGER, ForeignKey(AirlineTable.id))
    aircraft_id = Column(INTEGER, ForeignKey(AircraftTable.id))
