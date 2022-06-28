from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, REAL

from ..db import Base
from . import CountryTable


class AirportTable(Base):
    __tablename__ = "airport"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT)
    icao = Column(TEXT)
    iata = Column(TEXT)
    location = Column(TEXT)
    country_id = Column(INTEGER, ForeignKey(CountryTable.id))
    latitude = Column(REAL)
    longitude = Column(REAL)
