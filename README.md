# What this project does
REST API that reads exchange rates from openexchangerates.org and stores price information for given currency in database.

#Available endpoints:

#/exchange_operations/add

When this endpoint is called, then the latest forex prices are fetched from OpenExchangeRates API.
The price for given currency is multiplied by the amount passed in the POST request.
Following fields are stored in MySQL:

 - currency
 - amount requested,
 - exchange_price,
 - final_amount in USD,
 - date when price was published

Method: POST
Params:
 - currency_code - should be ISO3 code, for example EUR, USD, BTC etc
 - amount - this the amount that will be used to multiply price with this amount provided, for example: 1.5

Example how to use:

    curl http://0.0.0.0:5000/exchange_operations/add -d "currency_code=PLN&amount=1.5" -X POST
    
Output:

    {"id": 1, "currency": "PLN", "amount_requested": "1.50000000", "exchange_price": "3.79766101", "final_amount": "5.69649152", "date": "2020-10-09 10:00:00"}
    

#/exchange_operations/last/  

This endpoint will return the last operation stored in MySQL

* If currency is passed in url then it will return the last record for that specific currency from the MySQL DB.
* If operations_count is passed in url then it will return the last number of operations.
* If both currency and operations_count is passed then it will return the last number of operations for that currency.

Method: GET
URL params - currency and operations_count

Example how to use:

    curl http://0.0.0.0:5000/exchange_operations/last -X GET
    
Output:

    [
      {
        "id": 1,
        "currency": "AUD",
        "amount_requested": "1.50000000",
        "exchange_price": "1.39137201",
        "final_amount": "2.08705802",
        "date": "2020-10-09 10:00:00"
      }
    ]

This example returns last 3 operations:

    curl http://0.0.0.0:5000/exchange_operations/last/3 -X GET
    
    [
      {
        "id": 2,
        "currency": "EUR",
        "amount_requested": "1.50000000",
        "exchange_price": "0.84725201",
        "final_amount": "1.27087802",
        "date": "2020-10-09 11:00:00"
      },
      {
        "id": 3,
        "currency": "PLN",
        "amount_requested": "1.50000000",
        "exchange_price": "3.79118201",
        "final_amount": "5.68677302",
        "date": "2020-10-09 11:00:00"
      },
      {
        "id": 1,
        "currency": "AUD",
        "amount_requested": "1.50000000",
        "exchange_price": "1.39137201",
        "final_amount": "2.08705802",
        "date": "2020-10-09 10:00:00"
      }
    ]

This example will return last two operations for AUD currency

    curl http://0.0.0.0:5000/exchange_operations/last/AUD/2 -X GET

    [
      {
        "id": 4,
        "currency": "AUD",
        "amount_requested": "1.50000000",
        "exchange_price": "1.39100400",
        "final_amount": "2.08650600",
        "date": "2020-10-09 11:00:00"
      },
      {
        "id": 1,
        "currency": "AUD",
        "amount_requested": "1.50000000",
        "exchange_price": "1.39137201",
        "final_amount": "2.08705802",
        "date": "2020-10-09 10:00:00"
      }
    ]


# How to run dev server 

    docker-compose up --build
    
# Frontend 

Frontend runs on http://0.0.0.0:3000/    
    
# How to run tests

    docker-compose up -d --build && docker-compose exec api flask test
    
# Deploy to production

Code was deployed to 

http://intense-refuge-82371.herokuapp.com/     

    curl http://intense-refuge-82371.herokuapp.com/exchange_operations/add -d "currency_code=PLN&amount=1.5" -X POST
    {"id": 21, "currency": "PLN", "amount_requested": "1.50000000", "exchange_price": "3.78240000", "final_amount": "5.67360000", "date": "2020-10-09 14:00:00"}
