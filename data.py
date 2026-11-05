import os, yfinance as yf, pandas as pd

START = '2024-01-01'
END = '2025-12-31'
CACHE_DIR = os.path.join('data', 'cache')
def cache_path(ticker, start, end):
    return os.path.join(CACHE_DIR, f'{ticker}_{start}_{end}.csv')
def get_stock_data(ticker, start=START, end=END, refresh=False):
    # Read from the on-disk cache when possible: it keeps runs fast, avoids Yahoo
    # rate limits, and makes the backtest offline-reproducible. Pass refresh=True
    # to re-download.
    path = cache_path(ticker, start, end)
    if os.path.exists(path) and not refresh:
        data = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True)
        data.index.name = 'Date'
        return data
    data = yf.download(ticker, start=start, end=end)
    os.makedirs(CACHE_DIR, exist_ok=True)
    data.to_csv(path)
    return data

def get_currency_symbol(ticker):
    info=yf.Ticker(ticker).info
    currency=info.get('currency','USD')
    symbols = {'USD': '$', 'GBP': '£', 'GBp': 'p', 'EUR': '€'}
    return symbols.get(currency, currency + ' ')