# import dependencies used
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import requests
import time
from config import api_key

''' This program is a stock screener that utilizes the TD Ameritrade API
and scans for stocks with excellent potential according to a specific set
of rules, and uses Mark Minervini's Trend Template, as well as many 
more of my own personal scanning strategies.

'''

###################
# get a list of all SnP500 companies and put them in a list(by scraping wiki)
# def get_sp500():
# 	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# 	sp500_tickers = sp500_tickers[0]
# 	tickers = sp500_tickers['Symbol'].values.tolist()
# 	return tickers

# ###################

# companies = get_sp500()
# # using only some to speed up debugging process
# companies = companies[0:50]
# # adding the index to top of list, TD Ameritrade API doesnt have an option for ^GSPC so 
# # i am going to use SPY which is an ETF that tracks/mimicks the S+P500, 
# companies.insert(0, 'SPY')

# print(companies)

stock_data = pd.read_csv('Data/metrics_data.csv')
stock_data = stock_data.head()
print(stock_data)

export_list = pd.DataFrame(columns=['Symbol', 'RS_Rating', '50_MA', '150_MA', '200_MA', '52_Low', '52_High'])

for x in stock_data.index:
    symbol = str(stock_data['Symbols'][x])
    rel_strength = stock_data['Rel_Strength'][x]

    try:
        df = pdr.get_data_yahoo(stock, start, now)