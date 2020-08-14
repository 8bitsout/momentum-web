from Nasdaqomx import Nasdaqomx
from globalxetfs import GlobalXEtfs
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask
from typing import NamedTuple, List

app = Flask(__name__)
gxe = GlobalXEtfs()
gxe.get_etfs()


@app.route('/api/momentum/nasdaqomx/tickers/<index>')
def momentum_tickers(index):
    ndx = Nasdaqomx()
    tickers = ndx.fetchTickers(index)
    top, bottom = fetch_momentum_stocks(tickers)
    print(top)
    return {"best": top, "worst": bottom}


@app.route('/api/momentum/globalx/tickers/<index>')
def globalx_momentum_tickers(index):
    print(index)
    holdings = gxe.etfs_map[index].get_holdings()
    print(holdings)
    tickers = holdings["Ticker"].tolist()
    print(tickers)
    top, bottom = fetch_momentum_stocks(tickers)
    print(top)
    return {"best": top, "worst": bottom}


def fetch_momentum_stocks(tickers, start_date=datetime.today(), lookback_period=6):
    def get_my_key(obj):
        return obj['return']

    end_date = start_date - relativedelta(months=lookback_period)
    stocks = yf.download(tickers, end_date, start_date)
    stocks.dropna()
    stock_returns = []
    print(stocks)
    for stock in stocks['Adj Close']:
        s = stocks['Adj Close'][stock].dropna()
        r = ((s[-1] / s[0]) - 1) * 100
        stock_returns.append({'name': s.name, 'return': r})

    stock_returns.sort(key=get_my_key)
    stock_returns.reverse()

    top = stock_returns[:5]
    bottom = stock_returns[-5:]

    return top, bottom


# def fetch_returns_since_inception()

if __name__ == '__main__':
    app.run()
