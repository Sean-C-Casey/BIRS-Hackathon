from API import fetch_div_legislators
from API import fetch_div_legislation


class Legislators:
    data = None

    @staticmethod
    def fetch_data(params={}):
        Legislators.data = fetch_div_legislators(params)
        
class Legislation:
    data = None
    
    @staticmethod
    def fetch_data(params={}):
        Legislation.data = fetch_div_legislation(params)