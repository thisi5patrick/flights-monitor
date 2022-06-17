## Flights monitor
This project is an attempt to create a REST API application with which a user will be able to get data about a flight, airline, airport and more.


### Installation
All the dependencies are managed by the `potry` tool, so to begin with, this tool must be installed with:
```shell
pip install poetry
```
After the tool is installed, run:
```shell
poetry install
```

### Creating database
Run the script `db_init.py`. This will automatically create all tables and relations with:
```shell
python database/db_init.py
```

### Filling database
There are multiple steps that has to be run in order to fill every table.
The order is crucial so keep that in mind.

#### Step 1. Fill `country` table
Run:
```shell
python scripts/fill_country_table.py
```

#### Step 2. Fill `aircraft` table
Run:
```shell
python scripts/fill_aircraft_table.py
```

#### Step 3. Fill `airline` table
Run:
```shell
python scripts/fill_airline_table.py
```

#### Step 4. Fill `airport` table
Run:
```shell
python scripts/fill_airport_table.py
```

---
The next scripts will have to work all the time, since the data is gathered on the fly.
They can be run as new instances.

#### Fill `fleet` table
Run:
```shell
python scripts/monitor_fleet.py
```
