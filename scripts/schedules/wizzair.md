

| Method | URL                                                 |
|--------|-----------------------------------------------------|
| POST   | https://be.wizzair.com/12.10.0/Api/search/timetable | 

### Request Params

| Required | Parameter  | type | Example              |
|----------|------------|------|----------------------|
| True     | adultCount | int  | 1                    |
| True     | flightList | list | [`flightListParam`,] |


#### `flightListParam`

| Required | Parameter        | type | Example    |
|----------|------------------|------|------------|
| True     | departureStation | str  | KRK        |
| True     | arrivalStation   | str  | LCA        |
| True     | from             | str  | 2022-06-27 |
| True     | to               | str  | 2022-07-31 |



### Response

list of 

| Name             | Type   | Example                                |
|------------------|--------|----------------------------------------|
| departureStation | str    | KTW                                    |
| arrivalStation   | str    | LCA                                    |
| departureDate    | str    | '2022-07-06T00:00:00'                  |
| price            | object | {'amount': 0.0, 'currencyCode': 'PLN'} |
| priceType        | str    | CheckPrice                             |
| departureDates   | list   | ['2022-07-06T06:10:00']                |
| classOfService   | str    | F                                      |
| hasMacFlight     | bool   | True                                   |




