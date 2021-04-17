# import dependencies used
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
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

stock_df = pd.DataFrame(stock_data)
print(stock_df)

for x in stock_data.index:

    if ((stock_data['price'][x] > stock_data['200_MA'][x]) and (stock_data['price'][x] > stock_data['150_MA'][x])):
        rule1 = True
        if (rule1 == True):
            stock_df['rule 1'] = rule1
    else:
        rule1 = False
        stock_df['rule 1'] = rule1
    #print(rule1)

    # if (stock_data['150_MA'][x] > stock_data['200_MA'][x]):
    #     rule2 = True
    #     if (rule2 == True):
    #         stock_df['rule 2'] = rule2
    # else:
    #     rule2 = False
    #     stock_df['rule 2'] =rule2
    # #print(rule2)

    # if (stock_data['200_MA'][x] > stock_data['200_MA_1month_ago'][x]):
    #     rule3 = True
    #     if (rule3 == True):
    #         stock_df['rule 3'] = rule3
    # else:
    #     rule3 = False
    #     stock_df['rule 3'] = rule3
    # #print(rule3)

    # if ((stock_data['50_MA'][x] > stock_data['200_MA'][x]) and (stock_data['50_MA'][x] > stock_data['150_MA'][x])):
    #     rule4 = True
    #     if (rule4 == True):
    #         stock_df['rule 4'] = rule4
    # else:
    #     rule4 = False
    #     stock_df['rule 4'] = rule4
    # #print(rule4)

    # if (stock_data['price'][x] > stock_data['50_MA'][x]):
    #     rule5 = True
    #     if (rule5 == True):
    #         stock_df['rule 5'] = rule5
    # else:
    #     rule5 = False
    #     stock_df['rule 5'] = rule5
    # #print(rule5)

    # if (stock_data['price'][x] > stock_data['Above_30%_Low'][x]):
    #     rule6 = True
    #     if (rule6 == True):
    #         stock_df['rule 6'] = rule6
    # else:
    #     rule6 = False
    #     stock_df['rule 6'] = rule6
    # #print(rule6)

    # if (stock_data['price'][x] > stock_data['Within_25%_High'][x]):
    #     rule7 = True
    #     if (rule7 == True):
    #         stock_df['rule 7'] = rule7
    # else:
    #     rule7 = False
    #     stock_df['rule 7'] = rule7
    # #print(rule7)

    # if (stock_data['RS_Rank'][x] > 0.8):
    #     rule8 = True
    #     if (rule8 == True):
    #         stock_df['rule 8'] = rule8
    # else:
    #     rule8 = False
    #     stock_df['rule 8'] = rule8
    # #print(rule8)

    # if((rule1 == True) and (rule2 == True) and (rule3 == True) and (rule4 == True) and (rule5 == True) and (rule6 == True) and (rule7 == True) and (rule8 == True)):
    #     all_rules_met = True
    #     buy_now = 'BUY!'
    #     print(buy_now)
    #     print(all_rules_met)
    # else:
    #     all_rules_met = False
    
    print(stock_df)




# print(x)












