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
#print(stock_data)

for x in stock_data.index:

    if ((stock_data['price'][x] > stock_data['200_MA'][x]) and (stock_data['price'][x] > stock_data['150_MA'][x])):
        rule1 = True
    else:
        rule1 = False
    print(rule1)
#     if (stock_data['150_MA'] > stock_data['200_MA']):
#         rule2 = True
#     else:
#         rule2 = False
#     if (stock_data['200_MA'] > stock_data['200_MA_1month_ago']):
#         rule3 = True
#     else:
#         rule3 = False
#     if ((stock_data['50_MA'] > stock_data['200_MA']) and (stock_data['50_MA'] > stock_data['150_MA'])):
#         rule4 = True
#     else:
#         rule4 = False
#     if (stock_data['price'] > stock_data['50_MA']):
#         rule5 = True
#     else:
#         rule5 = False
#     if (stock_data['price'] > stock_data['Above_30%_Low']):
#         rule6 = True
#     else:
#         rule6 = False
#     if (stock_data['price'] > stock_data['Within_25%_High']):
#         rule7 = True
#     else:
#         rule7 = False
#     if (stock_data['RS_Rank'] > 0.8):
#         rule8 = True
#     else:
#         rule8 = False
#     if((rule1 == True) and (rule2 == True) and (rule3 == True) and (rule4 == True) and (rule5 == True) and (rule6 == True) and (rule7 == True) and (rule8 == True)):
#         all_rules_met = True
#         print(all_rules_met)
#     else:
#         all_rules_met = False
# print(x)

