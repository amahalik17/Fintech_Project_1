import sqlite3
from config import db_path

def create_db_tables():

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY, 
            symbol TEXT NOT NULL UNIQUE, 
            name TEXT NOT NULL,
            exchange TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_price (
            id INTEGER PRIMARY KEY, 
            stock_id INTEGER,
            date NOT NULL,
            open NOT NULL, 
            high NOT NULL, 
            low NOT NULL, 
            close NOT NULL, 
            volume NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email NOT NULL UNIQUE,
            password NOT NULL,
            first_name NOT NULL,
            last_name NOT NULL
        )
    """)


# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS strategy (
#         id INTEGER PRIMARY KEY,  
#         name NOT NULL
#     )
# """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS stock_strategy (
#         stock_id INTEGER NOT NULL, 
#         strategy_id INTEGER NOT NULL,
#         FOREIGN KEY (stock_id) REFERENCES stock (id)
#         FOREIGN KEY (strategy_id) REFERENCES strategy (id)
#     )
# """)

# strategies = ['opening_range_breakout', 'opening_range_breakdown']

# for strategy in strategies:
#     cursor.execute("""
#         INSERT INTO strategy (name) VALUES (?)
#     """, (strategy,))


    connection.commit()