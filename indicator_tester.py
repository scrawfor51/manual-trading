#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 21:24:11 2022

@author: Stephen
"""


"""

Functions checked: get_data; sma; sma_ratio; momentum; Bollinger Bands, BBP, RSI, Aroon, stochastic oscillator 

Still unsure: EMA, MACD (Requires EMA), Signal (Requires EMA), OBV (Needs volume data)
"""

import tech_ind
import os
import pandas as pd 
from matplotlib import pyplot as plt 
import math
import numpy as np
from backtest import get_data as gd
from matplotlib import pyplot 




processed_data_price = tech_ind.get_data(start_date='2019-01-01', end_date='2019-02-01', symbols=['DIS'], include_spy=(False))
processed_data_vol = tech_ind.get_data(start_date='2019-01-01', end_date='2019-02-01', symbols=['DIS'], column_name = 'Volume', include_spy=(False))
obv = tech_ind.On_Balance_Volume(processed_data_price, processed_data_vol)
williams_per  = tech_ind.Williams_Percentage_Range(processed_data_price)
bb = tech_ind.Bollinger_Bands(processed_data_price, 14)
plot = bb.plot(figsize=(15, 12), title='Bolinger Bands')
plot.set_ylabel('Price Per Share')
plot.set_xticks(step=1)

trades = processed_data_price.copy()
trades.loc[:,:] = np.NaN


# Create a binary (0-1) array showing when price is above SMA-14.
sma_crossovers = pd.DataFrame(0, index=bb.index, columns=["Price"])
bb_bottom_crossovers = sma_crossovers.copy()
bb_top_crossovers = sma_crossovers.copy()

bb_ratios = sma_crossovers.copy()

bb_ratios["Price"] = bb["Price"] / bb["Price"]
bb_ratios["SMA"] = bb["Price"] / bb["SMA"]
bb_ratios["Top Band"] = bb["Price"] / bb["Top Band"]
bb_ratios["Bottom Band"] = bb["Price"] / bb["Bottom Band"]
    
    
sma_crossovers[bb_ratios["SMA"] >= 1] = 1

bb_bottom_crossovers[bb_ratios["Bottom Band"] >= 1] = 1

bb_top_crossovers[bb_ratios["Top Band"] >= 1] = 1

# Turn that array into one that only shows the crossings (-1 == cross down, +1 == cross up).
sma_crossovers.iloc[1:] = sma_crossovers.diff().iloc[1:]
sma_crossovers.iloc[0] = 0

bb_bottom_crossovers.iloc[1:] = bb_bottom_crossovers.diff().iloc[1:]
bb_bottom_crossovers.iloc[0] = 0

bb_top_crossovers.iloc[1:] = bb_top_crossovers.diff().iloc[1:]
bb_top_crossovers.iloc[0] = 0

sma_intersection_up_rows = bb_ratios.index[sma_crossovers["Price"] == 1]
sma_intersection_down_rows = bb_ratios.index[sma_crossovers["Price"] == -1]

bb_top_intersection_up_rows = bb_ratios.index[bb_top_crossovers["Price"] == 1]
bb_top_intersection_down_rows = bb_ratios.index[bb_top_crossovers["Price"] == -1]

bb_bottom_intersection_up_rows = bb_ratios.index[bb_bottom_crossovers["Price"] == 1]
bb_bottom_intersection_down_rows = bb_ratios.index[bb_bottom_crossovers["Price"] == -1]

plot.plot(sma_intersection_up_rows, bb["Price"][sma_intersection_up_rows], 'rD')
plot.plot(sma_intersection_down_rows, bb["Price"][sma_intersection_down_rows], 'bD')

# plot.plot(bb_top_intersection_up_rows, bb["Price"][bb_top_intersection_up_rows], 'r.')
# plot.plot(bb_top_intersection_down_rows, bb["Price"][bb_top_intersection_down_rows], 'b.')

# plot.plot(bb_bottom_intersection_up_rows, bb["Price"][bb_bottom_intersection_up_rows], 'r*')
# plot.plot(bb_bottom_intersection_down_rows, bb["Price"][bb_bottom_intersection_down_rows], 'b*')
