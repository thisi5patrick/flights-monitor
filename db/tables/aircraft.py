from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db_init import Base


class AircraftTable(Base):
    __tablename__ = "aircraft"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    model = Column(TEXT)
    model_acronym = Column(TEXT)
    iata = Column(TEXT)

