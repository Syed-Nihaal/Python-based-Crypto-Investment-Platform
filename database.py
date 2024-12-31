import sqlite3

# Path to the SQLite database file
path = 'CW2/crypto_investment_platform.db'

def initialise_database():
    # Establishing a connection to the database
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    # Creating tables for accounts, portfolio, transactions, and assets if they do not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT NOT NULL, balance REAL NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS portfolio (username TEXT, asset_name TEXT, quantity INTEGER, FOREIGN KEY(username) REFERENCES accounts(username))")
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions (username TEXT, asset_name TEXT, quantity INTEGER, action TEXT, date TEXT, FOREIGN KEY(username) REFERENCES accounts(username))")
    cursor.execute("CREATE TABLE IF NOT EXISTS assets (asset_name TEXT PRIMARY KEY, price REAL NOT NULL)")

    # Inserting asset data into the assets table
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Bitcoin", 100475))
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Ethereum",3785))
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Tether", 1))
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Solana", 229))
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Binance Coin", 695))
    cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Litecoin", 115))

    # Commiting changes and close the connection
    connection.commit()
    connection.close()

def get_connection():
    # Return a new connection to the database
    return sqlite3.connect(path)