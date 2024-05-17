import requests
import json
from database import SqlServer
import database
import pyodbc
from datetime import datetime, timedelta
import sys
import os
import logging

logging.basicConfig(filename='exchange_rates.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def get_connection_string():
  return os.environ.get("exchange_rates_conn_string") #f'Driver=SQL Server Native Client 11.0;Server=.;Database=EXCHANGE_RATES_DB;Trusted_Connection=yes'


def get_exchange_rates(exchange_date, coins, api_id): #coins seperated with comma e.g. EUR,USD
  url = f"https://openexchangerates.org/api/historical/{exchange_date}.json?app_id={api_id}&symbols={coins}&show_alternative=false&prettyprint=true"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers)
  #print(response.text)
  exc_rts = json.loads(response.content)
  return exc_rts, exc_rts['rates'][coins]


def main():
    conn_string = get_connection_string()
    sink = SqlServer(conn_string)
        
    print('======= START THE PROGRAM =========')
    logging.debug('======= START PROGRAM =========')
    
    #print(sink.get_exchange_rate_from_db('2024-05-13', 'EUR'))
    
    next_run_aa = 0
    next_run_aa = sink.get_next_aa()
    
    print('next_run_aa: ' + str(next_run_aa))
    logging.debug('next_run_aa: ' + str(next_run_aa))
    sink.write_db_trace('START', 'INFO', next_run_aa)
    
    if next_run_aa <= 0:
        sink.write_db_trace('next_run_aa <= 0', 'ERROR', next_run_aa)
        raise Exception("next_run_aa <= 0")
    
    
    # date parameters
    date_from = datetime.now().date()
    
    api_id = os.environ.get("exchange_rates_api_id")
    coins = os.environ.get("exchange_rates_currency")
    
    if coins is None or api_id is None:
        #cursor.execute(f"exec [dbo].[usp_write_trace] @INPUTMESSAGE=?, @INFO=?, @RUNID=?", 'print("Cannot read the global variables")', 'ERROR', next_run_aa)
        #cnxn.commit() 
        sink.write_db_trace('cannot read the global variables', 'ERROR', next_run_aa)
        raise Exception("can not read the global variables")
        
    logging.debug('Read global variables')
    
    #unit test
    #exch_rts = get_exchange_rates('2024-05-01', 'EUR', api_id)
    #print('2024-05-01 => Exchange Rate USD to ' + coins + ': ' + str(get_exchange_rate_value(get_exchange_rates('2024-05-01', 'EUR', api_id), 'EUR', '2024-05-01'))) #for unit test
    
    
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
        exchange_rates, rate = get_exchange_rates(exchange_date, coins, api_id)
        sink.insert_exchange_rates(exchange_rates, coins, exchange_date)        
        date_from += delta
        print('Exchange Rate USD to ' + coins + ': ' + str(rate))
        
    sink.write_db_trace('END', 'INFO', next_run_aa)
    print('======= END PROGRAM =========')
    
    
if __name__ == '__main__':
    try:
        logging.debug('=== New Call ===')
        main()
    except Exception as e:
        logging.error('@@@ Error @@@: ' + str(e))
        raise e




  

