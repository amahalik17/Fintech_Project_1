import mysql.connector
from config import db_pw


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=f"{db_pw}",
    database="my_database"
)

my_cursor = mydb.cursor()
# my_cursor.execute("CREATE DATABASE my_database")
# my_cursor.execute("SHOW DATABASES")

#my_cursor.execute("CREATE TABLE Person (name VARCHAR)")