import requests
import json

class Req(object):
    
    def __init__(self, url):
        self.url = url
        self.sess = requests.Session()        
        self.headers = {"accept": "application/json"}
        
    def get_exchange_rates_hst(self,exchange_date, coins, api_id):
        url = f"{self.url}/historical/{exchange_date}.json?app_id={api_id}&symbols={coins}&show_alternative=false&prettyprint=true"
        headers = self.headers #{"accept": "application/json"}
        response = requests.get(url, headers=headers)
        exc_rts = json.loads(response.content)
        return exc_rts, exc_rts['rates'][coins]
