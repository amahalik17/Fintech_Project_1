# import dependencies used
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
from flask import request
import time
import yfinance as yf
from config import db_path
import sqlite3



# Establish a connection to our sqlite database
connection = sqlite3.connect(db_path)
#connection.row_factory = sqlite3.Row
cursor = connection.cursor()

sql_query = """SELECT symbol FROM stock"""

cursor.execute("""SELECT symbol FROM stock""")

symbols_list = cursor.fetchall()
symbols_list = symbols_list[0:100]
#symbols = [row['symbol'] for row in symbols_list]

print(symbols_list)
#print(len(symbols))

# ticker_df = pd.read_sql(sql_query, connection)
# print(ticker_df)

yf.pdr_override()

# Ask user for stock ticker/symbol
stock = input("Enter a stock ticker symbol: ")
print(stock)

startyear = 2021
startmonth = 1
startday = 1

start = dt.datetime(startyear, startmonth, startday)

# 1 year historical data
#start_date = now - dt.timedelta(days = 365)

now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)

# method to loop through symbols list instead of asking user for stock
# for x in symbols:
#     df = pdr.get_data_yahoo(x, start, now)
#     print(x)
#     print(df)

# Create moving average variable
ma = 50

# Allow for different MA values
smaString = "Sma_" + str(ma)

# Add MA column to df
# Create the MA column with rolling MA with window size of our MA
df[smaString] = df["Adj Close"].rolling(window=ma).mean()

# Cut out first 50 rows because they have no 50-day MA 
df = df.iloc[ma:]
print(df)

# Define counters used in loop
numHigher = 0
numLower = 0


# Iterate through each date to check if closing value is above the MA
# In this df, the dates are the index row
for x in df.index:
    #print(df['Adj Close'][x])
    #print(df[smaString][x])
    # If adj close is higher then MA for specific date
    if (df['Adj Close'][x] > df[smaString][x]):
        #print("The close is higher than the MA")
        # Count the number of times close price was higher
        numHigher += 1
    else:
        #print("The close is lower than the MA")
        # Count the number of times close price was higher
        numLower += 1

print(f"The closing price was higher than the {ma} day moving average {str(numHigher)} times.")
print(f"The closing price was lower than the {ma} day moving average {str(numLower)} times.")

