import os
import pandas as pd
from data import get_stock_data, get_currency_symbol
from strategy import clean_data,generate_signals_EWMA, generate_signals_SMA, warmup_rows
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
    warmup = warmup_rows(stock_data)
    for suffix in ['EWMA', 'SMA']:
        result=summary_stats(stock_data, suffix, start=warmup)
        result['Ticker']=ticker
        result['Strategy']=suffix
        results.append(result)
    return results, stock_data, currency_symbol

def main(save_plots=True, outdir='outputs'):
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
    comparison_df = comparison_df[['Ticker', 'Strategy', 'Days Measured',
                                     'Annualized Return', 'Sharpe', 'Max Drawdown',
                                     'Buy and Hold Annualized Return', 'Buy and Hold Sharpe',
                                     'Buy and Hold Max Drawdown', 'Total Buy and Hold return',
                                     'Final Equity Curve', 'Number of trades', 'Turnover (units)',
                                     'Total Cost Charged (%)']]

    print("\n=== Multi-Ticker Comparison ===")
    print(comparison_df.to_string(index=False))
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, 'comparison.csv')
    comparison_df.to_csv(csv_path, index=False)
    print(f"\nComparison table written to {csv_path}")

    print("\n=== Sorted by Number of Trades ===")
    print(comparison_df[['Ticker', 'Strategy', 'Number of trades', 'Final Equity Curve']].sort_values('Number of trades').to_string(index=False))

    if save_plots:
        for ticker, (stock_data, currency_symbol) in all_stock_data.items():
            for suffix in ['EWMA', 'SMA']:
                plot_price_chart(stock_data, ticker, suffix, currency_symbol, outdir)
            plot_equity_chart(stock_data, currency_symbol, ticker, outdir)
        print(f"\nCharts written to {outdir}/")

    # Reuse the frames fetched above rather than downloading them a second time.
    for ticker in ('AAPL', 'MSFT'):
        if ticker in all_stock_data:
            print(f"\n=== EWMA vs SMA agreement: {ticker} ===")
            agreements(all_stock_data[ticker][0])

    return comparison_df

if __name__ == "__main__":
    main()