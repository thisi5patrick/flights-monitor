

| Method | URL                                                        |
|--------|------------------------------------------------------------|
| POST   | https://en.aegeanair.com/sys/Timetable/ShowMaskMainResults | 

### Request Params

| Required | Parameter     | type | Example                       |
|----------|---------------|------|-------------------------------|
| True     | AirportFrom   | str  | ATH                           |
| True     | AirportTo     | str  | AMS                           |
| True     | TravelType    | str  | `O` - One way OR `R` - Return |
| True     | DateDeparture | str  | 29/06/2022                    |
| False    | DateReturn    | str  | "" OR 30/06/2022              |
| True     | DirectFlight  | bool | true                          |


### Response

HTML page
Needs parsing. See `parsing.py`


---
### To get the airports

| Method | URL                                           |
|--------|-----------------------------------------------|
| GET    | https://en.aegeanair.com/sys/flights/airports |

### Request Params

If param is provided, destinations from this airport will be displayed.

| Required | Parameter | type | Example |
|----------|-----------|------|---------|
| False    | airport   | str  | ATH     |
