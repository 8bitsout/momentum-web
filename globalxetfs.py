from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import List

Response = requests.models.Response


class ETF:
    def __init__(self, ticker: str, url: str, name: str):
        self.ticker = ticker
        self.url = url
        self.name = name
        self.holdings = None

    def get_holdings(self):
        data = pd.read_csv(
            self.url + "?download_full_holdings=true",
            sep=',',
            skiprows=2,
            header=0
        ).dropna()
        data["Ticker"] = data["Ticker"].apply(lambda x: x.split(' ')[0])
        self.holdings = data
        return data


class GlobalXEtfs:
    etfs: List[ETF] = []
    url: str = "https://www.globalxetfs.com/"
    etfs_map = {}

    def get_etfs(self):
        page: Response = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links: list = soup.find_all("a", attrs={"data-ticker": True, "href": True})

        for link in links:
            ticker: str = link.get('data-ticker')
            url: str = link.get('href')
            name: str = link.get_text()
            etf: ETF = ETF(ticker, url, name)
            self.etfs_map[ticker] = etf
            self.etfs.append(etf)
