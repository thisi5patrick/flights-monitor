from flask import Blueprint, jsonify
from database.db import Session
from database.tables import AirportTable, CountryTable

airport = Blueprint("airport", __name__, url_prefix="/api/airport")


@airport.get("/")
def get_all():
    with Session() as session:
        rows = (
            session.query(
                AirportTable.name,
                AirportTable.icao,
                AirportTable.iata,
                AirportTable.location,
                AirportTable.latitude,
                AirportTable.longitude,
            )
            .limit(1000)
            .all()
        )

    result = jsonify([row._asdict() for row in rows])

    return result


@airport.get("/<string:country_short_name>")
def get_airports_by_country(country_short_name: str):
    with Session() as session:
        rows = (
            session.query(
                AirportTable.name,
                AirportTable.icao,
                AirportTable.iata,
                AirportTable.location,
                AirportTable.latitude,
                AirportTable.longitude,
            )
            .join(CountryTable, CountryTable.id == AirportTable.country_id)
            .filter(CountryTable.short_name == country_short_name)
            .limit(1000)
            .all()
        )

    result = jsonify([row._asdict() for row in rows])

    return result
