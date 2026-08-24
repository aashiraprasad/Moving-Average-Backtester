# Moving Average Crossover Backtester

A small quantitative finance project exploring **moving-average crossover strategies** using Python.

This is my first quantitative finance project, built as an early exploration of algorithmic trading, financial time series, and backtesting.

The project compares two simple technical strategies:

* **20/50 Exponentially Weighted Moving Average (EWMA) crossover**
* **20/50 Simple Moving Average (SMA) crossover**

The strategies are tested across several stocks and compared against a simple **buy-and-hold** benchmark.

> **Note:** This project is for educational purposes only. It is not intended to provide financial advice or a production-ready trading system.

---

## Project Overview

The basic idea is straightforward:

> If the short-term moving average crosses above the long-term moving average, generate a buy signal. If it crosses below, generate a sell signal.

For both strategies, I use:

* Short moving average: **20 trading days**
* Long moving average: **50 trading days**

The EWMA strategy uses exponentially weighted averages, while the SMA strategy uses ordinary rolling averages.

The project then asks:

**How do these simple strategies perform compared with simply buying and holding the stock?**

---

## Strategies

### 1. EWMA Crossover

The EWMA strategy calculates:

* `EMA20`
* `EMA50`

A buy signal is generated when the previous day's EMA20 was below EMA50 and the current EMA20 moves above EMA50.

A sell signal is generated for the opposite crossover.

The implementation also shifts the resulting position by one day before calculating strategy returns, so the signal generated on a day is not immediately used to calculate that same day's return.

### 2. SMA Crossover

The SMA strategy works in the same way, but uses:

* `SMA20`
* `SMA50`

calculated using rolling 20-day and 50-day averages.

---

## Backtesting

The backtester calculates daily percentage returns and applies the strategy's position to those returns.

I also included a transaction cost of **0.1% per signal/trade**:

```python
cost_rate = 0.001
```

The strategy's equity curve is then calculated by compounding the daily returns. A separate buy-and-hold equity curve is calculated as a benchmark.

The backtest produces the following metrics:

* Final strategy return
* Buy-and-hold return
* Number of signals/trades
* Maximum drawdown
* Sharpe ratio
* Annualized return

These statistics are calculated in `summary_stats()`.

---

## Stocks Tested

The current version tests six tickers:

| Ticker | Company      |
| ------ | ------------ |
| AAPL   | Apple        |
| BRBY.L | Burberry     |
| TSLA   | Tesla        |
| MSFT   | Microsoft    |
| GOOGL  | Alphabet     |
| RL     | Ralph Lauren |

Market data is downloaded using `yfinance`, currently starting from **January 1, 2024** and continuing to the date on which the program is run.

---

## Results

The current run produced the following results:

| Ticker | Strategy | Strategy Return | Buy & Hold | Trades | Max Drawdown | Sharpe |
| ------ | -------- | --------------: | ---------: | -----: | -----------: | -----: |
| AAPL   | EWMA     |           1.96% |     68.67% |     11 |      -33.99% |   0.17 |
| AAPL   | SMA      |          -2.07% |     68.67% |     17 |      -35.33% |   0.10 |
| BRBY.L | EWMA     |         -67.09% |    -23.57% |     16 |      -80.54% |  -0.92 |
| BRBY.L | SMA      |          -8.51% |    -23.57% |     11 |      -59.93% |   0.10 |
| TSLA   | EWMA     |          43.53% |     46.07% |      8 |      -54.34% |   0.53 |
| TSLA   | SMA      |          23.97% |     46.07% |     12 |      -54.47% |   0.43 |
| MSFT   | EWMA     |         -36.48% |     33.08% |     17 |      -48.79% |  -0.51 |
| MSFT   | SMA      |         -50.04% |     33.08% |     14 |      -51.92% |  -0.88 |
| GOOGL  | EWMA     |          67.90% |    151.78% |     11 |      -25.22% |   0.79 |
| GOOGL  | SMA      |          91.36% |    151.78% |      8 |      -24.02% |   0.98 |
| RL     | EWMA     |         -25.75% |    164.05% |     11 |      -47.45% |  -0.13 |
| RL     | SMA      |         -57.84% |    164.05% |     13 |      -67.54% |  -0.78 |

### Some observations

A few things stood out from the results:

1. **Buy-and-hold performed better than both moving-average strategies for most of these stocks.**

2. **GOOGL was the strongest result for the moving-average strategies.**
   The SMA strategy returned about 91.36%, compared with 151.78% for buy-and-hold.

3. **TSLA produced relatively competitive results.**
   EWMA returned approximately 43.53%, compared with 46.07% for buy-and-hold.

4. **BRBY.L, MSFT and RL show how badly a simple crossover strategy can perform in some periods.**

