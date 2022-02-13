# import dependencies used
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# This is a strategy that displays 6 short term EMAs in red 
# and 6 longer term EMAs in blue, 
# it's a quick way of finding a
# short term trends in equities, 
# entry point = when red first crosses blue
# and sell point = when blue crosses red

# Get stock data like this, use this workaround since its changed
yf.pdr_override()

# Ask user for stock ticker/symbol
stock = input("Enter a stock ticker symbol: ")
#print(stock)

now = dt.datetime.now()
start_date = now - dt.timedelta(days = 365)
df = pdr.get_data_yahoo(stock, start_date, now)

# Exponential moving averages list
all_emas = [3, 5, 8, 10, 12, 15, 30, 40, 50, 75, 100, 150]

# Iterate through ema list
for x in all_emas:
    ema = x
    # This creates new column for each ema used and sets it equal to
    df['Ema_' + str(ema)] = round(df["Adj Close"].ewm(span=ema, adjust=False).mean(), 2)
    
print(df.tail())

# Define variables that will determine if a position should be entered
# The num variable will keep track of the row we are on
# The percentchange list is where we will store our trades
position = 0
number = 0
percent_change = []
# Iterate through each date and check for rwb pattern, df.index is date
for i in df.index:
    # These are the values we need to determine if we are in a rwb pattern
    ema_min = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])
    ema_max = max(df["Ema_30"][i], df["Ema_40"][i], df["Ema_50"][i], df["Ema_75"][i], df["Ema_100"][i], df["Ema_150"][i])
    close = df["Adj Close"][i]

    # If we are in a rwb pattern
    if (ema_min > ema_max):
        print("Red White Blue")
        # Buy at closing price
        if (position == 0):
            buy_price = close
            # Turn our position on(buy)
            position = 1
            print("Buying now at " + str(buy_price))

    elif (ema_min < ema_max):
        print("Blue White Red")
        # If we are in a position and we want to sell because pattern changed to bwr
        if (position == 1):
            position = 0
            sell_price = close
            print("Selling now at " + str(sell_price))
            # Calculates profit
            pc = (sell_price/buy_price - 1) * 100
            # Adds percent change value to our list for analysis
            percent_change.append(pc)

    if (number == df["Adj Close"].count() - 1 and position == 1):
        position = 0
        sell_price = close
        print("Selling now at " + str(sell_price))
        pc = (sell_price/buy_price - 1) * 100
        percent_change.append(pc)
    
    number += 1

print(percent_change)


# Analysis and summary statistics

# Define variables
gains = 0
gain_count = 0
losses = 0
loss_count = 0
total_return = 1

# Iterate through each value in percent change list
for x in percent_change:
    if (x > 0):
        gains += 1
        gain_count += 1
    else:
        losses += 1
        loss_count += 1
    total_return = total_return * ((x/100) + 1)

# Multiply all %s together to calculate total return for each trade
# Round and display as % for user
total_return = round((total_return - 1) * 100, 2)

# Calculate avg gain and loss and win-loss ratio
if (gain_count > 0):
    avg_gain = gains/gain_count
    # Find best trade from list
    best_trade = str(max(percent_change))
else:
    avg_gain = 0
    best_trade = "No good trade!"

if (loss_count > 0):
    avg_loss = losses/loss_count
    # Find worst trade from list
    worst_trade = str(min(percent_change))
    # Create win/loss ratio
    ratio = str(avg_gain/avg_loss)
else:
    avg_loss = 0
    worst_trade = "No good trade!"
    ratio = "Infinite"

# Calculate % of good vs. bad trades
if (gain_count > 0 or loss_count > 0):
    win_loss_ratio = gain_count/(gain_count+loss_count)
else:
    win_loss_ratio = 0

# Results
print("--------------------------------------------------------")
print(f"Results for {stock} going back to {str(df.index[0])}")
print(f"Sample size: {str(gain_count + loss_count)} trades")
print(f"EMAs used: {str(all_emas)}")
print(f"Win/Loss ratio: {str(win_loss_ratio)}")
print(f"Gain/loss ratio: {ratio}")
print(f"Average Gain: {str(avg_gain)}")
print(f"Average Loss: {str(avg_loss)}")
print(f"Best Trade Return: {best_trade}")
print(f"Worst Trade Return: {worst_trade}")
print(f"Total return % over {str(gain_count + loss_count)} trades: {str(total_return)} %")
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )















# i must give credit where credit is due, some of this program was inspired 
# and instructed by 'richard moglen' on youtube











