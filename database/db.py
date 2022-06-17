from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_path = Path(__file__).resolve().parent.joinpath("database.db")

Base = declarative_base()

engine = create_engine(f"sqlite:///{database_path}", pool_pre_ping=True)

Session = sessionmaker(bind=engine)
