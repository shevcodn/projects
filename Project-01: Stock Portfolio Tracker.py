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

    def is_market_open(self, datetime):
        et = pytz.timezone('America/New_York')
        now = datetime.now(et)
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

        if not self.is_market_open(datetime.datetime):
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
            self.holdings[ticker] += qty
        else:
            self.holdings[ticker] = qty
        self.history.add("BUY", ticker, qty, price)

    def sell(self, ticker, qty):
        if ticker not in self.holdings or self.holdings[ticker] < qty:
            raise ValueError("Not enough shares to sell")