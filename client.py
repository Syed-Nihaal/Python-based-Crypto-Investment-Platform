# Importing external modules
from socket import *
from tkinter import *

# Client address configuration
HOST = "127.0.0.1"
PORT = 4000
ADDRESS = (HOST, PORT)

class Client:
    def __init__(self):
        # Initialising the client and connect to the server
        self.socket = None
        self.connect_to_server()

    def connect_to_server(self):
        # Attempting to connect to the server
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(ADDRESS)
            print("Connected to server.")
        # If the connection fails, print an error message
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.socket = None

    def send_request(self, request):
        # Sending a request to the server and returning the response
        if not self.socket:
            self.connect_to_server()
            if not self.socket:
                return "Error: Unable to connect to the server."
        # Sending the request to the server and receiving the response
        try:
            self.socket.send(request.encode())
            response = self.socket.recv(1024).decode()
            return response
        # If there is an error sending or receiving the request, print an error message
        except Exception as e:
            print(f"Error communicating with server: {e}")
            self.socket = None
            return "Error: Lost connection to server."

    def close_connection(self):
        # Closing the connection to the server
        if self.socket:
            self.socket.close()
            print("Disconnected from server.")

class Menu:
    def __init__(self):
        # Initialising the menu and client
        self.client = Client()
        # If the client is unable to connect to the server, exit the program
        if not self.client.socket:
            print("Exiting due to connection issues.")
            exit()
        # Creating the main window
        self.geo = "1366x720+0+0"
        self.root = Tk() 
        self.root.title("Crypto Investment App")
        self.root.geometry(self.geo)
        self.root.configure(bg="#1b4f72")
        # Creating the main window frames
        self.main_menu_frame = Frame(self.root, bg="#1b4f72")
        self.create_account_frame = Frame(self.root, bg="#1b4f72")
        self.login_frame = Frame(self.root, bg="#1b4f72")
        self.logged_in_frame = Frame(self.root, bg="#1b4f72")
        # Creating the label for responses
        self.response_label = Label(self.root, text="", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold"))
        self.response_label.pack()
        # Creating the main menu buttons
        self.create_main_menu()
        self.create_create_account_view()
        self.create_login_view()
        self.create_logged_in_view()
        # Showing the main menu frame
        self.show_frame(self.main_menu_frame)

    def create_main_menu(self):
        # Creating the main menu buttons
        Button(self.main_menu_frame, text="Create Account", bg="#fdfefe", fg="#17202a", font=("Arial", 14, "bold"), command=lambda: self.show_frame(self.create_account_frame)).pack(pady=10)
        Button(self.main_menu_frame, text="Login", bg="#fdfefe", fg="#17202a", font=("Arial", 14, "bold"), command=lambda: self.show_frame(self.login_frame)).pack(pady=10)
        Button(self.main_menu_frame, text="Exit", bg="#d0d3d4", fg="#17202a", font=("Arial", 14, "bold"), command=self.exit_application).pack(pady=10)

    def toggle_password_visibility(self, entry_widget, toggle_button):
        # Toggle between masking and showing the password
        if entry_widget.cget("show") == "*":
            entry_widget.config(show="")  # Show password
            toggle_button.config(text="Hide")  # Update button label
        else:
            entry_widget.config(show="*")  # Mask password
            toggle_button.config(text="Show")  # Update button label

    def create_create_account_view(self):
        # Creating the view for account creation
        # Creating the label and entry for the username
        Label(self.create_account_frame, text="Username:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.username_entry = Entry(self.create_account_frame)
        self.username_entry.pack(pady=2)
        # Creating the label and entry for the password
        Label(self.create_account_frame, text="Password:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        password_frame = Frame(self.create_account_frame, bg="#1b4f72")
        password_frame.pack(pady=2)
        self.password_entry = Entry(password_frame, show="*")
        self.password_entry.pack(side="left", padx=(0, 5))
        toggle_button = Button(password_frame, text="Show", bg="#d0d3d4", fg="#17202a", font=("Arial", 10), width=5, command=lambda: self.toggle_password_visibility(self.password_entry, toggle_button))
        toggle_button.pack(side="right")
        # Creating the label and entry for the initial balance
        Label(self.create_account_frame, text="Initial Balance:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.initial_balance_entry = Entry(self.create_account_frame)
        self.initial_balance_entry.pack(pady=2)
        # Creating the create account button
        Button(self.create_account_frame, text="Create Account", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.create_account_request).pack(pady=10)
        # Creating the back button
        Button(self.create_account_frame, text="Back", bg="#d0d3d4", fg="#17202a", font=("Arial", 12, "bold"),command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=10)

    def create_login_view(self):
        # Creating the view for user login
        # Creating the label and entry for the username
        Label(self.login_frame, text="Username:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.login_username_entry = Entry(self.login_frame)
        self.login_username_entry.pack(pady=5)
        # Creating the label and entry for the password
        Label(self.login_frame, text="Password:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        password_frame = Frame(self.login_frame, bg="#1b4f72")
        password_frame.pack(pady=2)
        self.login_password_entry = Entry(password_frame, show="*")
        self.login_password_entry.pack(side="left", padx=(0, 5))
        toggle_button = Button(password_frame, text="Show", bg="#d0d3d4", fg="#17202a", font=("Arial", 10), width=5, command=lambda: self.toggle_password_visibility(self.login_password_entry, toggle_button))
        toggle_button.pack(side="right")
        # Creating the login button
        Button(self.login_frame, text="Login", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.login_request).pack(pady=10)
        # Creating the back button
        Button(self.login_frame, text="Back", bg="#d0d3d4", fg="#17202a", font=("Arial", 12, "bold"), command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=10)

    def create_logged_in_view(self):
        # Creating the view for logged-in users
        # Creating the buttons for viewing assets, account information, transactions and to log out
        Button(self.logged_in_frame, text="View Available Assets", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.view_assets).pack(pady=10)
        Button(self.logged_in_frame, text="View Account Portfolio", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.view_portfolio).pack(pady=10)
        Button(self.logged_in_frame, text="Deposit", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.deposit).pack(pady=10)
        Button(self.logged_in_frame, text="Withdraw", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.withdraw).pack(pady=10)
        Button(self.logged_in_frame, text="Buy Assets", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.buy_assets).pack(pady=10)
        Button(self.logged_in_frame, text="Sell Assets", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.sell_assets).pack(pady=10)
        Button(self.logged_in_frame, text="Logout", bg="#d0d3d4", fg="#17202a", font=("Arial", 12, "bold"), command=self.logout_request).pack(pady=10)

    def show_frame(self, frame):
        # Showing the specified frame and hide all other frames
        for f in [self.main_menu_frame, self.create_account_frame, self.login_frame, self.logged_in_frame]:
            f.pack_forget()
        # Showing only the selected frame
        frame.pack(fill="both", expand=True)

    def create_account_request(self):
        # Handling account creation request
        # Getting the username, password, and initial balance from the input entries
        username = self.username_entry.get()
        password = self.password_entry.get()
        initial_balance = self.initial_balance_entry.get()
        # If the initial balance is invalid
        if not initial_balance.isdigit():
            self.response_label['text'] = "Error: Initial balance must be a number."
            return
        # If the initial balance is is greater than or equal to 1,000,000
        initial_balance = float(initial_balance)
        if initial_balance >= 1000000:
            self.response_label['text'] = "Error: Invalid amount. User cannot have more than $1,000,000 in their account."
            return
        # If inital balance is valid
        else:
            # Creating a new account with the given information by sending a request to the server and displaying the response
            response = self.client.send_request(f"create_account;{username};{password};{initial_balance}")
            self.response_label['text'] = response

    def login_request(self):
        # Handling login request
        # Getting the username and password from the input entries
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        # Sending request to server to check if the username and password are correct and displaying the response
        response = self.client.send_request(f"login;{username};{password}")
        self.response_label['text'] = response
        # If the login is successful, showing the logged-in view
        if response.startswith("Login successful"):
            self.show_frame(self.logged_in_frame)

    def logout_request(self):
        # Handling logout request
        response = self.client.send_request("logout")
        self.response_label['text'] = response
        # Clearing the login entries
        self.login_username_entry.delete(0, END)
        self.login_password_entry.delete(0, END)
        # Showing the main menu frame
        self.show_frame(self.main_menu_frame)

    def view_assets(self):
        # Sending request to view available assets
        response = self.client.send_request("view_assets")
        # Creating a new window to send request to view available assets and display the response
        self.deposit_window = Toplevel(self.root)
        self.deposit_window.title("View Available Assets")
        self.deposit_window.geo = "400x200+480+60"
        self.deposit_window.geometry(self.deposit_window.geo)
        self.deposit_window.configure(bg="#1b4f72")
        Label(self.deposit_window, text=response, bg="#1b4f72", fg="#fdfefe", font=("Arial", 14, "bold")).pack(pady=10)

    def view_portfolio(self):
        # Getting the username from the input entry and sending request to server and displaying the response
        username = self.login_username_entry.get()
        response = self.client.send_request(f"view_portfolio;{username}")
        # Creating a new window to view user's portfolio
        self.deposit_window = Toplevel(self.root)
        self.deposit_window.title("View Available Assets")
        self.deposit_window.geo = "400x200+480+60"
        self.deposit_window.geometry(self.deposit_window.geo)
        self.deposit_window.configure(bg="#1b4f72")
        Label(self.deposit_window, text=response, bg="#1b4f72", fg="#fdfefe", font=("Arial", 14, "bold")).pack(pady=10)

    def deposit(self):
        # Creating a new window for depositing funds
        self.deposit_window = Toplevel(self.root)
        self.deposit_window.title("Deposit Assets to Account")
        self.deposit_window.geo = "400x200+480+60"
        self.deposit_window.geometry(self.deposit_window.geo)
        self.deposit_window.configure(bg="#1b4f72")
        # Creating a label and entry for the amount to be deposited
        Label(self.deposit_window, text="Amount to Deposit:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.amount_entry = Entry(self.deposit_window)
        self.amount_entry.pack()
        # Creating a button to send the deposit request to the server
        Button(self.deposit_window, text="Deposit", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.deposit_request).pack(pady=10)

    def deposit_request(self):
        # Handling request for deposit
        # Getting the amount to be deposited from the input entry
        amount = self.amount_entry.get()
        # If the amount is invalid
        if not amount.isdigit():
            self.response_label['text'] = "Error: Deposit amount must be a number."
            return
        # Sending request to server and displaying the response
        response = self.client.send_request(f"deposit;{self.login_username_entry.get()};{amount}")
        self.response_label['text'] = response

    def withdraw(self):
        # Creating a new window for withdrawing funds
        self.withdraw_window = Toplevel(self.root)
        self.withdraw_window.title("Withdraw Assets from Account")
        self.withdraw_window.geo = "400x200+480+60"
        self.withdraw_window.geometry(self.withdraw_window.geo)
        self.withdraw_window.configure(bg="#1b4f72")
        # Creating a label and entry for the amount to be withdrawn
        Label(self.withdraw_window, text="Amount to Withdraw:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.amount_entry = Entry(self.withdraw_window)
        self.amount_entry.pack(pady=8)
        # Creating a button to send the withdrawal request to the server
        Button(self.withdraw_window, text="Withdraw", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.withdraw_request).pack(pady=10)

    def withdraw_request(self):
        # Handling request for withdrawal
        # Getting the amount to be withdrawn from the input entry
        amount = self.amount_entry.get()
        # If the amount is invalid
        if not amount.isdigit():
            self.response_label['text'] = "Error: Withdrawal amount must be a number."
            return
        # Sending request to server and displaying the response
        response = self.client.send_request(f"withdraw;{self.login_username_entry.get()};{amount}")
        self.response_label['text'] = response

    def buy_assets(self):
        # Creating a new window for buying assets
        self.buy_assets_window = Toplevel(self.root)
        self.buy_assets_window.title("Buy Assets")
        self.buy_assets_window.geo = "800x600+300+60"
        self.buy_assets_window.geometry(self.buy_assets_window.geo)
        self.buy_assets_window.configure(bg="#1b4f72")
        # Sending request to view available assets
        response = self.client.send_request("view_assets")
        available_assets = response.split("\n")
        # Creating a label to display available assets
        Label(self.buy_assets_window, text="Available Assets:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        # Creating a frame to hold the asset buttons
        asset_buttons_frame = Frame(self.buy_assets_window, bg="#1b4f72")
        asset_buttons_frame.pack()
        # Creating a variable to store the selected asset
        self.selected_asset = StringVar()
        # Creating buttons for each available asset
        for asset in available_assets:
            asset_name, asset_price = asset.split(": ")
            Button(asset_buttons_frame, text=asset_name, bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=lambda asset_name=asset_name: self.select_buying_asset(asset_name)).pack(pady=8)
        # Creating a label to display the selected asset
        self.asset_name_label = Label(self.buy_assets_window, text="Selected Asset: ", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold"))
        self.asset_name_label.pack()
        # Creating a label and entry for the quantity to be bought
        Label(self.buy_assets_window, text="Quantity:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.quantity_entry = Entry(self.buy_assets_window)
        self.quantity_entry.pack()
        # Creating a button to send the buy request to the server
        Button(self.buy_assets_window, text="Buy", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.buy_request).pack(pady=10)

    def select_buying_asset(self, asset_name):
        # Setting the selected asset
        self.selected_asset.set(asset_name)
        # Updating the asset name label
        self.asset_name_label['text'] = f"Selected Asset: {asset_name}"

    def buy_request(self):
        # Handling request for buying assets
        # Getting the asset name and quantity to be bought from the input entries
        asset_name = self.asset_name_label['text'].split(": ")[1]
        quantity = self.quantity_entry.get()
        # If the quantity is invalid
        if not quantity.isdigit():
            self.response_label['text'] = "Error: Quantity must be a number."
            return
        # Sending request to server and displaying the response
        response = self.client.send_request(f"buy_assets;{self.login_username_entry.get()};{asset_name};{quantity}")
        self.response_label['text'] = response

    def sell_assets(self):
        # Creating a new window for selling assets
        self.sell_assets_window = Toplevel(self.root)
        self.sell_assets_window.title("Sell Assets")
        self.sell_assets_window.geo = "800x600+300+60"
        self.sell_assets_window.geometry(self.sell_assets_window.geo)
        self.sell_assets_window.configure(bg="#1b4f72")
        # Sending request to view available assets
        response = self.client.send_request("view_assets")
        available_assets = response.split("\n")
        # Creating a label to display available assets
        Label(self.sell_assets_window, text="Available Assets:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        # Creating a frame to hold the asset buttons
        asset_buttons_frame = Frame(self.sell_assets_window, bg="#1b4f72")
        asset_buttons_frame.pack()
        # Creating a variable to store the selected asset
        self.selected_asset = StringVar()
        # Creating buttons for each available asset
        for asset in available_assets:
            asset_name, asset_price = asset.split(": ")
            Button(asset_buttons_frame, text=asset_name, bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=lambda asset_name=asset_name: self.select_selling_asset(asset_name)).pack(pady=10)
        # Creating a label to display the selected asset
        self.asset_name_label = Label(self.sell_assets_window, text="Selected Asset: ", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold"))
        self.asset_name_label.pack()
        # Creating a label and entry for the quantity to be bought
        Label(self.sell_assets_window, text="Quantity:", bg="#1b4f72", fg="#fdfefe", font=("Arial", 12, "bold")).pack(pady=8)
        self.quantity_entry = Entry(self.sell_assets_window)
        self.quantity_entry.pack()
        # Creating a button to send the sell request to the server
        Button(self.sell_assets_window, text="Sell", bg="#fdfefe", fg="#17202a", font=("Arial", 12, "bold"), command=self.sell_request).pack(pady=10)

    def select_selling_asset(self, asset_name):
        # Setting the selected asset and updating the asset name label
        self.selected_asset.set(asset_name)
        self.asset_name_label['text'] = f"Selected Asset: {asset_name}"

    def sell_request(self):
        # Handling request for selling assets
        # Getting the asset name and quantity to be sold from the input entries
        asset_name = self.asset_name_label['text'].split(": ")[1]
        quantity = self.quantity_entry.get()
        # If the quantity is invalid
        if not quantity.isdigit():
            self.response_label['text'] = "Error: Quantity must be a number."
            return
        # Sending request to server and displaying the response
        response = self.client.send_request(f"sell_assets;{self.login_username_entry.get()};{asset_name};{quantity}")
        self.response_label['text'] = response

    def exit_application(self):
        # Closing the client connection and exiting the application
        self.client.close_connection()
        self.root.destroy()

    def run(self):
        # Starting the Tkinter main loop
        self.root.mainloop()

# Creating a construct to create an instance of the Menu class and run the application
if __name__ == "__main__":
    menu = Menu()
    menu.run()