import pandas as pd
import bs4 as bs
import requests

html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text)

tickers = []
names = []

table = soup.find('table', {'class': 'wikitable sortable'})
rows = table.findAll('tr')[1:]

for row in rows:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker[:-1])

for row in rows:
    name = row.findAll('td')[1].text
    names.append(name[:-1])

df = pd.DataFrame(list(zip(tickers, names)))
#print(df)
#df.to_csv('otherdata/sp500names.csv', index=False)
