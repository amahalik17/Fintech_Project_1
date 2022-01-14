# Import dependencies
import talib
import yfinance as yf
from flask import Flask
import pandas as pd
from pattern_dict import patterns

data = yf.download("SPY", start="2021-01-13", end="2022-01-14")
print(data)


morningstar = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morningstar
data['Engulfing'] = engulfing

engulf_days = data[data['Engulfing'] != 0]
morningstar_days = data[data['Morning Star'] != 0]

print(engulf_days)
print(morningstar_days)




