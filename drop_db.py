import sqlite3
from config import db_path


connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
""")

cursor.execute("""
    DROP TABLE stock
""")

cursor.execute("""
    DROP TABLE users
""")

connection.commit()