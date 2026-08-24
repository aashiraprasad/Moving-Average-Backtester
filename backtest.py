import numpy as np 
def run_backtest(stock_data,position_col,suffix):
    stock_data['Daily Return']=stock_data['Close'].pct_change()
    stock_data[f'Daily Strategy Return {suffix}']=stock_data['Daily Return'] * (stock_data[position_col])

    cost_rate = 0.001  # 0.1% per trade
    stock_data[f'Daily Strategy Return {suffix}'] -= cost_rate * np.abs(stock_data[f'Signal_{suffix}'])

    stock_data[f'Equity Curve {suffix}']=(1+stock_data[f'Daily Strategy Return {suffix}']).cumprod()
    stock_data['Comparison']=(1+stock_data['Daily Return']).cumprod()

    return stock_data

def summary_stats(stock_data,suffix):
    Final_Equity_Curve = (stock_data[f'Equity Curve {suffix}'].iloc[-1]-1)*100
    Total_Buy_and_Hold_return = (stock_data['Comparison'].iloc[-1] -1)*100
    Number_of_trades  = len(stock_data[stock_data[f'Signal_{suffix}']!=0])
    
    stock_data[f'Equity Curve Peak {suffix}']=stock_data[f'Equity Curve {suffix}'].cummax()
    stock_data[f'Drawdown {suffix}']=(stock_data[f'Equity Curve {suffix}'] / stock_data[f'Equity Curve Peak {suffix}'] -1)*100
    max_drawdown = stock_data[f'Drawdown {suffix}'].min()

    daily_returns=stock_data[f'Daily Strategy Return {suffix}']
    sharpe=(daily_returns.mean()/daily_returns.std())*np.sqrt(252)

    n = stock_data[f'Daily Strategy Return {suffix}'].count()
    final_value=stock_data[f'Equity Curve {suffix}'].iloc[-1]
    annualized_return=(final_value ** (252/n)) - 1

    result={
        'Final Equity Curve':Final_Equity_Curve,
        'Total Buy and Hold return':Total_Buy_and_Hold_return,
        'Number of trades':Number_of_trades,
        'Max Drawdown': max_drawdown,
        'Sharpe':sharpe,
        'Annualized Return':annualized_return
    }
    return result


def agreements(stock_data):
    per_agree = (stock_data['Position_EWMA'] == stock_data['Position_SMA']).mean()
    print(f"Percentage Agreement = {per_agree}")

    stock_data['disagree'] = stock_data['Position_EWMA'] != stock_data['Position_SMA']
    disagreement_days = stock_data[stock_data['disagree']]
    print(disagreement_days[[('Date',''), 'Position_EWMA', 'Position_SMA']])