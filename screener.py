# import dependencies used
import pandas as pd
import numpy as np
#import yfinance as yf
import datetime as dt
#from pandas_datareader import data as pdr
import requests
import time
from config import api_key

''' This program is a stock screener that requires the use of the TD Ameritrade API
and scans for several key factors including:

'''

###################
# Get a list of all SnP500 companies and put them in a list(by scraping wiki)
def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]
	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

###################

companies = get_sp500()
# using 10 to speed up debugging process
companies = companies[0:3]
# Adding the index to top of list
#companies.insert(0,'^GSPC')
print(companies)

prices = {}
metrics = {}
#count = 0

for x in companies:
	prices[x] = {}
	metrics[x] = {}
	# define endpoint
	url = f'https://api.tdameritrade.com/v1/marketdata/{x}/pricehistory'
	# define payload
	payload = {
		'apikey':api_key,
		'periodType': 'year',
		'frequencyType': 'daily',
		'frequency': '1',
		'period': '1',
		'needExtendedHoursData': 'true'}
	# Make request and convert to dict
	response = requests.get(url, params=payload)
	data = response.json()
	#print(data)
	data = data['candles']
	for i in data:
		date = i['datetime']
		prices[x][date] = (i['close'])
	# add price and date data to pandas df
	price_df = pd.DataFrame.from_dict(prices)
	#print(price_df)
	# reverse the index to fix problem below
	price_df = price_df.iloc[::-1]

	# add moving average columns and calculate them respectively
	price_df['200_MA'] = price_df[x].rolling(window=200).mean()
	price_df['150_MA'] = price_df[x].rolling(window=150).mean()
	price_df['50_MA'] = price_df[x].rolling(window=50).mean()
	# Calculate the RS, there are aprox 252 trading days in a year
	#price_df['Relative_Strength'] = (price_df[x][-1]/price_df['^GSPC'][-1]) / (price_df[x][-252]/price_df['^GSPC'][-252]) * 100

	metrics[x]['200_MA'] = price_df['200_MA'][-1]
	metrics[x]['150_MA'] = price_df['150_MA'][-1]
	metrics[x]['50_MA'] = price_df['50_MA'][-1]

print(price_df)








