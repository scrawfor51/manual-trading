#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 19:01:42 2022

@author: Stephen
"""

import tech_ind 
import pandas as pd
import numpy as np

class OracleStrategy:
    def __init__(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def train(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def test(self, start_date='2018-01-01', end_date='2019-12-31', symbol = 'DIS', starting_cash = 200000):
        # Inputs represent the date range to consider, the single stock to trade, and the starting portfolio value.
        #
        # Return a date-indexed DataFrame with a single column containing the desired trade for that date.
        # Given the position limits, the only possible values are -2000, -1000, 0, 1000, 2000.
        
        
        # do you want to be long or do you want to be short 
        # from today to tomorrow do you want to have positive stock or negative stock 
        
        df_trades = tech_ind.get_data(start_date=start_date, end_date=end_date, symbols=[symbol], include_spy=False)
       
        daily_returns = df_trades.copy()
        daily_returns.values[1:,:] = abs(df_trades.values[1:,:] - df_trades.values[:-1, :]) * 1000
        daily_returns.values[0, :] = np.nan
        daily_returns['Cumulative Returns'] = (daily_returns).cumsum()
        daily_returns['Max Value'] = 200000 + daily_returns['Cumulative Returns']
                
        print(daily_returns)
        return daily_returns


if __name__ == "__main__":    
    OS = OracleStrategy()
    OS.test()
