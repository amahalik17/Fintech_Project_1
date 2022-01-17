import sqlite3
import alpaca_trade_api as tradeapi
from config import alpaca_api_key, alpaca_secret

connection = sqlite3.connect('fintech_app.db')

cursor = connection.cursor()
#cursor.execute("DELETE FROM stock")

api = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret,
    base_url='https://paper-api.alpaca.markets'
    )
assets = api.list_assets()

for asset in assets:
    #print(asset)
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(e)
        print(asset)

connection.commit()
