
patterns = {
    'CDL2CROWS':'Two Crows',
    'CDL3BLACKCROWS':'Three Black Crows',
    'CDL3INSIDE':'Three Inside Up/Down',
    'CDL3LINESTRIKE':'Three-Line Strike',
    'CDL3OUTSIDE':'Three Outside Up/Down',
    'CDL3STARSINSOUTH':'Three Stars In The South',
    'CDL3WHITESOLDIERS':'Three Advancing White Soldiers',
    'CDLABANDONEDBABY':'Abandoned Baby',
    'CDLADVANCEBLOCK':'Advance Block',
    'CDLBELTHOLD':'Belt-hold',
    'CDLBREAKAWAY':'Breakaway',
    'CDLCLOSINGMARUBOZU':'Closing Marubozu',
    'CDLCONCEALBABYSWALL':'Concealing Baby Swallow',
    'CDLCOUNTERATTACK':'Counterattack',
    'CDLDARKCLOUDCOVER':'Dark Cloud Cover',
    'CDLDOJI':'Doji',
    'CDLDOJISTAR':'Doji Star',
    'CDLDRAGONFLYDOJI':'Dragonfly Doji',
    'CDLENGULFING':'Engulfing Pattern',
    'CDLEVENINGDOJISTAR':'Evening Doji Star',
    'CDLEVENINGSTAR':'Evening Star',
    'CDLGAPSIDESIDEWHITE':'Up/Down-gap side-by-side white lines',
    'CDLGRAVESTONEDOJI':'Gravestone Doji',
    'CDLHAMMER':'Hammer',
    'CDLHANGINGMAN':'Hanging Man',
    'CDLHARAMI':'Harami Pattern',
    'CDLHARAMICROSS':'Harami Cross Pattern',
    'CDLHIGHWAVE':'High-Wave Candle',
    'CDLHIKKAKE':'Hikkake Pattern',
    'CDLHIKKAKEMOD':'Modified Hikkake Pattern',
    'CDLHOMINGPIGEON':'Homing Pigeon',
    'CDLIDENTICAL3CROWS':'Identical Three Crows',
    'CDLINNECK':'In-Neck Pattern',
    'CDLINVERTEDHAMMER':'Inverted Hammer',
    'CDLKICKING':'Kicking',
    'CDLKICKINGBYLENGTH':'Kicking - bull/bear determined by the longer marubozu',
    'CDLLADDERBOTTOM':'Ladder Bottom',
    'CDLLONGLEGGEDDOJI':'Long Legged Doji',
    'CDLLONGLINE':'Long Line Candle',
    'CDLMARUBOZU':'Marubozu',
    'CDLMATCHINGLOW':'Matching Low',
    'CDLMATHOLD':'Mat Hold',
    'CDLMORNINGDOJISTAR':'Morning Doji Star',
    'CDLMORNINGSTAR':'Morning Star',
    'CDLONNECK':'On-Neck Pattern',
    'CDLPIERCING':'Piercing Pattern',
    'CDLRICKSHAWMAN':'Rickshaw Man',
    'CDLRISEFALL3METHODS':'Rising/Falling Three Methods',
    'CDLSEPARATINGLINES':'Separating Lines',
    'CDLSHOOTINGSTAR':'Shooting Star',
    'CDLSHORTLINE':'Short Line Candle',
    'CDLSPINNINGTOP':'Spinning Top',
    'CDLSTALLEDPATTERN':'Stalled Pattern',
    'CDLSTICKSANDWICH':'Stick Sandwich',
    'CDLTAKURI':'Takuri (Dragonfly Doji with very long lower shadow)',
    'CDLTASUKIGAP':'Tasuki Gap',
    'CDLTHRUSTING':'Thrusting Pattern',
    'CDLTRISTAR':'Tristar Pattern',
    'CDLUNIQUE3RIVER':'Unique 3 River',
    'CDLUPSIDEGAP2CROWS':'Upside Gap Two Crows',
    'CDLXSIDEGAP3METHODS':'Upside/Downside Gap Three Methods'
}


# import pandas as pd
# import yfinance as yf
# import os
# import talib
# import sqlite3
# from config import db_path
# from datetime import date

# #for x in patterns:
#     #print(x[0])

# pattern = 'CDLDOJI'
# stocks = {}

# # Establish connection and cursor
# connection = sqlite3.connect(db_path)
# connection.row_factory = sqlite3.Row
# cursor = connection.cursor()

# # Create a list of all symbols in my stock db
# cursor.execute("""SELECT * FROM stock""")
# #stock_data = cursor.fetchall()

# # Make a symbols list
# symbols_list = [i[1] for i in cursor.fetchall()]

# # shorten list to speed up debugging process
# # symbols_list = symbols_list[0:100]
# #print(symbols_list)

# #df = pd.DataFrame(symbols_list)
# #print(df)

# # cursor.execute("""SELECT stock_id, date, open, high, low, close FROM stock_price ORDER BY date DESC""")
# # price_data = cursor.fetchall()

# cursor.execute("""
#     select symbol, name, stock_id, open, high, low, close, date
#     from stock_price join stock on stock.id = stock_price.stock_id
#     group by stock_id
#     order by symbol
# """)

# price_data = cursor.fetchall()

# price_df = pd.DataFrame(price_data)
# #print(price_df)

# for symbol in symbols_list:
#     stocks[symbol] = {"Company": ""}

# #print(stocks)


# if pattern:
#     for symbol in symbols_list:
#         pattern_func = getattr(talib, pattern)
#         try:
#             result = pattern_func(price_df[3], price_df[4], price_df[5], price_df[6])
#             #print(result)
#             last = result.tail(1).values[0]
#             if last > 0:
#                 stocks[symbol][pattern] = "Bullish"
#             elif last < 0:
#                 stocks[symbol][pattern] = "Bearish"
#             else:
#                 stocks[symbol][pattern] = None
#         except:
#             pass

# print(stocks)

# REMEMBER***note to self***
#print(df[2][0])

