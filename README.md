# Stock Portfolio Tracker

This Python application allows you to manage your stock portfolio, fetch real-time stock data from the Alpha Vantage API, and track the value of your investments. The application provides an intuitive graphical user interface (GUI) using Tkinter, where users can add or remove stocks, view their portfolio value, and save/load the portfolio data.


## Features
- **Add Stock**: Add a stock to the portfolio by specifying its symbol and quantity.
- **Remove Stock**: Remove a specified quantity of stock from the portfolio.
- **View Portfolio Value**: View the total value of the portfolio based on real-time stock prices.
- **Save/Load Portfolio**: Save and load the portfolio data to/from a JSON file.
- **Stock Data Fetching**: Fetch live stock data (current price and change percentage) from the Alpha Vantage API.
- **Portfolio Management**: Keep track of each stock's quantity and purchase price, calculate the profit for each stock, and calculate the total value of the portfolio.
  

## Requirements
- Python 3.x
- `requests` library (for API calls)
- `tkinter` library (for GUI)
- `json` (for saving/loading portfolio data)
- An Alpha Vantage API key (sign up for a free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key))


Install required dependencies:
- pip install requests
   

## Usage
1. Run the application:
   ```
   python stock_portfolio_tracker.py
   ```

2. Use the GUI to:
   - Add stocks by entering their symbol and quantity.
   - Remove stocks from the portfolio.
   - View the current value of the entire portfolio.
   - Save and load your portfolio data.

## Code Overview

### Functions:
- `get_stock_data(symbol)`: Fetches stock data (price and change percentage) from the Alpha Vantage API.
- `Portfolio`: A class that manages the stock portfolio, including adding/removing stocks, calculating portfolio value and stock profits, and saving/loading the portfolio to/from a file.
- `PortfolioApp`: A Tkinter-based GUI class that interacts with the `Portfolio` class, allowing users to manage their portfolio visually.

### API Key:
The application requires an Alpha Vantage API key, which should be set as an environment variable or directly inserted into the `API_KEY` variable.

---
