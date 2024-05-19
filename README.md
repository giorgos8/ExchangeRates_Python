# Project Title

Exchange Rates

## Description

The target is to call an API with Exchange Rates daily and input the data into a SQL Server Database table

## Getting Started

### Local Setup

* SQL Server with Vesrion >= 2017
* Python 3.11

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

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

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

ex. Giorgos Kokkinos
ex. giorgos.kokkinos@gmail.com

## Version History

* 0.1
    * Initial Release

