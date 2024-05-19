import requests
import os
from database import SqlServer
from datetime import datetime

#python -m pytest -v

exchange_date = datetime.now().date()
api_id = os.environ.get("exchange_rates_api_id")
coins = os.environ.get("exchange_rates_currency")
endpoint = os.environ.get("exchange_rates_endpoint")

url = f"{endpoint}/historical/{exchange_date}.json?app_id={api_id}&symbols={coins}&show_alternative=false&prettyprint=true"

#####################################
# I N T E G R A T I O N   T E S T S #
#####################################

def test_can_call_endpoint():
    response = requests.get(url)
    assert response.status_code == 200
    
def test_can_connect_db():    
    sink = SqlServer(os.environ.get("exchange_rates_conn_string"))
    assert sink is not None