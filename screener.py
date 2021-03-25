# import dependencies used
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import requests
import time


# Get stock data like this, use this workaround since its changed
yf.pdr_override()

# Get a list of all SnP500 companies and put them in a list(by scraping wiki)
def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]

	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

companies = get_sp500()
# Adding the index to top of list
companies.insert(0,'^GSPC')