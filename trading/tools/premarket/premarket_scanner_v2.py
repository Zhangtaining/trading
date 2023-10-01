from lib.google_finance import GoogleFinance
from lib.utils.ticker_list_gen import get_sp500_tickers
import pandas as pd
import argparse
import smtplib


def get_stock_scanner_results() -> pd.DataFrame:
    sp500_symbols = get_sp500_tickers()

    google_finance = GoogleFinance()

    sp500_tickers = [google_finance.get_ticker(
        symbol) for symbol in sp500_symbols]

    ticker_info_df = pd.DataFrame([ticker.to_map()
                                  for ticker in sp500_tickers if ticker != None])
    return ticker_info_df


def fetch_premarket_gap_up(market_data: pd.DataFrame, minMarketCap: float, minGap: float):
    filtered_data = market_data.loc[(market_data['market_cap'] > minMarketCap) & (
        market_data['pre_market_gap'] > minGap)]
    return filtered_data.sort_values('pre_market_gap', ascending=False).head(20).sort_values('market_cap', ascending=False)


def notify_by_mail(market_data: pd.DataFrame) -> None:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("zcao1208@gmail.com", "jnqfxslwqqjyhoei")

    message = market_data.to_markdown()
    s.sendmail("zcao1208@gmail.com", "caozhongli1208@gmail.com", message)
    s.quit()


def main():
    parser = argparse.ArgumentParser(
        prog='Premarket Scanner',
        description='Scan Premarket Top Movers',)
    parser.add_argument('--min_market_cap', dest='minMarketCap',
                        type=float, default=10000000000.0)
    parser.add_argument('--min_gap', dest='minGap', type=float, default=0.02)

    args = parser.parse_args()

    market_data = get_stock_scanner_results()
    desired_data = fetch_premarket_gap_up(
        market_data, args.minMarketCap, args.minGap)
    print(desired_data)
    notify_by_mail(desired_data)


if __name__ == "__main__":
    main()
