# Python Stock Analysis

A Python script that analyzes and produce a table containing relevant information of a portfolio of stocks.

### Built With

* [Python3](https://www.python.org/about/)
* [Pandas](https://pandas.pydata.org/)
* [YFinance](https://pypi.org/project/yfinance/)

# Features
* Analyzes portfolio of stocks to see which stocks are above their 10-day moving average, 50-day moving average, 50-day average volume, and are within 15% of their 52-week high
* Produces a table containing Stock Symbol, Current Price, Volume, 10-day MA, 50-day MA, 50-day Avg Volume, 52-Week High and Score for each stock in portfolio
* Sends a copy of information table to your personal email


# Usage
```
~/python-stock-analyzer python3 stocks.py
```