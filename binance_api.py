import requests
import pandas as pd

BASE_URL = "https://api.binance.com"

def get_usdt_pairs():

    url = BASE_URL + "/api/v3/exchangeInfo"

    data = requests.get(url).json()
    print(data)

    pairs = []

    for symbol in data["symbols"]:

        if (
            symbol["quoteAsset"] == "USDT"
            and symbol["status"] == "TRADING"
            and symbol["isSpotTradingAllowed"]
        ):
            pairs.append(symbol["symbol"])

    return pairs


def get_data(symbol, interval="1d", limit=250):

    url = BASE_URL + "/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades",
        "buy_base",
        "buy_quote",
        "ignore"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]

    df["time"] = pd.to_datetime(df["time"], unit="ms")

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df
