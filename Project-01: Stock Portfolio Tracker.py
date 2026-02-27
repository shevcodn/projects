import os
import requests
import time
import pytz
import datetime
from dotenv import load_dotenv

price_cache = {}
CACHE_TTL = 3900

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

class Transactions:
    def __init__(self, action, ticker, qty, price):
        self.action = action
        self.ticker = ticker
        self.qty = qty
        self.price = price
        self.next = None

class TransactionHistory:
    def __init__(self):
        self.head = None

    def add(self, action, ticker, qty, price):
        new_transaction = Transactions(action, ticker, qty, price)
        new_transaction.next = self.head
        self.head = new_transaction

    def get_for_ticker(self, ticker):
        current = self.head
        transaction = []
        while current:
            if current.ticker == ticker:
                transaction.append(current)
            current = current.next
        return transaction
    

class StockPortfolio: 
    def __init__(self):
        self.holdings = {}
        self.history = TransactionHistory()

    def is_market_open(self):
        et = pytz.timezone('America/New_York')
        now = datetime.datetime.now(et)
        if now.weekday() >= 5:
            return False
        market_open = now.replace(hour=9, minute=30, second=0)
        market_close = now.replace(hour=16, minute=0, second=0)
        return market_open <= now <= market_close

    def get_market_price(self, ticker):
        now = time.time()

        if ticker in price_cache:
            price, timestamp = price_cache[ticker]
            if now - timestamp < CACHE_TTL:
                return price

        if not self.is_market_open():
            if ticker in price_cache:
                return price_cache[ticker][0]
            return None

        try:
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
            response = requests.get(url, timeout=5)
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            price_cache[ticker] = (price, now)
            return price
        except Exception:
            if ticker in price_cache:
                return price_cache[ticker][0]
            return None


    def add(self, ticker, qty, price):
        if ticker in self.holdings:
            old_qty = self.holdings[ticker]["qty"]
            old_avg = self.holdings[ticker]["avg_price"]
            new_qty = old_qty + qty
            new_avg = (old_avg * old_qty + price * qty) / new_qty
            self.holdings[ticker] = {"qty": new_qty, "avg_price": new_avg}
        else:
            self.holdings[ticker] = {"qty": qty, "avg_price": price}
        self.history.add("BUY", ticker, qty, price)
        print(f"Bought {qty} shares of {ticker} at ${price:.2f}")


    def sell(self, ticker, qty):
        if ticker not in self.holdings:
            print(f"You don't own {ticker}")
            return
        if self.holdings[ticker]["qty"] < qty:
            print(f"Only have {self.holdings[ticker]['qty']} shares of {ticker}")
            return
        self.holdings[ticker]["qty"] -= qty
        if self.holdings[ticker]["qty"] == 0:
            del self.holdings[ticker]
        self.history.add("SELL", ticker, qty, self.get_market_price(ticker))
        print(f"Sold {qty} shares of {ticker} at ${self.get_market_price(ticker):.2f}")


    def portfolio(self):
        print("Current Portfolio:")
        for ticker, qty in self.holdings.items():
            transactions = self.history.get_for_ticker(ticker)
            total_cost = sum(tx.price * tx.qty for tx in transactions if tx.action == "BUY")
            total_qty = sum(tx.qty for tx in transactions if tx.action == "BUY")
            avg_price = total_cost / total_qty if total_qty > 0 else 0

            price = self.get_market_price(ticker)
            value = price * qty if price else "N/A"
            print(f"{ticker}: {qty} shares, Current price: ${price:.2f} "
                  f"Value: ${value if value != 'N/A' else 'N/A'}")
            pnl = (price - avg_price) * qty if price else "N/A"
            print(f"  P&L: ${pnl if pnl != 'N/A' else 'N/A'}")

