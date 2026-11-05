import numpy as np 
from strategy import warmup_rows
def run_backtest(stock_data,position_col,suffix,cost_rate=0.001):
    stock_data['Daily Return']=stock_data['Close'].pct_change()
    stock_data[f'Daily Strategy Return {suffix}']=stock_data['Daily Return'] * (stock_data[position_col])

    # Costs are charged on the day the position actually changes, on the notional
    # actually traded. A +1 -> -1 flip trades two units, not one, so we charge
    # |change in position| instead of "one trade per signal" - which also landed a
    # day early, because the signal is known one day before the position is taken.

    traded_notional = stock_data[position_col].fillna(0.0).diff().abs().fillna(0.0)
    stock_data[f'Traded Notional {suffix}'] = traded_notional
    stock_data[f'Transaction Cost {suffix}'] = traded_notional * cost_rate
    stock_data[f'Daily Strategy Return {suffix}'] -= stock_data[f'Transaction Cost {suffix}']

    stock_data[f'Equity Curve {suffix}']=(1+stock_data[f'Daily Strategy Return {suffix}']).cumprod()
    stock_data['Comparison']=(1+stock_data['Daily Return']).cumprod()

    return stock_data

def _sharpe(daily_returns,periods=252):
    sd=daily_returns.std()
    if not np.isfinite(sd) or sd==0:
        return float('nan')
    return (daily_returns.mean()/sd)*np.sqrt(periods)

def summary_stats(stock_data,suffix,start=0):
    # Measured only over the period in which the strategy can actually act. Before
    # the slow MA is computable there is no signal, so those rows are dead time:
    # they dilute the mean and (because zeros cut volatility more slowly than they
    # cut the mean) understate Sharpe. Strategy and benchmark are rebased to the
    # same start row so the comparison is apples to apples.
    window = stock_data.iloc[start:]
    strategy_returns = window[f'Daily Strategy Return {suffix}']
    equity = (1 + strategy_returns).cumprod()
    benchmark = window['Comparison'] / window['Comparison'].iloc[0]

    trade_events = int((window[f'Traded Notional {suffix}'] > 0).sum())
    turnover_units = float(window[f'Traded Notional {suffix}'].sum())
    cost_charged = float(window[f'Transaction Cost {suffix}'].sum())

    n = int(strategy_returns.count())
    final_value = float(equity.iloc[-1])
    bh_value = float(benchmark.iloc[-1])

    drawdown = (equity / equity.cummax() - 1) * 100
    bh_drawdown = (benchmark / benchmark.cummax() - 1) * 100

    result={
        'Final Equity Curve':(final_value-1)*100,
        'Total Buy and Hold return':(bh_value-1)*100,
        'Number of trades':trade_events,
        'Turnover (units)':turnover_units,
        'Total Cost Charged (%)':cost_charged*100,
        'Max Drawdown': float(drawdown.min()),
        'Buy and Hold Max Drawdown': float(bh_drawdown.min()),
        'Sharpe':_sharpe(strategy_returns),
        'Buy and Hold Sharpe':_sharpe(window['Daily Return']),
        'Annualized Return': final_value ** (252/n) - 1,
        'Buy and Hold Annualized Return': bh_value ** (252/n) - 1,
        'Days Measured': n
    }
    return result

def _spell_lengths(mask):
    # Lengths of consecutive True runs in a boolean mask.
    lengths=[]; run=0
    for flag in mask:
        if flag:
            run+=1
        elif run:
            lengths.append(run); run=0
    if run:
        lengths.append(run)
    return lengths

def agreements(stock_data,start=None):
    # Two corrections to the headline number. First, measure the positions actually
    # held (yPosition_*) rather than the signal-day positions, because exposure - not
    # intent - is what drives the P&L. Second, skip the warm-up: before the slow MA
    # exists both strategies sit flat at 0, which scores as agreement that never
    # happened and inflates the result.
    if start is None:
        start = warmup_rows(stock_data)
    window = stock_data.iloc[start:]
    a = window['yPosition_EWMA'].fillna(0.0)
    b = window['yPosition_SMA'].fillna(0.0)
    disagree = (a != b).to_numpy()
    spells = _spell_lengths(disagree)
    result={
        'Days Compared': len(a),
        'Agreement (%)': float((a == b).mean() * 100),
        'Disagreement Days': int(disagree.sum()),
        'Disagreement Spells': len(spells),
        'Median Spell (days)': float(np.median(spells)) if spells else 0.0,
        'Longest Spell (days)': int(max(spells)) if spells else 0
    }
    print(f"  Agreement {result['Agreement (%)']:.1f}% of {result['Days Compared']} days "
          f"({result['Disagreement Days']} disagreeing) across {result['Disagreement Spells']} spells "
          f"| median {result['Median Spell (days)']:.0f}d, longest {result['Longest Spell (days)']}d")
    return result