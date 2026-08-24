from matplotlib import pyplot as plt
def plot_price_chart(stock_data, ticker, suffix, currency_symbol):
    plt.figure(figsize=(14,7))
    plt.plot(stock_data[('Date', '')], stock_data['Close'], label='Close')
    if suffix == 'EWMA':
        ma_short, ma_long = 'EMA20', 'EMA50'
    else:
        ma_short, ma_long = 'SMA20', 'SMA50'

    plt.plot(stock_data[('Date','')], stock_data[ma_short], label=f'{suffix}20')
    plt.plot(stock_data[('Date','')], stock_data[ma_long], label=f'{suffix}50')
    
    buys= stock_data[stock_data[f'Signal_{suffix}']==1]
    sells= stock_data[stock_data[f'Signal_{suffix}']==-1]
    plt.scatter(buys[('Date', '')], buys['Close'], marker='^', color='g', label='Buy', s=120, edgecolors='black', zorder=5)
    plt.scatter(sells[('Date', '')], sells['Close'], marker='v', color='r', label='Sell', s=120, edgecolors='black', zorder=5)
    plt.xlabel('Date')
    plt.ylabel(f'Price ({currency_symbol})')
    plt.title(f'{ticker}- {suffix} Crossover Strategy')
    plt.legend()
    plt.grid(True)

def plot_equity_chart(stock_data, currency_symbol, ticker):
    plt.figure(figsize=(14,7))
    plt.plot(stock_data[('Date','')], stock_data['Equity Curve EWMA'], label='EWMA Strategy')
    plt.plot(stock_data[('Date','')], stock_data['Equity Curve SMA'], label='SMA Strategy')
    plt.plot(stock_data[('Date','')], stock_data['Comparison'], label='Buy and Hold')
    plt.xlabel('Date')
    plt.ylabel(f'Growth of 1{currency_symbol}')
    plt.title(f'{ticker} Strategy Comparison: EWMA vs SMA vs Buy and Hold')
    plt.axhline(y=1, color='b', linestyle='--', label='Break-even')
    plt.legend()
    plt.grid(True)
    plt.show()