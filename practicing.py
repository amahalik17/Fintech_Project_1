import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from datetime import timedelta


yf.pdr_override()
stock = input("Enter a stock ticker symbol: ")

# USE THIS to make ur time frame 1 year back
# from current date!!!
now = dt.datetime.now()
start = now - timedelta(days = 365)
df = pdr.get_data_yahoo(stock, start, now)

df = pdr.get_data_yahoo(stock, start, now)

print(now)
print(start)

###########################

