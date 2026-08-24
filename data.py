import yfinance as yf
import datetime

def get_stock_data(ticker):
    data=yf.download(ticker, start='2024-01-01' , end=datetime.date.today())
    return data

def get_currency_symbol(ticker):
    info=yf.Ticker(ticker).info
    currency=info.get('currency','USD')
    symbols = {'USD': '$', 'GBP': '£', 'GBp': 'p', 'EUR': '€'}
    return symbols.get(currency, currency + ' ')