
from config import db_path
import sqlite3


connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# cursor.execute("""
#     INSERT INTO id, email, password, first_name, last_name FROM users
# """)

# cursor.execute("""
#     INSERT INTO users (id, email, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)
# """, (x, x))

rows = cursor.fetchall()

connection.commit()