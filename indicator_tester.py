#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 21:24:11 2022

@author: Stephen
"""


"""

Functions checked: get_data; sma; sma_ratio; momentum; Bollinger Bands, BBP. RSI, Aroon, tochastic oscillator 

Still unsure: EMA, MACD (Requires EMA), Signal (Requires EMA), OBV (Needs volume data)


"""
import tech_ind
import os
import pandas as pd 
from matplotlib import pyplot as plt 
import math
import numpy as np
from backtest import get_data as gd




processed_data = tech_ind.get_data('2010-01-01', '2010-12-31', ['GOOG'], include_spy=(False))
aroon = tech_ind.Aroon_Oscillator(processed_data)
print(aroon)