from typing import Dict
import requests
from bs4 import BeautifulSoup
import logging
from lib.utils.modules.ticker import Ticker

PREVIOUS_PRICE = "Previous close"
DAY_RANGE = "Day range"
YEAR_RANGE = "Year range"
MARKET_CAP = "Market cap"
AVG_VOLUME = "Avg volume"
DIVIDEND_YIELD = "Dividend yield"


def build_nsdq_url(symbol: str) -> str:
    return f"https://www.google.com/finance/quote/{symbol.upper()}:NASDAQ"


def build_nyse_url(symbol: str) -> str:
    return f"https://www.google.com/finance/quote/{symbol.upper()}:NYSE"


def get_raw_response_from_google(symbol: str) -> str:
    # This function will help to generate the raw response from the web
    try:
        nsdq_url = build_nsdq_url(symbol)
        response = requests.get(nsdq_url)
        assert (response.status_code == 200)
        if "We couldn't find any match for your search" in response.text:
            nyse_url = build_nyse_url(symbol)
            response = requests.get(nyse_url)
            assert (response.status_code == 200)
        return response.text
    except:
        logging.error(
            f"Webv request failed with status code: {response.status_code}")
        return ""


def extract_price_number(price_tag: BeautifulSoup) -> str:
    price = price_tag.text.strip()
    return float(price.replace('$', '').replace(',', ''))


def _magnitude_value_to_number(mag_value: str) -> float:
    mag_map = {
        "K": 1000,
        "M": 1000000,
        "B": 1000000000,
        "T": 1000000000000,
    }
    mag_unit = mag_value[-1]
    value = mag_value[0:-1]
    multiplier = 1
    if mag_unit in mag_map:
        multiplier = mag_map[mag_unit]
    return float(value) * multiplier


def _fetch_current_price(soup: BeautifulSoup) -> float:
    current_prices = soup.find_all("div", {"class": "YMlKec fxKbKc"})
    if len(current_prices) == 0:
        logging.error(f"Failed fetch the price")
        return -1
    return extract_price_number(current_prices[-1])


def _fetch_all_info_in_card(soup: BeautifulSoup) -> float:
    card_sp = soup.find("div", {"class": "eYanAe"})
    cards = card_sp.find_all("div", {"class": "gyFHrc"})
    res = {}
    for card in cards:
        item_name = card.find("div", {"class": "mfs7Fc"}).text.strip()
        item_value = card.find("div", {"class": "P6K39c"}).text.strip()
        res[item_name] = item_value
    return res


def build_ticker_from_google(symbol: str) -> str:
    try:
        response_text = get_raw_response_from_google(symbol)

        soup = BeautifulSoup(response_text, 'html.parser')

        current_price = _fetch_current_price(soup)
        cards_info = _fetch_all_info_in_card(soup)
        prev_close_price = get_previous_price(cards_info)
        market_cap = get_market_cap(cards_info)
        return Ticker(symbol=symbol, current_price=current_price, prev_close_price=prev_close_price, market_cap=market_cap)
    except:
        logging.error(f"Error happened during fetch the ticker info")
        return None


def get_previous_price(card_map: Dict[str, str]) -> float:
    previous_price_value = card_map[PREVIOUS_PRICE]
    return float(previous_price_value.replace('$', '').replace(',', ''))


def get_market_cap(card_map: Dict[str, str]) -> float:
    market_value_str = card_map[MARKET_CAP]
    return _magnitude_value_to_number(market_value_str.replace(" USD", ""))
