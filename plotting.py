from matplotlib import pyplot as plt
import os
def _save(fig, outdir, filename):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, filename)
    fig.savefig(path, dpi=130, bbox_inches='tight')
    plt.close(fig)
    return path
def plot_price_chart(stock_data, ticker, suffix, currency_symbol, outdir='outputs'):
    if suffix == 'EWMA':
        ma_short, ma_long = 'EMA20', 'EMA50'
    else:
        ma_short, ma_long = 'SMA20', 'SMA50'

    fig, ax = plt.subplots(figsize=(14,7))
    ax.plot(stock_data[('Date', '')], stock_data['Close'], label='Close')
    ax.plot(stock_data[('Date','')], stock_data[ma_short], label=f'{suffix}20')
    ax.plot(stock_data[('Date','')], stock_data[ma_long], label=f'{suffix}50')

    
    buys= stock_data[stock_data[f'Signal_{suffix}']==1]
    sells= stock_data[stock_data[f'Signal_{suffix}']==-1]
    ax.scatter(buys[('Date', '')], buys['Close'], marker='^', color='g', label='Buy', s=120, edgecolors='black', zorder=5)
    ax.scatter(sells[('Date', '')], sells['Close'], marker='v', color='r', label='Sell', s=120, edgecolors='black', zorder=5)
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Price ({currency_symbol})')
    ax.set_title(f'{ticker} - {suffix} Crossover Strategy')
    ax.legend()
    ax.grid(True)
    return _save(fig, outdir, f'{ticker}_{suffix}_price.png')

def plot_equity_chart(stock_data, currency_symbol, ticker, outdir='outputs'):
    fig, ax = plt.subplots(figsize=(14,7))
    ax.plot(stock_data[('Date','')], stock_data['Equity Curve EWMA'], label='EWMA Strategy')
    ax.plot(stock_data[('Date','')], stock_data['Equity Curve SMA'], label='SMA Strategy')
    ax.plot(stock_data[('Date','')], stock_data['Comparison'], label='Buy and Hold')
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Growth of 1{currency_symbol}')
    ax.set_title(f'{ticker} Strategy Comparison: EWMA vs SMA vs Buy and Hold')
    ax.axhline(y=1, color='b', linestyle='--', label='Break-even')
    ax.legend()
    ax.grid(True)
    return _save(fig, outdir, f'{ticker}_equity.png')