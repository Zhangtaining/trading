from typing import Dict, Any


class Ticker:
    def __init__(self, symbol: str, current_price: float = -1.0, prev_close_price: float = -1.0, market_cap: float = -1.0):
        self.symbol = symbol
        # Current price is the price at the moment event in extended hour
        self.current_price = current_price
        # Last close price is the price at previous market closing time.
        self.prev_close_price = prev_close_price
        self.market_cap = market_cap

    def __str__(self):
        return f"""
        Symbol: {self.symbol}
        Current Price: {self.current_price}
        Previous Close Price: {self.prev_close_price}
        Market Cap: {self.market_cap}
        """

    def to_map(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "current_price": self.current_price,
            "prev_close_price": self.prev_close_price,
            "market_cap": self.market_cap,
            "pre_market_gap": (self.current_price - self.prev_close_price) / self.prev_close_price
        }
