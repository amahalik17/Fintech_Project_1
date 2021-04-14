# import dependencies used
import pandas as pd
import numpy as np
import datetime as dt
#from pandas_datareader import data as pdr
import requests
import time
from config import api_key

# This program is a stock screener that utilizes the TD Ameritrade API
# and scans for stocks with excellent potential according to a specific set
# of rules, and uses Mark Minervini's Trend Template, as well as
# more personal scanning strategies, which have not yet been added, but will be soon
# after i finish the minervini script.

###################
# get a list of all SnP500 companies and put them in a list(by scraping wiki)
def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]
	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

###################

companies = get_sp500()
# using only some to speed up debugging process
companies = companies[0:300]
# adding the index to top of list, TD Ameritrade API doesnt have an option for ^GSPC so 
# i am going to use SPY which is an ETF that tracks/mimicks the S+P500, 
companies.insert(0, 'SPY')

print(companies)

# create dict to prevent overwrting in nested loop
prices = {}
metrics = {}
#count = 0

for x in companies:

	prices[x] = {}
	metrics[x] = {}
	#count += 1
	#time.sleep(1)
	#print('count: ', count)

	try:
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

			milli_date = i['datetime']
			date = dt.datetime.fromtimestamp(milli_date/1000.0)
			prices[x][date] = i['close']

		# add price and date data to pandas df
		price_df = pd.DataFrame.from_dict(prices)
		#print(price_df)

		# add moving average columns and calculate them respectively
		price_df['200_MA'] = price_df[x].rolling(window=200).mean()
		price_df['150_MA'] = price_df[x].rolling(window=150).mean()
		price_df['50_MA'] = price_df[x].rolling(window=50).mean()

		# calculate the rs, there are aprox 252 trading days in a year
		# rs is a comparison of how the company is doing relative to the overall market, 
		# in this case, the s+p500 etf we are using to respresent 'the market'
		price_df['Relative_Strength'] = (price_df[x].iloc[-1]/price_df['SPY'].iloc[-1]) / (price_df[x].iloc[-252]/price_df['SPY'].iloc[-252]) * 100

		# get last price
		metrics[x]['price'] = price_df[x].iloc[-1]
		# get the last MA for metrics dict
		metrics[x]['200_MA'] = price_df['200_MA'].iloc[-1]
		metrics[x]['150_MA'] = price_df['150_MA'].iloc[-1]
		metrics[x]['50_MA'] = price_df['50_MA'].iloc[-1]
		# get the ma from 30 days ago
		metrics[x]['200_MA_1month_ago'] = price_df['200_MA'].iloc[-30]
		metrics[x]['150_MA_1month_ago'] = price_df['150_MA'].iloc[-30]
		# get the ma from 60 days ago
		metrics[x]['200_MA_1month_ago'] = price_df['200_MA'].iloc[-60]
		metrics[x]['150_MA_1month_ago'] = price_df['150_MA'].iloc[-60]
		# get 52w low/high, this way works only if timefram is 1 yr, use other way if mult years
		metrics[x]['52_Week_Low'] = price_df[x].min()
		metrics[x]['52_Week_High'] = price_df[x].max()
		#metrics[x]['52_Week_Low'] = price_df[x][-252:].min()   ### other way
		#metrics[x]['52_Week_High'] = price_df[x][-252:].max()  ### other way
		# get rs
		metrics[x]['Rel_Strength'] = price_df['Relative_Strength'].iloc[-1]
		# get data where current price is at least 30% higher than the 52 week low
		metrics[x]['Above_30%_Low'] = metrics[x]['52_Week_Low'] * 1.3
		# get data where current price is within 25% of 52 week high
		metrics[x]['Within_25%_High'] = metrics[x]['52_Week_High'] * 0.75
	except:
		pass

#print(price_df)
#print(metrics)

# create a metrics df from the metrics dict
metrics_df = pd.DataFrame.from_dict(metrics)
# transpose, will change the index to the tickers
# seperates arrays, read transpose documentation for more info
metrics_df = metrics_df.T

# Add a name to index column after transposing
metrics_df.index.name = 'Symbols'

# get companies with 80%+ relative strength
metrics_df['RS_Rank'] = metrics_df['Rel_Strength'].rank(pct=True)
# export df to csv file
metrics_df.to_csv('Data/metrics_data.csv')
#print(metrics_df)

###################

metrics_df = pd.read_csv('Data/metrics_data.csv')

#1 The stock price is above 150 and 200 day MA
metrics_df['Rule1'] = (metrics_df['price'] > metrics_df['200_MA']) & (metrics_df['price'] > metrics_df['150_MA'])
#2 The 150 MA is above the 200 MA
metrics_df['Rule2'] = metrics_df['150_MA'] > metrics_df['200_MA']
#3 The 200 MA line is trending up for at least 1 month 
metrics_df['Rule3'] = metrics_df['200_MA'] > metrics_df['200_MA_1month_ago']
#4 The 50 MA is above the 150 and 200 MA
metrics_df['Rule4'] = (metrics_df['50_MA'] > metrics_df['200_MA']) & (metrics_df['50_MA'] > metrics_df['150_MA'])
#5 The stock price is above the 50 MA
metrics_df['Rule5'] = metrics_df['price'] > metrics_df['50_MA']
#6 The current stock price is at least 30 percent above its 52-week low
metrics_df['Rule6'] = metrics_df['price'] > metrics_df['Above_30%_Low']
#7 The current stock price is within at least 25 percent of its 52-week high.
metrics_df['Rule7'] = metrics_df['price'] > metrics_df['Within_25%_High']
#8 The relative strength ranking is above 80
metrics_df['Rule8'] = metrics_df['RS_Rank'] > 0.8

all_rules_met = metrics_df[(metrics_df['Rule1'] == True) & (metrics_df['Rule2'] == True) & (metrics_df['Rule3'] == True) & (metrics_df['Rule4'] == True)
		& (metrics_df['Rule5'] == True) & (metrics_df['Rule6'] == True) & (metrics_df['Rule7'] == True) & (metrics_df['Rule8'] == True)]


print(metrics_df)
print(all_rules_met)




