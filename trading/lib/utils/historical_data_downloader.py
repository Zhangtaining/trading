import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

start = datetime.datetime(2023, 2, 1)
end = datetime.datetime(2023, 9, 28)

# url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
# s = requests.get(url).content
# companies = pd.read_csv(io.StringIO(s.decode('utf-8')))

# create empty dataframe
stock_final = pd.DataFrame()
# # iterate over each symbol
# for i in Symbols:


# try:
#     # download the stock price
stock = []
stock = yf.download("TSLA", start=start, end=end, progress=False)

# append the individual stock prices
if len(stock) == 0:
    None
else:
    stock['Name'] = "TSLA"
# except Exception:

#     None

print(stock)
