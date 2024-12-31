# Importing external modules
from socket import *
import sqlite3
import datetime
from database import initialise_database, get_connection
import threading

# Server address configuration
HOST = "127.0.0.1"
PORT = 4000
ADDRESS = (HOST, PORT)

class Server:
    def __init__(self):
        # Initialising the server socket by binding to the address and listening for incoming connections
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(ADDRESS)
        self.server_socket.listen(5)
        print(f"Server running at {HOST}:{PORT}")

    def handle_client(self, client_socket, client_address):
        # Handling communication with a connected client
        print(f"Connection from {client_address}")
        try:
            # Creating a loop to communicate with client
            while True:
                # Receiving data from the client
                data = client_socket.recv(1024).decode()
                if not data:
                    print(f"Client {client_address} disconnected.")
                    break
                # Sending response back to the client
                response = self.handle_request(data)
                client_socket.send(response.encode())
        # If server is not able to connect to the client
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
        # Closing the client socket
        finally:
            client_socket.close()

    def create_server(self):
        # Creating a loop to accept incoming client connections and start a new thread for each client
        print("Server is ready to connect.")
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_request(self, request):
        # Processing the client's request and return a response
        try:
            # Spliting the request into parts and extracting the action from the parts
            parts = request.split(";")
            action = parts[0]
            match action:
                case "create_account":
                    return User.create_account(parts[1], parts[2], float(parts[3]))
                case "login":
                    return User.login(parts[1], parts[2])
                case "view_assets":
                    return Assets.view_assets()
                case "deposit":
                    return User.update_balance(parts[1], float(parts[2]))
                case "withdraw":
                    return User.update_balance(parts[1], -float(parts[2]))
                case "view_portfolio":
                    return Portfolio.view_portfolio(parts[1])
                case "buy_assets":
                    return Portfolio.buy_assets(parts[1], parts[2], int(parts[3]))
                case "sell_assets":
                    return Portfolio.sell_assets(parts[1], parts[2], int(parts[3]))
                case "logout":
                    return User.logout()
        # If there is an error with the request sent by the client
        except (IndexError, ValueError) as e:
            return f"Error: Malformed request. {e}"

class User:
    def create_account(username, password, balance):
        # Creating a new user account
        with get_connection() as conn:
            cursor = conn.cursor()
            # If the username is not registered, creates a new user account
            try:
                # Inserting the user's information into the database
                cursor.execute(" INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)", (username, password, balance))
                conn.commit()
                return "Account created successfully."
            # If the username is already taken
            except sqlite3.IntegrityError:
                return "Error: Username already exists."

    def login(username, password):
        # Authenticating a username and password to login
        with get_connection() as conn:
            # Querying the database for the user's information
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            # If the username and password are correct
            if result:
                return "Login successful."
            # If the username and password are incorrect
            else:
                return "Error: Invalid username or password."

    def update_balance(username, amount):
        # Updating the user's account balance
        with get_connection() as conn:
            # Querying the database for the user's information
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            result = cursor.fetchone()
            # If the user exists
            if result:
                # Updating the user's balance
                new_balance = result[0] + amount
                # If the new balance is insufficient
                if new_balance < 0:
                    return "Error: Insufficient funds for this transaction."
                # Updating user's balance
                cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (new_balance, username))
                conn.commit()
                return f"Balance updated successfully. New balance: ${new_balance:.2f}"
            # If user does not exist
            else:
                return "Error: Account not found."
    
    def logout():
        return "Logout successful."

class Account:
    def __init__(self, username, password, balance=0):
        # Initialising an account object
        self.username = username
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        # Depositing an amount into the account
        if amount >= 0:
            self.balance += amount
            print("Deposit successful.")
        # If deposit amount is greater or equal to $1,000,000
        elif amount >= 1000000:
            print("Error: Invalid amount. User cannot deposit more than $1,000,000 in their account.")
        else:
            print("Error: Invalid amount.")

    def withdraw(self, amount):
        # Withdrawing an amount from the account
        # If the amount is insufficient
        if amount > self.balance:
            print(f"Error: Insufficient balance. Current balance: ${self.balance:.2f}")
        # User cannot withdraw $0 or negative amount.
        elif amount <= 0:
            print("Error: Invalid amount. Amount must be greater than 0.")
        # If withdraw amount is greater or equal to $1,000,000
        elif amount >= 1000000:
            print("Error: Invalid amount. User cannot withdraw more than $1,000,000 in their account.")
        else:
            self.balance -= amount
            print(f"Withdrawal successful. New balance: ${self.balance:.2f}")

    def update_balance(self):
        # Updating the account balance in the database
        with get_connection() as conn:
            cursor = conn.cursor()
            # Querying the database to update user's balance
            cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (self.balance, self.username))
            conn.commit()

