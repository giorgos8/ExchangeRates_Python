# Exchange Rates

The target is to call the API https://docs.openexchangerates.org/reference/api-introduction with Exchange Rates daily and input the data into a SQL Server Database table

## Description

1. Using OOP (Python): https://github.com/giorgos8/ExchangeRates_Python we extract data from a web source (Open Exchange Rates), transforms the dataset (convert from USD base to EUR) and loads it into a database (ETL).
2. Using RDBMS (SQL Server 2019): https://github.com/giorgos8/ExchangeRates_DB the extracted data is loadind daily into a table. Then we create views-reports about the data and statistics.
3. Using C# (.NET): https://github.com/giorgos8/ExchangeRates_C_Sharp a simple user can use a simle Windows Application to admin, watch and run (re-run) the API

### Local Setup

* SQL Server with Version >= 2017
* Python 3.11

### Configuration - modifications needed

```
#global environmental variables
api_id = os.environ.get("exchange_rates_api_id")
coins = os.environ.get("exchange_rates_currency")
endpoint = os.environ.get("exchange_rates_endpoint")
conn_string = os.environ.get("exchange_rates_conn_string")
```

### Executing

* The default CLI command haven't any argument and import just the current date.
```
python api.py
```
* The CLI command must also accept two arguments start_date and end_date in case we need to do a backfilling or re-import some dates in case an issue arised.
```
python api.py 2024-01-01 2024-01-31
```
* To run Unit & Integration tests
```
python -m pytest -v
```

## Help for Testing

Use Postman to call ad-hoq the API

## Authors

Giorgos Kokkinos
giorgos.kokkinos@gmail.com

## Version History

* 0.1
    * Initial Release

