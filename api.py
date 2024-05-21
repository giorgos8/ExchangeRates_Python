import json
from database import SqlServer_ExchRates
from req import Req
import database
import pyodbc
from datetime import datetime, timedelta
import sys
import os
import logging

# configuration log file
logging.basicConfig(filename='exchange_rates_logs.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# global environmental variables
api_id = os.environ.get("exchange_rates_api_id")
coins = os.environ.get("exchange_rates_currency")
endpoint = os.environ.get("exchange_rates_endpoint")
conn_string = os.environ.get("exchange_rates_conn_string")


# function that return the connection string
def get_connection_string():
  return conn_string

def main():    
    
    # crate api call object
    try:
        req = Req(endpoint)
    except:
        raise Exception("Error on creation api object!")
    
    # db connection
    try:
        sink = SqlServer_ExchRates(get_connection_string())
    except:
        raise Exception("Error connecting to db!")
    
    logging.debug('Connect to db succssesfully!')
    
    # get next aa for db table logs
    next_run_aa = 0
    next_run_aa = sink.get_next_aa()
    
    print('AA: ' + str(next_run_aa))
    logging.debug('for db logs, next run aa: ' + str(next_run_aa))
    sink.write_db_trace('START', 'INFO', next_run_aa)
    
    if next_run_aa <= 0:
        sink.write_db_trace('next_run_aa <= 0', 'ERROR', next_run_aa)
        raise Exception("next_run_aa <= 0")
    
    
    # date argument by default is the current data
    date_from = datetime.now().date()
    
    # check for valid currency and authentication id
    if coins is None or api_id is None:
        sink.write_db_trace('cannot read the global variables', 'ERROR', next_run_aa)
        raise Exception("can not read the global variables, coins, api_id")
        
    logging.debug('Read global variables')
    
    # check the user inputs
    # no input: run the current date
    # two input arguments: start_date end_date (for backfilling or re-import some dates)
    # otherwise exception...
    
    if len(sys.argv) == 1:
        date_to = date_from
    elif len(sys.argv) == 3:
        print('with parameters')
        date_from = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        date_to = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
    else:
        sink.write_db_trace('Something goes wrong with the parameters', 'ERROR', next_run_aa)
        raise Exception('Something goes wrong with the parameters')
    
    delta = timedelta(days=1)
    
    # iterate over range of dates
    while (date_from <= date_to):
        print(date_from, end="\n")        
        exchange_date = date_from
        exchange_rates, rate = req.get_exchange_rates_hst(exchange_date, coins, api_id)
        sink.insert_exchange_rates(exchange_rates, coins, exchange_date)        
        print('Exchange Rate USD to ' + coins + ': ' + str(rate))
        date_from += delta        
        
    sink.write_db_trace('END', 'INFO', next_run_aa)    
    
    
if __name__ == '__main__':
    try:
        print('======= START PROGRAM =========')
        logging.debug('=== New Call ===')
        main()
        print('======= END PROGRAM WITH SUCCESS =========')
    except Exception as e:
        print('======= END PROGRAM WITH ERROR =========')
        logging.error('@@@ Error @@@: ' + str(e))        
        raise e




  

