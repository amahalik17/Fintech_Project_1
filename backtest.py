# import dependencies used
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# Get stock data like this, use this workaround since its changed
yf.pdr_override()

# Ask user for stock ticker/symbol
stock = input("Enter a stock ticker symbol: ")
#print(stock)

# Define date data for our start date parameter in next step
startyear = 2020
startmonth = 10
startday = 1

# Define datetime object so python can process as a date
start = dt.datetime(startyear, startmonth, startday)
# Set end date, im choosing current date
now = dt.datetime.now()
# Store all data in a df
df = pdr.get_data_yahoo(stock, start, now)
#print(df)

# Exponential moving averages list
all_emas = [5, 10, 15, 30, 45, 50]

# Iterate through ema list
for x in all_emas:
    ema = x
    # This creates new column for each ema used and sets it equal to
    df['Ema_' + str(ema)] = round(df["Adj Close"].ewm(span=ema, adjust=False).mean(), 2)
    
print(df.tail())


for i in df.index:
    ema_min = min(df["Ema_5"][i], df["Ema_10"][i], df["Ema_15"])
    ema_max = max(df["Ema_30"][i], df["Ema_45"][i], df["Ema_50"])
    close = df["Adj Cose"][i]

    if (ema_min > ema_max):
        print("Red White Blue")
    elif (ema_min < ema_max):
        print("Blue White Red")









