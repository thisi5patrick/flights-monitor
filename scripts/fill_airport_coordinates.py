import orjson
import requests

from database.db import Session
from database.tables import AirportTable


def get_airports() -> list[AirportTable]:
    with Session() as session:
        result = session.query(AirportTable).all()
    return result


def update_airport_table(airport: AirportTable, data: dict) -> None:
    coordinates = data["coordinates"].split(", ")
    longitude = coordinates[0]
    latitude = coordinates[1]
    with Session() as session:
        row = session.query(AirportTable).filter(AirportTable.id == airport.id).first()
        row.latitude = latitude
        row.longitude = longitude
        session.commit()


data = requests.get("https://datahub.io/core/airport-codes/r/airport-codes.json")

data = orjson.loads(data.text)
airports = get_airports()

for airport in airports:
    iata = airport.iata
    for line in data:
        if iata == line["iata_code"]:
            update_airport_table(airport, line)


def remove_unfilled_airports():
    with Session() as session:
        session.query(AirportTable).filter(AirportTable.latitude == None).delete()
        session.commit()


remove_unfilled_airports()
