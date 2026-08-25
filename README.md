# Moving Average Crossover Backtester

A Python backtesting framework that compares two moving-average crossover strategies — **EMA(20,50)** and **SMA(20,50)** — against a buy-and-hold baseline, across multiple tickers, with risk-adjusted performance metrics and transaction cost modeling.

## What it does

For a given stock ticker, the tool:

1. Downloads historical daily price data (via `yfinance`)
2. Generates buy/sell signals from both an EMA and an SMA crossover strategy (fast MA crossing above/below a slow MA)
3. Backtests each strategy without lookahead bias (positions are lagged by one day — you can only trade on yesterday's signal, not today's)
4. Applies a 0.1% per-trade transaction cost to simulate realistic trading friction
5. Computes summary statistics: total return, buy-and-hold comparison, number of trades, max drawdown, Sharpe ratio, and annualized return
6. Runs the same analysis across a list of tickers and builds a single comparison table
7. Plots price charts (with buy/sell markers) and equity curves for visual inspection

## Project structure

| File | Responsibility |
|---|---|
| `data.py` | Fetches price data and currency metadata from Yahoo Finance |
| `strategy.py` | Cleans raw data and generates EMA/SMA crossover signals |
| `backtest.py` | Runs the backtest, applies transaction costs, computes summary stats |
| `plotting.py` | Renders price and equity curve charts |
| `main.py` | Orchestrates the pipeline across one or many tickers |

## Running it

```bash
python3 main.py
```

By default, `main()` runs the full pipeline across a fixed list of tickers (edit the `tickers` list in `main.py` to change them) and prints a comparison table. Plotting for individual tickers can be enabled by uncommenting the relevant calls in `run_pipeline`.

## Methodology notes

- **No lookahead bias**: strategies trade on `yPosition_{suffix}`, the *previous* day's position — not the current day's, since you can't act on a signal before it exists.
- **Transaction costs**: a flat 0.1% cost is deducted from daily strategy returns on any day a trade (buy or sell) occurs, applied before the equity curve is computed so it compounds realistically.
- **Sharpe ratio**: computed from daily strategy returns, annualized by `√252` (standard trading-days-per-year convention), using a risk-free rate of 0.
- **Annualized return**: computed as `(final_equity ** (252/n)) - 1`, where `n` is the count of valid (non-NaN) trading days for that strategy — not total row count, to avoid diluting the figure with the MA warm-up period.
- **Currency handling**: price/equity labels dynamically pull the correct currency symbol per ticker (e.g. GBp for LSE-listed stocks, $ for US stocks) rather than assuming one currency.

## Findings

**EWMA and SMA converge more than expected, and the reason is mechanical, not coincidental.** Across all six tested tickers (AAPL, BRBY.L, TSLA, MSFT, GOOGL, RL), the EWMA and SMA strategies held the *same* market position (long/flat/short) on 77–92% of days, depending on the ticker. Investigating why: disagreement days cluster in short bursts right after each crossover event, not as sustained divergence. This is a direct consequence of the formulas themselves — EMA always weights the most recent price most heavily, so it reacts to a price move a few days before SMA (which weights all 20/50 days equally) catches up. The two strategies aren't fundamentally different signals; they're the same signal with slightly different timing.

**There is no consistent winner between EWMA and SMA across tickers.** EWMA had a higher Sharpe ratio on 4 of 6 tickers, but SMA's occasional wins (notably BRBY.L, GOOGL) were sometimes larger in magnitude than EWMA's typical wins. The honest conclusion is a mild edge for EWMA on average, not a reliable one — performance is substantially ticker-dependent.

**Transaction costs matter more for high-frequency strategies, but don't explain everything.** Adding a realistic 0.1% per-trade cost degraded Sharpe ratios by roughly 2–4x more for high-trade-count strategies (16–17 trades) than for low-trade-count strategies (8 trades), confirming that trade frequency is a real, partial driver of underperformance. However, cost alone doesn't explain the full picture: strategies with *identical* trade counts still produced wildly different outcomes (e.g. GOOGL EWMA: +67.9% vs. RL EWMA: -25.7%, both at 11 trades), meaning the underlying price trajectory of each stock — trending vs. choppy — is a bigger factor than trade count or transaction cost alone.

## Known limitations

- Single fixed cost rate (0.1%) applied uniformly; real-world costs vary by broker, order size, and liquidity.
- No slippage modeling for larger trade sizes.
- No statistical significance testing on the Sharpe differences between strategies (small trade counts, especially at 8–13 trades, mean results could plausibly be noise rather than signal).
- No out-of-sample/walk-forward validation — all results are in-sample over the same fixed date range.
- Backtest currently covers a single date range (2024-01-01 to present) rather than testing performance across multiple, non-overlapping historical periods.

## Possible next steps

- Walk-forward validation (fit crossover parameters on one period, test on a later untouched period)
- Parameter sensitivity analysis across different (fast, slow) window pairs, not just (20, 50)
- Statistical significance testing on Sharpe ratio differences (e.g. bootstrap resampling)
