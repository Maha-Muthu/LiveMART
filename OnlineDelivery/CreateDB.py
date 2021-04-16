import sqlite3
connection = sqlite3.connect('Database.db')
connection.execute('CREATE TABLE Wholesalers (username TEXT PRIMARY KEY, password TEXT )')
connection.close()
