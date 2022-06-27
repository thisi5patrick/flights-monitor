

| Method | URL                                                     |
|--------|---------------------------------------------------------|
| POST   | https://www.lot.com/api/us/en/flightstatus.airport.json | 

### Request Params

| Required | Parameter     | type | Example    |
|----------|---------------|------|------------|
| True     | date          | str  | 2022-06-26 |
| False    | departureIATA | str  | WAW        |
| False    | arrivalIATA   | str  | WAW        |


### Response

list of 

| Name           | Type | Example                  |
|----------------|------|--------------------------|
| flightStatuses | list | `flightStatusesResponse` |


##### `flightStatusesResponse`

| Name    | Type   | Example        |
|---------|--------|----------------|
| \<date> | object | `dateResponse` |

##### `dateResponse`

| Name                  | Type | Example                   |
|-----------------------|------|---------------------------|
| statusCode            | str  | AR                        |
| carrierCode           | str  | LO                        |
| flightNumber          | int  | 3851                      |
| originDateUtc         | str  | 2022-06-24                |
| legId                 | str  | 95495981                  |
| departureAirportSched | str  | Warsaw                    |
| departureAirportAct   | str  | Warsaw                    |
| departureIATASched    | str  | WAW                       |
| departureIATAAct      | str  | WAW                       |
| departureCitySched    | str  | Warsaw                    |
| arrivalAirportSched   | str  | Wroclaw                   |
| arrivalAirportAct     | str  | Wroclaw                   |
| arrivalIATASched      | str  | WRO                       |
| arrivalIATAAct        | str  | WRO                       |
| arrivalCitySched      | str  | Wroclaw                   |
| departureSchedDtUtc   | str  | 2022-06-24T07:05:00+02:00 |
| departureActDtUtc     | str  | 2022-06-24T07:07:00+02:00 |
| arrivalSchedDtUtc     | str  | 2022-06-24T08:05:00+02:00 |
| arrivalActDtUtc       | str  | 2022-06-24T08:02:00+02:00 |
| departureTerminal     | null | null                      |
| departureGate         | null | null                      |
| arrivalTerminal       | null | null                      |
| arrivalGate           | null | null                      |
| aircraftSubType       | str  | 789                       |






