#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 19:01:42 2022

@author: Stephen
"""

import tech_ind 

class OracleStrategy:
    def __init__(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def train(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def test(start_date = '2018-01-01', end_date = '2019-12-31', symbol = 'DIS', starting_cash = 200000):
        # Inputs represent the date range to consider, the single stock to trade, and the starting portfolio value.
        #
        # Return a date-indexed DataFrame with a single column containing the desired trade for that date.
        # Given the position limits, the only possible values are -2000, -1000, 0, 1000, 2000.
        
        df_trades = tech_ind.get_data(start_date, end_date, symbol)
        
        return df_trades

    