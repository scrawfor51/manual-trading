#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 19:01:42 2022
@author: Stephen
"""

import tech_ind 
import pandas as pd
import numpy as np
import backtester_manual_trading as backtester
from matplotlib import cm
import matplotlib.pyplot as plt


class OracleStrategy:
    def __init__(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def train(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def test(self, start_date='2018-01-01', end_date='2019-12-31', symbol = 'DIS', starting_cash = 200000):
        
        df_trades = tech_ind.get_data(start_date=start_date, end_date=end_date, symbols=[symbol], include_spy=False)
        daily_returns = df_trades.copy()
        daily_returns.values[1:,:] = df_trades.values[1:,:] - df_trades.values[:-1, :]
        daily_returns.values[0, 0] = 0
        print("Daily Returns :", daily_returns)
        
        
        trades = df_trades.copy()
        trades.loc[:,:] = np.NaN
        
        trades[daily_returns[symbol].shift(-1) > 0] = 1000
        trades[daily_returns[symbol].shift(-1) < 0] = -1000

        
      
        trades.iloc[1:] = trades.diff().iloc[1:]
        
        print("Trades: ", trades)
        
        # And more importantly, drop all rows with no non-zero values (i.e. no trades).
        trades = trades.loc[(trades != 0).any(axis=1)]
        trades.iloc[-1] = 0 - (trades.iloc[-2,:] / 2)
     
        """
        # Compose the output trade list.
        trade_list = []
    
        for day in trades.index:
            if trades.loc[day,symbol] > 0:
                trade_list.append([day.date(), symbol, 'BUY', 1000])
            elif trades.loc[day,symbol] < 0:
                trade_list.append([day.date(), symbol, 'SELL', 1000])
    
        # Dump the trades to stdout.  (Redirect to a file if you wish.)
        for trade in trade_list:
            print ("    ".join(str(x) for x in trade))       
            
        
        daily_returns.values[1:,:] = abs(df_trades.values[1:,:] - df_trades.values[:-1, :]) * 1000
        daily_returns.values[0, :] = np.nan
        daily_returns['Cumulative Returns'] = (daily_returns).cumsum()
        daily_returns['Max Value'] = 200000 + daily_returns['Cumulative Returns']
        
        """
        
        print(trades)
        return trades


if __name__ == "__main__": 
    
    #start_date = '2018-01-01', end_date = '2019-12-31'
    start ='2019-01-01'
    end = '2020-12-31'
    sym = "SPY"
    data = tech_ind.get_data(start_date = start, end_date = end, symbols =[sym],  include_spy=False)
   
    daily_returns = (data.shift()-data) * 1000
    daily_returns.values[0, :] = np.nan
    daily_returns = daily_returns.cumsum()
    
    OS = OracleStrategy()
    oracle = OS.test(start_date = start, end_date = end, symbol = sym)
    portfolio = backtester.assess_strategy_dataframe(oracle, start, end, starting_value = 200000, fixed_cost = 0, floating_cost = 0)
    print(portfolio)
    backtester.calc_portfolio(portfolio, starting_value = 200000)
    base_returns = daily_returns
    base_returns.columns = ['Portfolio']
    backtester.calc_portfolio(base_returns, starting_value = 200000)
    base_returns.columns = ['Baseline']
    base_returns['Max Value'] =  portfolio - 200000
    plot = base_returns.plot(title='Baseline vs. Oracle', colormap=cm.Accent)
    plot.grid()
    plt.show()
    
