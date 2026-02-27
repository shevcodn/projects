import os
import requests
import time
import pytz
import datetime
from dotenv import load_dotenv

price_cache = {}
CACHE_TTL = 3900

FALLBACK_PRICES = {
    "AAPL": 272.84,
    "NVDA": 185.09,
    "TSLA": 408.38,
    "MSFT": 401.86,
    "GOOGL": 308.06,
    "AMZN": 207.95,
    "NFLX": 985.33,
    "META": 657.01,
    "AMD":  203.68,
}

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
        self.balance = 10000.0

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
            return FALLBACK_PRICES.get(ticker)

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
        cost = qty * price
        if cost > self.balance:
            print(f"✗ Insufficient funds. Need ${cost:.2f}, have ${self.balance:.2f}")
            return
        if ticker in self.holdings:
            old_qty = self.holdings[ticker]["qty"]
            old_avg = self.holdings[ticker]["avg_price"]
            new_qty = old_qty + qty
            new_avg = (old_avg * old_qty + price * qty) / new_qty
            self.holdings[ticker] = {"qty": new_qty, "avg_price": new_avg}
        else:
            self.holdings[ticker] = {"qty": qty, "avg_price": price}
        self.history.add("BUY", ticker, qty, price)
        self.balance -= cost
        print(f"✓ Bought {qty} {ticker} @ ${price:.2f} | Balance: ${self.balance:.2f}")


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
        price = self.get_market_price(ticker)
        proceeds = round(price * qty, 2) if price else 0
        self.balance += proceeds
        self.history.add("SELL", ticker, qty, price)
        price_str = f"${price:.2f}" if price else "N/A"
        print(f"✓ Sold {qty} {ticker} @ {price_str} | Balance: ${self.balance:.2f}")


    def portfolio(self):
        print("Current Portfolio:")
        for ticker, data in self.holdings.items():
            qty = data["qty"]
            transactions = self.history.get_for_ticker(ticker)
            total_cost = sum(tx.price * tx.qty for tx in transactions if tx.action == "BUY")
            total_qty = sum(tx.qty for tx in transactions if tx.action == "BUY")
            avg_price = total_cost / total_qty if total_qty > 0 else 0

            price = self.get_market_price(ticker)
            price_str = f"${price:.2f}" if price else "N/A"
            value = round(price * qty, 2) if price else "N/A"
            pnl = round((price - avg_price) * qty, 2) if price else "N/A"
            sign = "+" if isinstance(pnl, float) and pnl >= 0 else ""
            print(f"  {ticker}: {qty} shares | avg ${avg_price:.2f} | now {price_str} | value ${value} | P&L {sign}${pnl}")


    def history_for(self, ticker):
        if ticker not in self.holdings:
            print(f"No history for {ticker}")
            return
        transactions = self.history.get_for_ticker(ticker)
        print(f"Transaction history for {ticker}:")
        for tx in transactions:
            print(f"{tx.action} {tx.qty} shares at ${tx.price:.2f}")

    def top(self, n):
        pnl_list = []
        for ticker, data in self.holdings.items():
            price = self.get_market_price(ticker)
            if price:
                pnl = (price - data["avg_price"]) * data["qty"]
                pnl_list.append((ticker, pnl))
        pnl_list.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\nTop {n} holdings by P&L:")
        for i, (ticker, pnl) in enumerate(pnl_list[:n], 1):
            sign = "+" if pnl >= 0 else ""
            print(f" {i}. {ticker}: {sign}${pnl:.2f}")
        
if __name__ == "__main__":
    p = StockPortfolio()
    print("=" * 55)
    print("  Stock Portfolio Tracker | Balance: $10,000.00")
    print("=" * 55)
    print("Commands: buy TICKER QTY | sell TICKER QTY")
    print("          portfolio | history TICKER | top N | quit")
    print("Available: AAPL NVDA TSLA MSFT GOOGL AMZN META AMD NFLX")
    print("=" * 55)

    while True:
        try:
            cmd = input("\n> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not cmd:
            continue

        action = cmd[0].lower()

        if action == "quit":
            print("Goodbye!")
            break
        elif action == "buy" and len(cmd) == 3:
            price = p.get_market_price(cmd[1].upper())
            if not price:
                print(f"✗ Unknown ticker: {cmd[1].upper()}")
            else:
                p.add(cmd[1].upper(), int(cmd[2]), price)
        elif action == "sell" and len(cmd) == 3:
            p.sell(cmd[1].upper(), int(cmd[2]))
        elif action == "portfolio":
            p.portfolio()
        elif action == "history" and len(cmd) == 2:
            p.history_for(cmd[1].upper())
        elif action == "top" and len(cmd) == 2:
            p.top(int(cmd[1]))
        else:
            print("Unknown command. Try: buy AAPL 5 | sell AAPL 3 | portfolio | history AAPL | top 3 | quit")


