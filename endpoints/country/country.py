from flask import Blueprint, Response, jsonify

from database.db import Session
from database.tables import CountryTable

country = Blueprint("country", __name__, url_prefix="/api/country")


@country.get("/<int:records>")
def get_all(records: int = None) -> tuple[Response, int]:
    with Session() as session:
        query = session.query(CountryTable.short_name, CountryTable.long_name)
        if records:
            query = query.limit(records)
        rows = query.all()

    result = jsonify([row._asdict() for row in rows])

    return result, 200


@country.get("/short-name/<string:short_name>/")
@country.get("/short-name/<string:short_name>/<int:records>")
def get_country_by_short_name_with_limit(short_name: str, records: int = None) -> tuple[Response, int]:
    with Session() as session:
        query = session.query(CountryTable.short_name, CountryTable.long_name).filter(
            CountryTable.short_name.like(f"{short_name}%")
        )
        if records:
            query = query.limit(records)
        rows = query.all()

    result = jsonify([row._asdict() for row in rows])
    return result, 200


@country.get("/long-name/<string:long_name>")
@country.get("/long-name/<string:long_name>/<int:records>")
def get_country_by_long_name(long_name: str, records: int = None) -> tuple[Response, int]:
    with Session() as session:
        query = session.query(CountryTable.short_name, CountryTable.long_name).filter(
            CountryTable.long_name.like(f"{long_name}%")
        )
        if records:
            query = query.limit(records)
        rows = query.all()

    result = jsonify([row._asdict() for row in rows])
    return result, 200
