from flask import Blueprint, jsonify, Response
from database.db import Session
from database.tables import AirportTable, CountryTable
from sqlalchemy.sql import or_

airport = Blueprint("airport", __name__, url_prefix="/api/airport")


@airport.get("/")
@airport.get("/<int:records>")
def get_all(records: int = None) -> tuple[Response, int]:
    with Session() as session:
        query = session.query(
            CountryTable.short_name,
            CountryTable.long_name,
            AirportTable.name,
            AirportTable.icao,
            AirportTable.iata,
            AirportTable.location,
            AirportTable.latitude,
            AirportTable.longitude,
        ).join(CountryTable, CountryTable.id == AirportTable.country_id)

        if records:
            query = query.limit(records)
        rows = query.all()

    result = jsonify([row._asdict() for row in rows])
    return result, 200


@airport.get("/country/<string:country>")
@airport.get("/country/<string:country>/<int:records>")
def get_airports_by_country(country: str, records: int = None) -> tuple[Response, int]:
    with Session() as session:
        query = (
            session.query(
                CountryTable.short_name,
                CountryTable.long_name,
                AirportTable.name,
                AirportTable.icao,
                AirportTable.iata,
                AirportTable.location,
                AirportTable.latitude,
                AirportTable.longitude,
            )
            .join(CountryTable, CountryTable.id == AirportTable.country_id)
            .filter(or_(CountryTable.short_name.like(country), CountryTable.long_name.like(country)))
        )
        if records:
            query = query.limit(records)
        rows = query.all()

    result = jsonify([row._asdict() for row in rows])
    return result, 200
