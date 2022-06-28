from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from database.tables import *

database_path = Path(__file__).resolve().parent.joinpath("database.db")
engine = create_engine(f"sqlite:///{database_path}")

tables = [
    AircraftTable.__table__,
    AirlineTable.__table__,
    AirportTable.__table__,
    CountryTable.__table__,
    FleetTable.__table__,
    FlightTable.__table__,
    FlightStatusFlagTable.__table__,
    FlightStatusTable.__table__,
    FlightScheduleTable.__table__,
]

Base = declarative_base()
Base.metadata.create_all(bind=engine, tables=tables)
