### Departure airports

| Method | URL                                                        |
|--------|------------------------------------------------------------|
| GET    | https://www.ryanair.com/api/locate/v5/airports?fields=code | 

### Response

| Name | Type | Example             |
|------|------|---------------------|
|      | list | [{"code": "FAO"}, ] |

---
### Destinations

| Method | URL                                                                                                        |
|--------|------------------------------------------------------------------------------------------------------------|
| GET    | https://www.ryanair.com/api/locate/v5/routes?departureAirportCode={airportIATA}&fields=arrivalAirport.code | 

### Response

| Name | Type | Example                  |
|------|------|--------------------------|
|      | list | `arrivalAirportResponse` |

### `arrivalAirportResponse`

| Name           | Type   | Example        |
|----------------|--------|----------------|
| arrivalAirport | object | {"code": "AHO" |

---



| Method | URL                                                                                              |
|--------|--------------------------------------------------------------------------------------------------|
| GET    | https://www.ryanair.com/api/timtbl/3/schedules/{dep_icao}/{arr_icao}/years/{year}/months/{month} | 

### Request Params

| Params   | Explanation               |
|----------|---------------------------|
| dep_icao | ICAO of departure airport |
| arr_icao | ICAO of arriving airport  |
| year     | Year to check schedule    |
| month    | Month to check schedule   |

### Response

| Name  | Type   | Example      |
|-------|--------|--------------|
| month | int    | 6            |
| days  | list   | daysResponse |


#### daysResponse
| Name    | Type   | Example                                                                              |
|---------|--------|--------------------------------------------------------------------------------------|
| day     | int    | 27                                                                                   |
| flights | list   | [{"carrierCode":"FR","number":"947","departureTime":"13:00","arrivalTime":"14:00"},] |
