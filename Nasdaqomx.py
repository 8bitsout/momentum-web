import requests
from datetime import datetime


class Nasdaqomx:
    URL = 'https://indexes.nasdaqomx.com/Index/WeightingData'
    indexes = {}

    def fetchTickers(self, index, time_of_day='SOD'):
        tickers = []

        r = requests.post(self.URL, data={
            "id": index,
            "tradeDate": datetime.now().isoformat(),
            "timeOfDay": time_of_day
        })

        data = r.json()
        companies = data['aaData']

        for company in companies:
            tickers.append(company["Symbol"])

        self.indexes[index] = tickers

        return tickers
