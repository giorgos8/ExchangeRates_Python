# Exchange Rates

The basic target is to call the API https://docs.openexchangerates.org/reference/api-introduction with Exchange Rates daily and input the data into a SQL Server Database table

## Description

1. Using OOP (Python): https://github.com/giorgos8/ExchangeRates_Python we extract data from a web source (Open Exchange Rates), transforms the dataset (convert from USD base to EUR) and loads it into a database (ETL).
2. Using RDBMS (SQL Server 2019): https://github.com/giorgos8/ExchangeRates_DB the extracted data is loadind daily into a table. Then we create views-reports about the data and statistics.
3. Using C# (.NET): https://github.com/giorgos8/ExchangeRates_C_Sharp a simple user can use a simle Windows Application to admin, watch and run (re-run) the API

### Local Setup

* SQL Server with Version >= 2017
* Python 3.11
* Windows OS, .NET Framework

### Configuration - Modifications needed

```
Global Environmental Variables 
os.environ.get("exchange_rates_api_id") e.g. 51484b1ac5314ea894bf33038f24515d
os.environ.get("exchange_rates_currency") e.g. EUR
os.environ.get("exchange_rates_endpoint") e.g. https://openexchangerates.org/api
os.environ.get("exchange_rates_conn_string") e.g. Driver=SQL Server Native Client 11.0;Server=.;Database=EXCHANGE_RATES_DB;Trusted_Connection=yes
exchange_rates_python_exe_path e.g. C:\GIORGOS\Pythons\Python311\Python.exe
exchange_rates_python_script_path: e.g. C:\GIORGOS\ExchangeRates\ExchangeRates_Python\api.py
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

