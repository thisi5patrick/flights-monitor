from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db import Base


class FlightStatusFlagTable(Base):
    __tablename__ = "flight_status_flag"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    status = Column(TEXT)

    def __init__(self, status: str):
        self.status = status
