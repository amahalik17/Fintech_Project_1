import os
import pandas as pd


def is_consolidating(df, percentage=3):
    recent_candles = df[-15:]
    #print(recent_candles)

    max_close = recent_candles['Close'].max()
    min_close = recent_candles['Close'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True
    
    return False

    #print("The max close was {} and the min close was {}".format(max_close, min_close))




def is_breaking_out(df, percentage=3):
    last_close = df[-1:]['Close'].values[0]
    #print(last_close)

    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-16:-1]

        if last_close > recent_closes['Close'].max():
            return True

    return False

for filename in os.listdir('Data'):
    df = pd.read_csv('Data/{}'.format(filename))
    #print(df)

    if is_consolidating(df, percentage=3):
        print("{} is consolidating".format(filename))
    
    if is_breaking_out(df):
        print("{} is breaking out".format(filename))



