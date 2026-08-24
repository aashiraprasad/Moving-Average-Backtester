import pandas as pd
def clean_data(stock_data, ticker):
    stock_data=stock_data.dropna()
    stock_data=stock_data.reset_index()
    stock_data.columns=stock_data.columns.to_flat_index()
    stock_data = stock_data.rename(columns={('Close', ticker): 'Close'})
    return stock_data

def generate_signals_EWMA(stock_data):
    stock_data['EMA20']=stock_data['Close'].ewm(span=20, adjust=False).mean()
    stock_data['EMA50']=stock_data['Close'].ewm(span=50, adjust=False).mean()
    stock_data['yEMA20']=stock_data['EMA20'].shift(1)
    stock_data['yEMA50']=stock_data['EMA50'].shift(1)

    buy_condition = (stock_data['yEMA20'] < stock_data['yEMA50']) & (stock_data['EMA20'] > stock_data['EMA50'])
    sell_condition = (stock_data['yEMA50'] < stock_data['yEMA20']) & (stock_data['EMA50'] > stock_data['EMA20'])
    stock_data['Signal_EWMA'] = 0
    stock_data.loc[ buy_condition, 'Signal_EWMA'] = 1
    stock_data.loc[ sell_condition, 'Signal_EWMA'] = -1

    stock_data['Position_EWMA'] = stock_data['Signal_EWMA'].replace(0, float('nan')).ffill().fillna(0)
    stock_data['yPosition_EWMA']=stock_data['Position_EWMA'].shift(1)
    return stock_data

def generate_signals_SMA(stock_data):
    stock_data['SMA20']=stock_data['Close'].rolling(20).mean()
    stock_data['SMA50']=stock_data['Close'].rolling(50).mean()
    stock_data['ySMA20']=stock_data['SMA20'].shift(1)
    stock_data['ySMA50']=stock_data['SMA50'].shift(1)

    buy_condition = (stock_data['ySMA20'] < stock_data['ySMA50']) & (stock_data['SMA20'] > stock_data['SMA50'])
    sell_condition = (stock_data['ySMA50'] < stock_data['ySMA20']) & (stock_data['SMA50'] > stock_data['SMA20'])
    stock_data['Signal_SMA'] = 0
    stock_data.loc[ buy_condition, 'Signal_SMA'] = 1
    stock_data.loc[ sell_condition, 'Signal_SMA'] = -1

    stock_data['Position_SMA'] = stock_data['Signal_SMA'].replace(0, float('nan')).ffill().fillna(0)
    stock_data['yPosition_SMA']=stock_data['Position_SMA'].shift(1)
    return stock_data
