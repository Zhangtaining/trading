from lib.utils.google_finance_crawler import (
    build_ticker_from_google
)
from lib.utils.modules.ticker import Ticker


class GoogleFinance:

    def get_ticker(self, symbol: str) -> Ticker:
        return build_ticker_from_google(symbol)
