<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=18&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=600&lines=Portfolio+Projects;Python+%C2%B7+Rich+%C2%B7+Alpha+Vantage+%C2%B7+FastAPI;Built+during+1000-task+curriculum" alt="Typing SVG" />

### Denis Shevchenko · [shevcodn.dev](https://shevcodn.dev)

[![Python](https://img.shields.io/badge/Python-3.12-00ff88?style=flat-square&logo=python&logoColor=black)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active_Development-00ff88?style=flat-square)](https://github.com/shevcodn/projects)
[![Projects](https://img.shields.io/badge/Projects-2_of_7-00ff88?style=flat-square)](https://github.com/shevcodn/projects)

</div>

---

## Projects

| # | Project | Stack | Try it | Status |
|---|---------|-------|--------|--------|
| 01 | [Stock Portfolio Tracker](https://github.com/shevcodn/projects) | Python · Alpha Vantage API · LinkedList · HashMap | [▶ Live demo](https://shevcodn.dev/#project-01) | ✅ Done |
| 02 | [TradeLedger](https://github.com/shevcodn/tradeledger) | Python · Rich · Alpha Vantage · LinkedList · Heap | [▶ Live demo](https://shevcodn.dev/#project-02) | ✅ Done |
| 03 | MarketPulse | WebSockets · Redis · React | — | 🔜 p800 |
| 04 | DeployKit | Docker · GitHub Actions · Railway | — | 🔜 p900 |
| 05 | AuthVault | JWT · OAuth · Railway deploy | — | 🔜 p960 |
| 06 | WealthTrack | FastAPI · PostgreSQL · Docker | — | 🔜 p980 |
| 07 | PortfolioOS | TBD | — | 🔜 p1000 |

---

## Project-01: Stock Portfolio Tracker

> **Python CLI app** — track your stock portfolio in the terminal with real-time prices.

```
Stack:   Python · Alpha Vantage API · LinkedList · HashMap
Balance: $10,000 virtual
Tickers: AAPL · NVDA · TSLA · MSFT · GOOGL · AMZN · META · AMD · NFLX
```

### Features

| Command | Description |
|---------|-------------|
| `buy TICKER QTY` | Buy shares at real-time market price |
| `sell TICKER QTY` | Sell with automatic P&L calculation |
| `portfolio` | Full table: avg price · current price · value · P&L |
| `history TICKER` | Transaction history via LinkedList |
| `top N` | Top N positions ranked by profit |

### Data Structures

- **HashMap** — `O(1)` lookup for holdings by ticker
- **LinkedList** — transaction history, newest → oldest

### Quick Start (local)

```bash
git clone https://github.com/shevcodn/projects
cd projects/stock-portfolio-tracker
cp .env.example .env
pip install -r ../requirements.txt
python main.py
```

> **Free API key:** [alphavantage.co](https://www.alphavantage.co/support/#api-key) — 30 seconds to get

### Try it live

**[▶ shevcodn.dev/#project-01](https://shevcodn.dev/#project-01)** — interactive terminal, no install needed


---

<div align="center">

*Built during p1→p1000 Python engineering curriculum · Toronto 2026*

[\![Website](https://img.shields.io/badge/shevcodn.dev-00ff88?style=flat-square&logo=vercel&logoColor=black)](https://shevcodn.dev)
[\![Full Roadmap](https://img.shields.io/badge/Full_Roadmap-all_7_projects-00ff88?style=flat-square&logo=github&logoColor=black)](https://github.com/shevcodn/roadmap)

</div>
