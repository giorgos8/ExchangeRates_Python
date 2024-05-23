import unittest
import api
import database
import os
from req import Req
from database import SqlServer_ExchRates

#python -m pytest -v

api_id = os.environ.get("exchange_rates_api_id")
coins = os.environ.get("exchange_rates_currency")
endpoint = os.environ.get("exchange_rates_endpoint")


#######################
# U N I T   T E S T S #
#######################


class TestClass(unittest.TestCase):

    def test_get_api_rate_Jan(self):
        req = Req(endpoint)
        lst, rate = req.get_exchange_rates_hst('2024-01-01', 'EUR', api_id)
        self.assertEqual(rate, 0.906074)
    
    def test_get_api_rate_May(self):
        req = Req(endpoint)
        lst, rate = req.get_exchange_rates_hst('2024-05-01', 'EUR', api_id)
        self.assertEqual(rate, 0.933021)
        
        lst, rate = req.get_exchange_rates_hst('2024-05-02', 'EUR', api_id)
        self.assertEqual(rate, 0.931923)
        
    def test_get_db_rate_Jan(self):
        sink = SqlServer_ExchRates(os.environ.get("exchange_rates_conn_string"))
        rate = sink.get_exchange_rate_from_db('2024-01-01', 'EUR')        
        self.assertEqual(rate, 0.906074)
        
    
    
    
if __name__ == '__main__':
    unittest.main()