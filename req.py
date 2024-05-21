import requests
import json

class Req(object):
    
    def __init__(self, url):
        self.url = url
        self.headers = {"accept": "application/json"}
        
    def get_exchange_rates_hst(self,exchange_date,coins,api_id):
        prms = {}
        prms['symbols'] = coins
        prms['show_alternative'] = False
        prms['prettyprint'] = True
        base_url = f"{self.url}/historical/{exchange_date}.json?app_id={api_id}"
        headers = self.headers
        response = requests.get(base_url, params = prms, headers=headers)
        print(response.status_code)
        #print(response.url)
        exc_rts = json.loads(response.content)
        #print(response.text[:200])        
        return exc_rts, exc_rts['rates'][coins]