5. **EWMA and SMA can produce noticeably different results even though they use the same basic crossover idea.**

These results are not evidence that one strategy is universally better. They simply describe what happened during this particular backtest period.

---

## Visualisations

The project generates two types of plots.

### Price and Trading Signals

For each stock and strategy, the program plots:

* closing price
* short moving average
* long moving average
* buy signals
* sell signals

The plotting code distinguishes between EWMA and SMA and places the crossover signals directly on the price chart.

### Equity Curve

The equity curve compares:

* EWMA strategy
* SMA strategy
* Buy-and-hold

This makes it easier to see how the strategies evolve over time rather than only looking at their final returns.

---

## Project Structure

```text
moving_average_backtester/
│
├── main.py
├── data.py
├── strategy.py
├── backtest.py
├── plotting.py
└── README.md
```

### `data.py`

Responsible for downloading market data and determining the currency symbol for a ticker.

### `strategy.py`

Contains:

* data cleaning
* EWMA calculation
* SMA calculation
* buy/sell signal generation
* position generation

### `backtest.py`

Contains:

* strategy return calculation
* transaction costs
* equity curves
* performance statistics
* strategy agreement analysis

### `plotting.py`

Creates price/signal charts and strategy-vs-buy-and-hold equity curves.

### `main.py`

Acts as the pipeline connecting everything together.

For each ticker it:

1. downloads the data
2. cleans the data
3. generates EWMA signals
4. generates SMA signals
5. runs both backtests
6. calculates statistics
7. stores the results
8. produces the plots

---

## Running the Project

### Requirements

The project currently uses:

```text
Python
numpy
pandas
matplotlib
yfinance
```

Install the dependencies with:

```bash
pip install numpy pandas matplotlib yfinance
```

### Run

Clone the repository and run:

```bash
python main.py
```

The program will download the latest available data for the configured tickers, run the backtests, print the comparison tables, and generate the visualisations.

---

## What I Learned

This project was primarily a learning exercise.

Some of the concepts I explored were:

* Python project structure
* working with financial time series
* `pandas` DataFrames
* moving averages
* exponentially weighted moving averages
* signal generation
* position management
* backtesting
* transaction costs
* cumulative returns
* maximum drawdown
* Sharpe ratio
* annualised returns
* data visualisation
* comparing a strategy against a benchmark

One of the more interesting parts was discovering that a strategy that sounds reasonable in theory can perform substantially worse than simply holding the underlying asset.

---

## Limitations

This is a relatively simple backtester and has several limitations.

### 1. Very small strategy set

Only two moving-average crossover strategies are currently implemented.

### 2. Limited universe

The backtest currently uses only six stocks.

### 3. No portfolio construction

Each stock is considered independently. There is currently no portfolio-level allocation, position sizing, or capital allocation model.

### 4. Simplified transaction costs

The model applies a fixed 0.1% cost to signals. Real trading costs can depend on the broker, market, liquidity, spread and order size.

### 5. No slippage

The model does not currently simulate bid-ask spreads or market impact.

### 6. No parameter optimisation

The 20/50 moving-average periods were chosen as fixed parameters rather than optimised against the data.

### 7. No out-of-sample testing

The current project does not separate training and testing periods, so the results should not be interpreted as evidence of future performance.

### 8. "Number of trades"

The current implementation counts non-zero signals, meaning a buy or sell signal is counted individually rather than grouping a complete buy-to-sell cycle into one round-trip trade.

---

## Future Improvements

Some things I would like to explore next:

* [ ] Add more stocks and asset classes
* [ ] Add configurable moving-average periods
* [ ] Add more technical strategies
* [ ] Add stop-loss and take-profit rules
* [ ] Add slippage modelling
* [ ] Add position sizing
* [ ] Add portfolio-level backtesting
* [ ] Add train/test splits
* [ ] Perform walk-forward testing
* [ ] Compare different transaction-cost assumptions
* [ ] Add statistical significance testing
* [ ] Improve the definition of a "trade"
* [ ] Add automated performance reports
* [ ] Investigate whether the apparent strategy differences are statistically meaningful

---

## Why I Built This

I am currently in the early stages of studying **Engineering Mathematics and Computer Science**, and this is my first project exploring quantitative finance.

The goal was not to build a sophisticated trading system immediately, but to understand the basic mechanics of turning a mathematical idea into code:

**mathematical idea → trading rule → signal → position → returns → backtest → evaluation**

This project is the beginning of my exploration into quantitative finance and systematic trading.

---

## Disclaimer

This project is intended for **educational and research purposes only**.

Backtested performance does not guarantee future results. The strategies implemented here are simplified models and should not be used as a basis for real financial decisions without substantially more research, testing and risk analysis.
