# Import dependencies and api key
from config import api_key
import requests, time, re, os
import pandas as pd
import pickle as pkl

# define endpoint/url
url = "https://api.tdameritrade.com/v1/instruments"

# Read in data, and store symbols in list
df = pd.read_csv('Data/sandp500.csv')
symbols = df['Symbol'].values.tolist()

start = 0
end = 500
files = []

#print(len(symbols))

# iterate throuh symbols list
while start < len(symbols):
    tickers = symbols[start:end]


    # define payload
    payload = {
        'apikey': api_key,
        'symbol': tickers,
        'projection': 'fundamental'}

    # make request
    results = requests.get(url, params=payload)
    data = results.json()
    #print(data)
    f_name = time.asctime() + '.pkl'
    f_name = re.sub('[ :]', '_', f_name)
    files.append(f_name)
    with open(f_name, 'wb') as file:
        pkl.dump(data, file)
    start = end
    end += 500
    time.sleep(1)

#print(len(data))
#print(data.keys())

data = []

for x in files:
    with open(x, 'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    points = ['symbol', 'netProfitMarginMRQ', 'peRatio', 'pegRatio', 'high52']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(x)
    
points = ['symbol', 'Margin', 'PE', 'PEG', 'high52']
df_results = pd.DataFrame(data, columns=points)

print(df_results)




# # define endpoint
# url_1 = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format('GOOG')

# # define payload
# payload = {
#     'apikey':api_key,
#     'periodType': 'day',
#     'frequencyType': 'minute',
#     'frequency': '1',
#     'period': '2',
#     'needExtendedHoursData': 'true'}

# # Make request
# content = requests.get(url_1, params=payload)

# # convert to dict
# data = content.json()
# print(data)