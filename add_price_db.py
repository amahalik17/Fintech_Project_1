from config import alpaca_api_key, alpaca_secret, base_url, db_path
import alpaca_trade_api as tradeapi
import sqlite3

api = tradeapi.REST(alpaca_api_key, alpaca_secret, base_url)

connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = []
stock_dict = {}

# This makes it easier to reference pk and fk
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

group_size = 200
for i in range(0, len(symbols), group_size):

    symbol_group = symbols[i:i+group_size]
    barsets = api.get_barset(symbol_group, 'day')

    for symbol in barsets:
        print(f"processing symbol {symbol}")
        
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()
