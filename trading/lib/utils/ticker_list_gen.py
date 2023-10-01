import requests
import pandas as pd

def get_sp500_tickers():
    # URL for the S&P 500 constituents list
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Send an HTTP GET request to fetch the data
    response = requests.get(url)

    # Use pandas to read the HTML tables on the page
    tables = pd.read_html(response.text)

    # The first table on the page contains the S&P 500 constituents
    sp500_table = tables[0]

    # Extract the ticker symbols from the table
    sp500_tickers = sp500_table['Symbol'].tolist()

    return sp500_tickers

