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

# Create moving average variable
ma = 50
# Allow for different MA values
smaString = "Sma_" + str(ma)
# Add MA column to df

df[smaString] = df["Adj Close"].rolling(window=ma).mean()
#print(df)

# Cut out first 50 rows because they have no 50-day MA 
df = df.iloc[ma:]
print(df)

# Define counters used in loop
numHigher = 0
numLower = 0

# Iterate through each day(date) to check if closing value is above the ma
# Since in this df, the dates are the index
for i in df.index:
    #print(df.iloc[:,4][i])
    #print(df['Adj Close'][i])
    #print(df[smaString][i])
    if (df['Adj Close'][i] > df[smaString][i]):
        print("The close is higher than the MA")
        # Count the number of times close price was higher
        numHigher += 1
    else:
        print("The close is lower than the MA")
        # Count the number of times close price was higher
        numLower += 1

print(f"The closing price was higher than the {ma} day moving average {str(numHigher)} times.")
print(f"The closing price was lower than the {ma} day moving average {str(numLower)} times.")











