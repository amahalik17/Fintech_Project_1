# import dependencies used
import pandas as pd
import numpy as np
#import yfinance as yf
import datetime as dt
#from pandas_datareader import data as pdr
import requests
import time
from config import api_key

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
companies = companies[0:2]
# Adding the index to top of list
#companies.insert(0,'^GSPC')

print(companies)

# # Define a function that get price history data
# def get_history():
# 	# define url
# 	price_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
# 	# define payload
# 	payload = {
# 		'apikey':api_key,
# 		'periodType': 'year',
# 		'frequencyType': 'daily',
# 		'frequency': '1',
# 		'period': '1',
# 		'needExtendedHoursData': 'true'
# 		}
# 	# Make request
# 	response = requests.get(price_url, params=payload)
# 	# convert to dict
# 	data = response.json()
# 	return data



prices = {}
metrics = {}
count = 0

for x in companies:
	prices[x] = {}
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

	# Make request
	response = requests.get(url, params=payload)
	# convert to dict
	data = response.json()
	#print(data)
	data = data['candles']
	for i in data:
		date = i['datetime']
		prices[x][date] = (i['close'])

print(prices)








