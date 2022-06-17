from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db_init import Base
from . import CountryTable


class AirlineTable(Base):
    __tablename__ = "airline"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    long_name = Column(TEXT)
    call_sign = Column(TEXT)
    country_id = Column(INTEGER, ForeignKey(CountryTable.id))
