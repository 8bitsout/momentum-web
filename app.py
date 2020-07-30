from Nasdaqomx import Nasdaqomx
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask
from typing import NamedTuple, List

app = Flask(__name__)


@app.route('/api/momentum/tickers/<index>')
def momentum_tickers(index: list):
    top, bottom = fetch_momentum_stocks(index)
    print(top)
    return {"best": top, "worst": bottom}


def fetch_momentum_stocks(index, start_date=datetime.today(), lookback_period=6):
    def get_my_key(obj):
        return obj['return']

    ndx = Nasdaqomx()
    tickers = ndx.fetchTickers(index)
    end_date = start_date - relativedelta(months=lookback_period)
    stocks = yf.download(tickers, end_date, start_date)

    stock_returns = []

    for stock in stocks['Adj Close']:
        s = stocks['Adj Close'][stock]
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
