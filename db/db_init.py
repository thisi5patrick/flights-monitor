from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///db/database.db", echo=True, pool_pre_ping=True)

Session = sessionmaker(bind=engine)

