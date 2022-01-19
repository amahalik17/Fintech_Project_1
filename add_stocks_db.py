# Import dependencies
import sqlite3
import alpaca_trade_api as tradeapi
from config import alpaca_api_key, alpaca_secret, base_url, db_path

# Establish connection
connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row

# Define cursor
cursor = connection.cursor()

# This would delete all data in a stock table
#cursor.execute("DELETE FROM stock")

cursor.execute("""SELECT symbol, name FROM stock""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]
#print(symbols)

api = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret,
    base_url
    )
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol}, {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()


