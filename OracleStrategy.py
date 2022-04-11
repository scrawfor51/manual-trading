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
