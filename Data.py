from API import fetch_div_legislators


class Legislators:
    data = None

    @staticmethod
    def fetch_data(params={}):
        Legislators.data = fetch_div_legislators(params)