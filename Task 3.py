import os
import requests
import tkinter as tk
from tkinter import messagebox, ttk
import json

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'YOUR_API_KEY_HERE')  # Secure API Key


def get_stock_data(symbol):
    """Fetch stock data from Alpha Vantage API."""
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'Global Quote' in data and '05. price' in data['Global Quote']:
            return {
                'symbol': data['Global Quote']['01. symbol'],
                'price': float(data['Global Quote']['05. price']),
                'change_percent': float(data['Global Quote']['10. change percent'].strip('%'))
            }
        return None
    except requests.RequestException as e:
        print(f"API error: {e}")
        return None


class Portfolio:
    """Class to manage a stock portfolio."""
    def __init__(self):
        self.stocks = {}  # Store as {symbol: {"quantity": int, "purchase_price": float}}

    def add_stock(self, symbol, quantity):
        """Add stocks to the portfolio."""
        stock_data = get_stock_data(symbol)
        if not stock_data:
            return None

        current_price = stock_data['price']
        if symbol in self.stocks:
            total_quantity = self.stocks[symbol]["quantity"] + quantity
            avg_price = (
                (self.stocks[symbol]["quantity"] * self.stocks[symbol]["purchase_price"] +
                 quantity * current_price) / total_quantity
            )
            self.stocks[symbol] = {"quantity": total_quantity, "purchase_price": avg_price}
        else:
            self.stocks[symbol] = {"quantity": quantity, "purchase_price": current_price}

        return current_price

    def remove_stock(self, symbol, quantity):
        """Remove stocks from the portfolio."""
        if symbol in self.stocks:
            self.stocks[symbol]["quantity"] -= quantity
            if self.stocks[symbol]["quantity"] <= 0:
                del self.stocks[symbol]

    def get_portfolio_value(self):
        """Calculate the total value of the portfolio."""
        total_value = 0
        for symbol, data in self.stocks.items():
            stock_data = get_stock_data(symbol)
            if stock_data:
                total_value += stock_data['price'] * data["quantity"]
        return total_value

    def get_stock_profit(self, symbol):
        """Calculate profit for a specific stock."""
        if symbol in self.stocks:
            stock_data = get_stock_data(symbol)
            if stock_data:
                current_price = stock_data['price']
                purchase_price = self.stocks[symbol]["purchase_price"]
                return (current_price - purchase_price) * self.stocks[symbol]["quantity"]
        return 0

    def save_to_file(self, filename="portfolio.json"):
        """Save the portfolio to a file."""
        with open(filename, "w") as file:
            json.dump(self.stocks, file)

    def load_from_file(self, filename="portfolio.json"):
        """Load the portfolio from a file."""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.stocks = json.load(file)


class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.portfolio = Portfolio()
        self.portfolio.load_from_file()

        # Labels
        tk.Label(root, text="Stock Symbol:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)

        # Entry Fields
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=5)

        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add Stock", command=self.add_stock).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(root, text="Remove Stock", command=self.remove_stock).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(root, text="View Portfolio Value", command=self.view_portfolio_value).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Save Portfolio", command=self.save_portfolio).grid(row=4, column=0, columnspan=2, pady=10)

        # Portfolio Table
        self.tree = ttk.Treeview(root, columns=("Symbol", "Quantity", "Purchase Price"), show="headings", height=8)
        self.tree.heading("Symbol", text="Stock Symbol")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Purchase Price", text="Purchase Price")
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.update_table()

    def add_stock(self):
        """Add a stock to the portfolio."""
        symbol = self.symbol_entry.get().strip().upper()
        try:
            quantity = int(self.quantity_entry.get().strip())
            current_price = self.portfolio.add_stock(symbol, quantity)

            if current_price is not None:
                self.update_table()
                messagebox.showinfo("Success", f"Added {quantity} shares of {symbol}.")
            else:
                messagebox.showwarning("Error", f"Failed to fetch data for {symbol}.")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")

    def remove_stock(self):
        """Remove a stock from the portfolio."""
        symbol = self.symbol_entry.get().strip().upper()
        try:
            quantity = int(self.quantity_entry.get().strip())
            self.portfolio.remove_stock(symbol, quantity)
            self.update_table()
            messagebox.showinfo("Success", f"Removed {quantity} shares of {symbol}.")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")

    def view_portfolio_value(self):
        """View the total portfolio value."""
        value = self.portfolio.get_portfolio_value()
        messagebox.showinfo("Portfolio Value", f"Total portfolio value: ${value:.2f}")

    def save_portfolio(self):
        """Save the portfolio to a file."""
        self.portfolio.save_to_file()
        messagebox.showinfo("Save Portfolio", "Portfolio saved successfully!")

    def update_table(self):
        """Update the table with current portfolio data."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for symbol, data in self.portfolio.stocks.items():
            self.tree.insert("", "end", values=(symbol, data["quantity"], f"${data['purchase_price']:.2f}"))


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()