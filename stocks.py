import time, os, glob, ssl, shutil, smtplib, pathlib
from typing import final
import pandas
import yfinance as yf
from get_all_tickers import get_tickers as gt
from prettytable import PrettyTable, from_csv

# Stock groups
banks = ["JPM", "BAC", "WFC", "PNC"]
tech = ["RNG", "DOCU", "ERIC", "NOK", "AMD", "ZM", "CRM", "TEAM", "WORK",
"INTC", "IBM", "VMW", "AVYA", "GDDY", "SNAP", "BABA", "PINS", "DXCM", "OKTA",
"PYPL", "TWLO", "DBX", "KEYS", "COHR", "CTXS", "DLR", "QTS", "SWCH", "CONE", 
"COR", "CCI", "AMT", "NVDA", "NIO", "MA", "VIAV", "LITE"]
covid = ["LOW", "HD", "CLX", "GE"]
food = ["PEP", "KO", "SBUX", "MCD"]
health = ["ABBV", "LLY", "ABT", "NVAX", "CODX", "HCA", "JNJ", "AZN", "PFE", 
"EBS", "BNTX", "QDEL", "RGEN", "GILD", "MRNA", "TEVA"]
gaming = ["EA", "TTWO", "ATVI", "SNE"]
big_tech = ["AAPL", "MSFT", "FB", "TWTR", "NFLX"]

total_stocks = banks + tech + covid + food + health + gaming + big_tech
total = len(banks) + len(tech) + len(covid) + len(food) + len(health) + len(gaming) + len(big_tech)

# Path to store stock info
path = str(pathlib.Path(__file__).parent.absolute())+ "/Stocks"

# Creates new directory
os.mkdir(path)

i = 0
while (i < total):
    stock = total_stocks[i] 
    symbol = yf.Ticker(stock)
    history = symbol.history(period="1y")
    history.to_csv(path + "/" + stock + ".csv")
    i += 1

tickers = (glob.glob(path + "/*.csv"))
new_data = []
current_ticker = 0

while current_ticker < total:
    data = pandas.read_csv(tickers[current_ticker])
    count = 0

    fifty_day_ma = 0
    fifty_day_va = 0

    ten_day_ma = 0

    year_high = 0
    curval = 0
    curvol = 0
    score = 0
    
    while (count <= 251):
        if count >= 202:
            fifty_day_ma += data.iloc[count,4]
            fifty_day_va += data.iloc[count,5]
        
        if count >= 242:
            ten_day_ma += data.iloc[count,4]

        try:
            curval = data.iloc[count,4]
            curvol = data.iloc[count,5]
            if data.iloc[count,2] > year_high:
                year_high = data.iloc[count,2]
        except IndexError:
            break

        count += 1

    name = ((os.path.basename(tickers[current_ticker])).split(".csv")[0])
    ten_day_ma /= 10
    fifty_day_ma /= 50
    fifty_day_va /= 50

    if curvol > fifty_day_va:
        score += 1
    if curval > ten_day_ma:
        score += 1
    if curval > fifty_day_ma:
        score += 1
    if curvol >= (year_high * 0.85):
        score += 1

    curval = "{:.2f}".format(round(curval, 2))
    curvol = round(curvol)
    ten_day_ma = "{:.2f}".format(round(ten_day_ma, 2))
    fifty_day_ma = "{:.2f}".format(round(fifty_day_ma, 2))
    fifty_day_va = round(fifty_day_va)
    year_high = "{:.2f}".format(round(year_high, 2))

    new_data.append([name, curval, curvol, ten_day_ma, fifty_day_ma, fifty_day_va, year_high, score]) 
    current_ticker += 1
df = pandas.DataFrame(new_data, columns = ["Stock", "Current Price", "Volume", "10-Day MA", "50-Day MA", "50-Day Avg Volume", "52-Week High", "Score"])

df.sort_values("Score", inplace = True, ascending = False)
df.to_csv(path + "/Data.csv", index = False)

csv_file = open(path + "/Data.csv")
analyzed_stocks = from_csv(csv_file)

email = """\
Subject: Stock Analysis

Stocks ranked by score:

""" + analyzed_stocks.get_string() + """\


Sent from Python"""

gmail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
gmail.login("INSERT SENDER EMAIL HERE", "INSERT ASSOCIATED PASSWORD")
gmail.sendmail("INSERT SENDER EMAIL HERE", "INSERT RECEIVER EMAIL HERE", email)
gmail.close()

print("Email sent succesfully!")
print(analyzed_stocks)
shutil.rmtree(path)