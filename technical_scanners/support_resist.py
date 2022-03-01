# import dependencies used
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

# Get stock data like this, use this workaround since its changed
yf.pdr_override()

# Set date info
now = dt.datetime.now()
start_date = now - dt.timedelta(days = 365)

# Ask user for stock ticker/symbol
stock = input("Enter a stock ticker symbol: ")
#print(stock)

# type stop for the input to squit program
while stock != "stop":
    
    df = pdr.get_data_yahoo(stock, start_date, now)

    df['High'].plot(label = "High")

    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = max(Range, default = 0)
        value = round(df['High'][i], 2)

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(Range, default = 0):
            counter += 1
        else:
            counter = 0
        if counter == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)

    print(" ")
    print(str(pivots))
    print(str(dates))

    timedelta = dt.timedelta(days = 30)

    for index in range(len(pivots)):
        print(str(pivots[index]) + " : " + str(dates[index]))

        plt.plot_date([dates[index], dates[index] + timedelta], 
        [pivots[index], pivots[index]], linestyle = "-", linewidth = 2, marker = ",")


    plt.show()

    stock = input("Enter a stock ticker symbol: ")

