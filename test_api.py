import unittest
import api
import database
import os

api_id = os.environ.get("exchange_rates_api_id")
coins = os.environ.get("exchange_rates_currency")

class TestClass(unittest.TestCase):

    def test_get_exchange_rates_May(self):
    
        lst, rate = api.get_exchange_rates('2024-05-01', 'EUR', api_id)
        self.assertEqual(rate, 0.933021)
        
        lst, rate = api.get_exchange_rates('2024-05-02', 'EUR', api_id)
        self.assertEqual(rate, 0.931923)
        
    def test_get_exchange_rates_Jan(self):
    
        lst, rate = api.get_exchange_rates('2024-01-01', 'EUR', api_id)
        self.assertEqual(rate, 0.933021)
    
    
if __name__ == '__main__':
    unittest.main()