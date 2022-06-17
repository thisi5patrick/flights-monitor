from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db_init import Base
from . import CountryTable


class AirportTable(Base):
    __tablename__ = "airport"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT)
    icao = Column(TEXT)
    iata = Column(TEXT)
    location = Column(TEXT)
    country_id = Column(INTEGER, ForeignKey(CountryTable.id))
