### Api URL

| Method | URL                                         |
|--------|---------------------------------------------|
| GET    | https://wizzair.com/static_fe/metadata.json | 

### Response

| Name   | Type | Example                            |
|--------|------|------------------------------------|
| apiUrl | str  | https://be.wizzair.com/12.11.2/Api |


---
### Destinations

| Method | URL                                                             |
|--------|-----------------------------------------------------------------|
| GET    | https://be.wizzair.com/12.11.2/Api/asset/map?languageCode=en-gb |

### Response

| Name   | Type | Example          |
|--------|------|------------------|
| cities | list | `citiesResponse` |

### `citiesResponse`

| Name                      | Type  | Example              |
|---------------------------|-------|----------------------|
| iata                      | str   | KFZ                  |
| longitude                 | float | 20.4                 |
| currencyCode              | str   | EUR                  |
| latitude                  | float | 42.03                |
| shortName                 | str   | Kukes                |
| countryCode               | str   | AL                   |
| connections               | list  | `connectionResponse` |
| aliases                   | list  | ['Kukes',]           |
| isExcludedFromGeoLocation | bool  | False                |
| rank                      | int   | 1                    |
| categories                | list  ||
| isFakeStation             | bool  | False                |


### `connectionResponse`

| Name                      | Type | Example                           |
|---------------------------|------|-----------------------------------|
| iata                      | str  | FKB                               |
| operationStartDate        | str  | 2022-07-10T13:25:00               |
| rescueEndDate             | str  | 2022-07-08T10:37:52.7788291+01:00 |
| isDomestic                | bool | False                             |
| isNew                     | bool | True                              |

---

### Schedule

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




