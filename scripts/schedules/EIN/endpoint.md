| Method | URL                                                                                                                        |
|--------|----------------------------------------------------------------------------------------------------------------------------|
| GET    | https://www.aerlingus.com/api/timetables?arrivalAirport={arrivalAirport}&departureAirport={departureAirport}&month={month} | 

### Request Params

| Required | Parameter        | type | Example |
|----------|------------------|------|---------|
| True     | arrivalAirport   | str  | ATH     |
| True     | departureAirport | str  | AMS     |
| True     | month            | int  | 6       |


### Response

| Name     | Type   | Example        |
|----------|--------|----------------|
| data     | object | `dataResponse` |
| messages | list   | []             |


#### dataResponse
| Name             | Type | Example                 |
|------------------|------|-------------------------|
| arrivalAirport   | str  | DUB                     |
| departureAirport | str  | FRA                     |
| month            | int  | 7                       |
| timeTableList    | list | `timeTableListResponse` |

#### timeTableListResponse

| Name | Type   | Example                     |
|------|--------|-----------------------------|
| 0    | object | `timeTableEntitiesResponse` |

#### timeTableEntitiesResponse

| Name                   | Type | Example       |
|------------------------|------|---------------|
| flightNo               | str  | El651         |
| validFrom              | int  | 1648339200000 |
| daysOfService          | str  | M T W T F S S |
| aircraftType           | str  | n/a           |
| departureAirport       | str  | FRA           |
| departureTerminal      | str  | 2             |
| departureTime          | str  | 1055          |
| arrivalTerminal        | str  | DUB           |
| arrivalTerminal        | str  | 2             |
| arrivalTime            | str  | 1215          |
| nextDayIndicator       | bool | False         |
| validTo                | int  | 1666998000000 |
| directFlight           | str  | Y             |
| numberOfStops          | int  | 0             |
| mealCodes              | str  | NON           |
| codeShareComments      | str  |               |
| DepartureCityName      | str  | FRANKFURT     |
| departureAirportName   | str  |               |
| destinationCityName    | str  | DUBLIN        |
| destinationAirportName | str  |               |
