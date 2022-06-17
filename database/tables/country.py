from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, TEXT

from ..db import Base


class CountryTable(Base):
    __tablename__ = "country"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    long_name = Column(TEXT)
    short_name = Column(TEXT)
