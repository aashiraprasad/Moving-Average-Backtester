import pandas as pd
from data import get_stock_data, get_currency_symbol
from strategy import clean_data,generate_signals_EWMA, generate_signals_SMA
from backtest import run_backtest, summary_stats, agreements
from plotting import plot_price_chart, plot_equity_chart

def run_pipeline(ticker):
    stock_data = get_stock_data(ticker)
    currency_symbol = get_currency_symbol(ticker)
    stock_data = clean_data(stock_data, ticker)
    stock_data = generate_signals_EWMA(stock_data)
    stock_data = generate_signals_SMA(stock_data)
    stock_data = run_backtest(stock_data, 'yPosition_EWMA', 'EWMA')
    stock_data = run_backtest(stock_data, 'yPosition_SMA', 'SMA')
    
    results=[]
    for suffix in ['EWMA', 'SMA']:
        result=summary_stats(stock_data, suffix)
        result['Ticker']=ticker
        result['Strategy']=suffix
        results.append(result)
    return results, stock_data, currency_symbol

def main():
    tickers = ['AAPL', 'BRBY.L', 'TSLA', 'MSFT', 'GOOGL', 'RL', ]  
    all_results = []
    all_stock_data = {}
    for ticker in tickers:
        print(f"\nRunning backtest for {ticker}...")
        try:
            results, stock_data, currency_symbol = run_pipeline(ticker)
            all_results.extend(results)
            all_stock_data[ticker] = (stock_data, currency_symbol)
        except Exception as e:
            print(f"  Skipped {ticker} due to error: {e}")

    comparison_df = pd.DataFrame(all_results)
    comparison_df = comparison_df[['Ticker', 'Strategy', 'Final Equity Curve',
                                     'Total Buy and Hold return', 'Number of trades',
                                     'Max Drawdown', 'Sharpe', 'Annualized Return']]

    print("\n=== Multi-Ticker Comparison ===")
    print(comparison_df.to_string(index=False))
    print("\n=== Sorted by Number of Trades ===")
    print(comparison_df[['Ticker', 'Strategy', 'Number of trades', 'Final Equity Curve']].sort_values('Number of trades').to_string(index=False))

    for ticker, (stock_data, currency_symbol) in all_stock_data.items():
        for suffix in ['EWMA', 'SMA']:
            plot_price_chart(stock_data, ticker, suffix, currency_symbol)
        plot_equity_chart(stock_data, currency_symbol, ticker)

main()
# Ad-hoc investigation: how often do EWMA and SMA agree on position?
# (see README for what this revealed)
_, stock_data, _ = run_pipeline('AAPL')
agreements(stock_data)
_, stock_data, _ = run_pipeline('MSFT')
agreements(stock_data)
