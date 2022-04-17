"""
Created on Thu Apr 15

"""

import tech_ind 
import pandas as pd
import numpy as np
import backtester_manual_trading as backtester
from matplotlib import cm
import matplotlib.pyplot as plt

class TechnicalStrategy:
    def __init__(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def train(self, *params, **kwparams):
        # Defined so you can call it with any parameters and it will just do nothing.
        pass

    def test(self, start_date='2020-01-01', end_date='2021-12-31', symbol = 'DIS', starting_cash = 200000):
        
        lookback = 9
        
        price = tech_ind.get_data(start_date, end_date, symbols=[symbol], include_spy=(False))
        
        ### Use the three indicators to make some kind of trading decision for each day.
        trades = price.copy()
        trades.loc[:,:] = np.NaN
        volume = tech_ind.get_data(start_date, end_date, symbols=[symbol], column_name = 'Volume', include_spy=(False))
        obv = tech_ind.On_Balance_Volume(price, volume)
        williams_per  = tech_ind.Williams_Percentage_Range(price, lookback)
        bb = tech_ind.Bollinger_Bands(price, lookback)        
        
        obv_avg = obv.rolling(window=lookback,min_periods=lookback).mean()
        
        

        # Create a binary (0-1) array showing when price is above SMA-14.
        sma_cross = pd.DataFrame(0, index=bb.index, columns= ["SMA"])
        
        bb_ratios = sma_cross.copy()
        
        bb_ratios["Price"] = bb["Price"] / bb["Price"]
        bb_ratios["SMA"] = bb["Price"] / bb["SMA"]        
        
        sma_cross[bb_ratios["SMA"] >= 1] = 1
        
        #Create a binary (0-1) array showing when price is within 10% of OBV-14
        obv_trade = pd.DataFrame(0, index=bb.index, columns= ["OBV Trade"])
        obv_trade[abs(obv[symbol]/obv_avg[symbol] - 1) < .1] = 1
        #obv_trade = obv_trade.loc[(obv_trade != 0).any(axis=1)]
        #obv_trade["OBV Trade"] = 1 if abs(obv/obv_avg - 1) < 1 else 0
        
        print(obv_trade)
        
        # Turn that array into one that only shows the crossings (-1 == cross down, +1 == cross up).
        sma_cross.iloc[1:] = sma_cross.diff().iloc[1:]
        sma_cross.iloc[0] = 0         
        
        #Return to mean strategy when price is above/below the Bollinger Bands but valued as "overbought" or "oversold" by the Williams Percent Range or On-Balance Volume, buy to expect reversion to mean
        #Short when high, buy when low
        #print(williams_per)
        print(obv)
        print(obv_avg)
        trades[(bb["Top Band"] < bb["Price"]) & ((williams_per["Williams Percentage"] < -20) & (obv_trade["OBV Trade"] == 1)) ] = 1000
        trades[(bb["Bottom Band"] > bb["Price"]) & ((williams_per["Williams Percentage"] > -80) & (obv_trade["OBV Trade"] == 1))] = 1000
        
        #Breakout Strategy when price is above/below the Bollinger Bands but not valued as "overbought" or "oversold" by the Williams Percent Range AND On-Balance Volume, buy to ride the momentum
        # Short when low, buy when high
        trades[(bb["Top Band"] < bb["Price"]) & ((williams_per["Williams Percentage"] > -20) & (obv_trade["OBV Trade"] == 0))] = 1000
        trades[(bb["Bottom Band"] > bb["Price"]) & ((williams_per["Williams Percentage"] < -80) & (obv_trade["OBV Trade"] == 0))] = 1000        
        
        # Apply our exit order conditions all at once.  Again, this represents TARGET SHARES.
        trades[(sma_cross != 0)] = 0       
        
        #Close trade to avoid skewing the calculations by shorting on last day
        trades.iloc[-1] = 0
        
        # Forward fill NaNs with previous values, then fill remaining NaNs with 0.
        trades.ffill(inplace=True)
        trades.fillna(0, inplace=True)
        
        trades.iloc[1:] = trades.diff().iloc[1:]
        trades.iloc[0] = 0        
        
        # And more importantly, drop all rows with no non-zero values (i.e. no trades).
        trades = trades.loc[(trades != 0).any(axis=1)]
        
       
        print(trades)
        return trades


if __name__ == "__main__":    
    start ='2019-01-01'
    end = '2020-12-31'
    sym = "SPY"
    data = tech_ind.get_data(start_date = start, end_date = end, symbols =[sym],  include_spy=False)
   
    daily_returns = (data.shift()-data) * 1000
    daily_returns.values[0, :] = np.nan
    daily_returns = daily_returns.cumsum()
    
    TS = TechnicalStrategy()
    tech_trader = TS.test(start_date = start, end_date = end, symbol = sym)
    portfolio = backtester.assess_strategy_dataframe(tech_trader, start, end, starting_value = 200000)
    print(portfolio)
    backtester.calc_portfolio(portfolio, starting_value = 200000)
    base_returns = daily_returns
    base_returns.columns = ['Portfolio']
    backtester.calc_portfolio(base_returns, starting_value = 200000)
    base_returns.columns = ['Baseline']
    base_returns['Technical Strategy'] =  portfolio - 200000
    plot = base_returns.plot(title='Baseline vs. Technical Strategy', colormap=cm.Accent)
    plot.grid()
    plt.show()