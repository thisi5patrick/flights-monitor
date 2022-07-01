| Method | URL                                                                                 |
|--------|-------------------------------------------------------------------------------------|
| POST   | https://api-production-aerok-booksecure.ezyflight.se/api/v1/Availability/SearchShop | 

### Request Headers
| Required | Parameter         | type | Example                                                          |
|----------|-------------------|------|------------------------------------------------------------------|
| True     | Tenant-Identifier | str  | G735CZwKYQqb7DlVTFYuc7TUXD3NMlhIdWMe49ZQ2nhhefLG0IdwXp6TcXKqL01x |



### Request Params

| Required | Parameter  | type | Example           |
|----------|------------|------|-------------------|
| True     | routes     | list | `routesParam`     |
| True     | passengers | list | `passengersParam` |
| True     | currency   | str  | KRW               |


### routesParam

| Required | Parameter   | type | Example    |
|----------|-------------|------|------------|
| True     | startDate   | str  | 2022-07-01 |
| True     | endDate     | str  | 2022-09-01 |
| True     | fromAirport | str  | CJU        |
| True     | toAirport   | str  | CJJ        |

### passengersParam

| Required | Parameter | type | Example |
|----------|-----------|------|---------|
| True     | code      | str  | ADT     |
| True     | count     | int  | 1       |




### Response

| Name    | Type | Example          |
|---------|------|------------------|
| routes  | list | `routesResponse` |

#### routesResponse

| Name    | Type   | Example           |
|---------|--------|-------------------|
| from    | object | `fromResponse`    |
| to      | object | `toResponse`      |
| flights | list   | `flightsResponse` |


#### fromResponse

| Name        | Type | Example                                                                           |
|-------------|------|-----------------------------------------------------------------------------------|
| connections | list | [{'name': 'Cheongju 청주', 'code': 'CJJ', 'currency': 'KRW', 'countryCode': 'KOR'}] |
| name        | str  | Jeju 제주                                                                           |
| code        | str  | CJU                                                                               |
| currency    | str  | KRW                                                                               |
| countryCode | str  | KOR                                                                               |

#### toResponse

| Name        | Type | Example     |
|-------------|------|-------------|
| name        | str  | Cheongju 청주 |
| code        | str  | CJJ         |
| currency    | str  | KRW         |
| countryCode | str  | KOR         |

#### flightsResponse

| Name                           | Type  | Example                   |
|--------------------------------|-------|---------------------------|
| carrierCode                    | str   | RF                        |
| flightNumber                   | str   | 614                       |
| arrivalDate                    | str   | 2022-07-01T22:00:00       |
| lowestFareId                   | int   | 5                         |
| cabin                          | str   | ECONOMY                   |
| lowestPriceTotal               | float | 58800.0                   |
| lowestPriceDiscount            | float | 0.0                       |
| fares                          | list  |                           |
| allFares                       | list  |                           |
| fareTypes                      | list  |                           |
| legs                           | list  |                           |
| key                            | str   | 40983:7/1/2022 8:45:00 PM |
| lowestPriceWithoutTax          | int   | 75                        |
| soldOut                        | bool  | False                     |
| soldout                        | bool  | False                     |
| isInternational                | bool  | False                     |
| isPlaceHolder                  | bool  | False                     |
| lowestPriceSinglePax           | float | 58800.0                   |       
| lowestPriceSinglePaxWithoutTax | float | 35000.0                   |   
| appliedPromotion               | str   | None                      |
| id                             | int   | 40983                     |