class Assets:
    def view_assets():
        # Retrieving and displaying available assets and their prices
        with get_connection() as conn:
            cursor = conn.cursor()
            # Querying the database to retrieve available assets and their prices
            cursor.execute("SELECT asset_name, price FROM assets")
            assets = cursor.fetchall()
            return "\n".join([f"{name}: ${price}" for name, price in assets])

class Portfolio:
    def view_portfolio(username):
        # Displaying the user's portfolio
        with get_connection() as conn:
            cursor = conn.cursor()
            # Querying the database to retrieve user's portfolio
            cursor.execute("SELECT asset_name, quantity FROM portfolio WHERE username = ?", (username,))
            assets = cursor.fetchall()
            # If the user has available assets in their portfolio
            if assets:
                portfolio_details = [f"{asset_name}: {quantity}" for asset_name, quantity in assets]
                return "\n".join(portfolio_details)
            # If the user has no assets in their portfolio
            else:
                return "Portfolio is empty."

    def buy_assets(username, asset_name, quantity):
        # Processing the purchase of assets for the user
        with get_connection() as conn:
            cursor = conn.cursor()
            # Querying the database to retrieve the asset's price
            cursor.execute("SELECT price FROM assets WHERE asset_name = ?", (asset_name,))
            price_result = cursor.fetchone()
            # If the asset does not exist in the database
            if not price_result:
                return "Error: Asset not found."
            # Calculating the total cost of the purchase
            total_cost = price_result[0] * quantity
            # Querying the database to check if the user has sufficient balance
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            account_result = cursor.fetchone()
            # If the user has sufficient balance
            if account_result and account_result[0] >= total_cost:
                # Calculating the remaining balance after the purchase
                new_balance = account_result[0] - total_cost
                # Updating the user's balance and inserting the purchased assets into the user's portfolio in the database
                cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (new_balance, username))
                cursor.execute("SELECT quantity FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
                portfolio_result = cursor.fetchone()
                # If the asset is already exists in the user's portfolio
                if portfolio_result:
                    new_quantity = portfolio_result[0] + quantity
                    cursor.execute("UPDATE portfolio SET quantity = ? WHERE username = ? AND asset_name = ?", (new_quantity, username, asset_name))
                # If the asset does not exist in the user's portfolio
                else:
                    cursor.execute("INSERT INTO portfolio (username, asset_name, quantity) VALUES (?, ?, ?)", (username, asset_name, quantity))
                # Inserting the transaction history into the transactions table in the database using datetime module
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO transactions (username, asset_name, quantity, action, date) VALUES (?, ?, ?, ?, ?)", (username, asset_name, quantity, "buy", date))
                conn.commit()
                return f"Purchased {quantity} of {asset_name} for ${total_cost:.2f}. Remaining balance: ${new_balance:.2f}"
            # If the user does not have sufficient balance
            else:
                return "Error: Insufficient funds."

    def sell_assets(username, asset_name, quantity):
        # Processing the sale of assets for the user
        with get_connection() as conn:
            cursor = conn.cursor()
            # Querying the database to retrieve the asset's price
            cursor.execute("SELECT quantity FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
            portfolio_result = cursor.fetchone()
            # If the asset is insufficent in the user's portfolio
            if not portfolio_result or portfolio_result[0] < quantity:
                return "Error: Insufficient quantity in portfolio."
            # Querying the database to retrieve the asset's price
            cursor.execute("SELECT price FROM assets WHERE asset_name = ?", (asset_name,))
            price_result = cursor.fetchone()
            # If the asset does not exist in the database
            if not price_result:
                return "Error: Asset price not found."
            # Calculating the total cost of the sale and the remaining quantity in the user's portfolio
            total_value = price_result[0] * quantity
            new_quantity = portfolio_result[0] - quantity
            # If remaining quantity is 0, delete the asset from the user's portfolio
            if new_quantity == 0:
                cursor.execute("DELETE FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
            # If remaining quantity is not 0, update the user's portfolio
            else:
                cursor.execute("UPDATE portfolio SET quantity = ? WHERE username = ? AND asset_name = ?", (new_quantity, username, asset_name))
            # Querying the database to retrieve the user's balance
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            account_result = cursor.fetchone()
            # If the user's balance is found
            if account_result:
                # Calculating the new balance after the sale
                new_balance = account_result[0] + total_value
                # Updating the user's balance in the database
                cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (new_balance, username))
                # Inserting the transaction history into the transactions table in the database using datetime module
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO transactions (username, asset_name, quantity, action, date) VALUES (?, ?, ?, ?, ?)", (username, asset_name, quantity, "sell", date))
                conn.commit()
                return f"Sold {quantity} of {asset_name} for ${total_value:.2f}. New balance: ${new_balance:.2f}"
            # If the user's balance is not found
            else:
                return "Error updating account."

# Creating a construct to start the server and initialise the database
if __name__ == "__main__":
    initialise_database()
    server = Server()
    server.create_server()