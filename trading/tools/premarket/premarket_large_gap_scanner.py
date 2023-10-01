from tradingview_screener import get_scanner_data, Scanner


def pick_premarket_top_gainer(config=None):
    top_gainers = Scanner.premarket_gainers.get_data()
    return top_gainers.loc[(top_gainers['market_cap_basic'] > 1000000000) & (top_gainers['premarket_change'] > 2) & (top_gainers['volume'] > 20000)]
    
picked_stock_today = pick_premarket_top_gainer()
print(picked_stock_today)
