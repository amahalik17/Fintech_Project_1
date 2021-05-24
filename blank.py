# import dependencies used
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import requests
import time
from config import api_key



# Will come back to this method, it will be the same screener, a different
# way, by iterating through the df and using if statements to pick out winners


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

# metrics_df = pd.read_csv('Data/metrics_data.csv')
# metrics_df = metrics_df.head(50)
# print(metrics_df)

#stock_df = pd.DataFrame(stock_data)
#print(stock_df)

# for x in metrics_df.index:


#     #1 The stock price is above 150 and 200 day MA
#     metrics_df['Rule1'] = (metrics_df['price'] > metrics_df['200_MA']) & (metrics_df['price'] > metrics_df['150_MA'])
#     #2 The 150 MA is above the 200 MA
#     metrics_df['Rule2'] = metrics_df['150_MA'] > metrics_df['200_MA']
#     #3 The 200 MA line is trending up for at least 1 month 
#     metrics_df['Rule3'] = metrics_df['200_MA'] > metrics_df['200_MA_1month_ago']
#     #4 The 50 MA is above the 150 and 200 MA
#     metrics_df['Rule4'] = (metrics_df['50_MA'] > metrics_df['200_MA']) & (metrics_df['50_MA'] > metrics_df['150_MA'])
#     #5 The stock price is above the 50 MA
#     metrics_df['Rule5'] = metrics_df['price'] > metrics_df['50_MA']
#     #6 The current stock price is at least 30 percent above its 52-week low
#     metrics_df['Rule6'] = metrics_df['price'] > metrics_df['Above_30%_Low']
#     #7 The current stock price is within at least 25 percent of its 52-week high.
#     metrics_df['Rule7'] = metrics_df['price'] > metrics_df['Within_25%_High']
#     #8 The relative strength ranking is above 80
#     metrics_df['Rule8'] = metrics_df['RS_Rank'] > 0.8

#     all_rules_met = metrics_df[(metrics_df['Rule1'] == True) & (metrics_df['Rule2'] == True) & (metrics_df['Rule3'] == True) & (metrics_df['Rule4'] == True)
#             & (metrics_df['Rule5'] == True) & (metrics_df['Rule6'] == True) & (metrics_df['Rule7'] == True) & (metrics_df['Rule8'] == True)]


#print(metrics_df)
#print(all_rules_met)




#for x in stock_data.index:

    # if ((stock_data['price'][x] > stock_data['200_MA'][x]) and (stock_data['price'][x] > stock_data['150_MA'][x])):
    #     rule1 = True
    #     if (rule1 == True):
    #         stock_df['rule 1'] = rule1
    # else:
    #     rule1 = False
    #     stock_df['rule 1'] = rule1
    # print(rule1)

    # if (stock_data['150_MA'][x] > stock_data['200_MA'][x]):
    #     rule2 = True
    #     stock_data['rule_2'] = 'good'
    # else:
    #     rule2 = False
    #     stock_data['rule_2'] = 'bad'
    #print(rule2)
#print(stock_data)

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
    
#print(stock_df)

# print(x)



