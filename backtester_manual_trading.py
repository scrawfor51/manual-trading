import pandas as pd
from tech_ind import get_data
import datetime
import math as m


def assess_strategy_dataframe(trades, start_date, end_date, starting_value = 1000000, fixed_cost = 9.95, floating_cost = 0.005):

    #Get traded symbol
    symbol = trades.columns

    #get stock data
    stocks_vals = get_data(start_date, end_date, symbol, include_spy=False)
   
    #shares = stocks_vals.index
    shares = pd.DataFrame(index=stocks_vals.index)
    
    cash_val = pd.DataFrame(index=stocks_vals.index)
    cash_val.loc[start_date:, "Cash"] = starting_value
  
    shares.loc[start_date:, symbol] = 0


    
    for day in trades.index:
        
        trade_shares = trades.loc[day,symbol].values[0]
        total_transaction_value = trade_shares * stocks_vals.loc[day, symbol].values[0]
        

        if trade_shares > 0:
            shares.loc[day : , symbol] += trade_shares
            cash_val.loc[day :, "Cash"] -=  total_transaction_value*(1 + floating_cost) + fixed_cost
            
        elif trade_shares < 0:
            shares.loc[day :, symbol] += trade_shares
            cash_val.loc[day : , "Cash"] -=  total_transaction_value*(1 - floating_cost) - fixed_cost
   
 
    portfolio_val = pd.DataFrame(index=stocks_vals.index)
    
    portfolio_val['Portfolio'] = (shares.values * stocks_vals.values)+ cash_val
    
    return portfolio_val

def calc_portfolio(portfolio_val, starting_value = 200000, risk_free_rate = 0.0, sample_freq = 252):
    
    portfolio = portfolio_val.copy()
    end_value = portfolio_val["Portfolio"].iloc[-1]
    average_daily_return = ((portfolio["Portfolio"]/ portfolio["Portfolio"].shift()) - 1).mean()
    stdev_daily_return = ((portfolio_val["Portfolio"]/ portfolio_val["Portfolio"].shift()) - 1).std()
    cumulative_return = (end_value/starting_value) - 1 
    sharpe_ratio = m.sqrt(sample_freq) * ((average_daily_return - risk_free_rate)/ stdev_daily_return)

    print("Sharpe Ratio: ", sharpe_ratio)    
    print("Volatility (stdev of daily returns): ", stdev_daily_return)
    print("Average Daily Return: ", average_daily_return)
    print("Cumulative Return: ", cumulative_return)
    print("End Value: ", end_value)


