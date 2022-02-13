# import dependencies used
import pandas as pd
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

'''This is a strategy to identify when a stock has reached an ATH
and rests for at least 3 months, then starts to break out, and
signals a good entry point. For now, this program will use the yahoo 
finance api for simplicity purposes,'''

# Get stock data like this, use this workaround since its changed
yf.pdr_override()

# Set time data
now = dt.datetime.now()
start_date = now - dt.timedelta(days = 365)

# Ask user for stock ticker/symbol
stock = input("Enter a stock ticker symbol: ")
#print(stock)
while stock != "stop":
    df = pdr.get_data_yahoo(stock, start_date, now)

    df.drop(df[df['Volume'] < 1000].index, inplace= True)

    month_data = df.groupby(pd.Grouper(freq="M"))["High"].max()
    
    # Define variables for previous ATHs, and rest periods, and current ATHs
    recent_ATH_date = 0
    recent_ATH_value = 0

    current_ATH_date = ""
    current_ATH_value = 0

    for index, value in month_data.items():
        # Check if the current monthly high is greater than the current ATH
        # then set the values
        if value > current_ATH_value:
            current_ATH_value = value
            current_ATH_date = index
            month_counter = 0

        if value < current_ATH_value:
            month_counter = month_counter + 1

            if month_counter == 3 and ((index.month != now.month) or (index.year != now.year)):
                if current_ATH_value != recent_ATH_value:
                    print(current_ATH_value)
                recent_ATH_date = current_ATH_date
                recent_ATH_value = current_ATH_value
                # Reset monthly counter
                month_counter = 0

    if recent_ATH_value == 0:
        message = stock + " does not appear to be on a breakout."
    else:
        message = (" Last breakout " + str(recent_ATH_value) + " on " + str(recent_ATH_date))
    
    print(message)

    stock = input("Enter a stock ticker symbol: ")




