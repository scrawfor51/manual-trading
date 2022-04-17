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
        
        
        trades = df_trades.copy()
        trades.loc[:,:] = np.NaN
        
        trades[daily_returns[symbol].shift(-1) > 0] = 1000
        trades[daily_returns[symbol].shift(-1) < 0] = -1000

        
      
        trades.iloc[1:] = trades.diff().iloc[1:]
        
        # And more importantly, drop all rows with no non-zero values (i.e. no trades).
        trades = trades.loc[(trades != 0).any(axis=1)]
        trades.iloc[-1] = 0 - (trades.iloc[-2,:] / 2)
    
        return trades


if __name__ == "__main__": 
    
    #start_date = '2018-01-01', end_date = '2019-12-31'
    start ='2018-01-01'
    end = '2019-12-31'
    
    data = tech_ind.get_data(start_date = start, end_date = end, symbols =['DIS'],  include_spy=False)
   
    baseline = data.copy()
    baseline.loc[:,:] = np.NaN
    baseline.iloc[0,0] = 1000
    baseline_portfolio = backtester.assess_strategy_dataframe(baseline, start, end, starting_value = 200000, fixed_cost = 0, floating_cost = 0)
    print("BASELINE STATS: ")
    backtester.calc_portfolio(baseline_portfolio)
    
    
    OS = OracleStrategy()
    oracle = OS.test(start_date = start, end_date = end)
    oracle_portfolio = backtester.assess_strategy_dataframe(oracle, start, end, starting_value = 200000, fixed_cost = 0, floating_cost = 0)
    print(oracle_portfolio)
    print("ORACLE STATS: ")
    backtester.calc_portfolio(oracle_portfolio)
    
   
    base_returns = baseline_portfolio.copy() - 200000
    base_returns.columns = ['Baseline']
    base_returns['Max Value'] =  oracle_portfolio - 200000
    plot = base_returns.plot(title='Baseline vs. Oracle', colormap=cm.Accent)
    plot.grid()
    
