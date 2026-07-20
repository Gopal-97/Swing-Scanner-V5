import requests
import pandas as pd

BASE_URL = "https://api.bybit.com"


def get_usdt_pairs():

    url = BASE_URL + "/v5/market/instruments-info"

    params = {
        "category": "spot"
    }

    data = requests.get(url, params=params).json()

    pairs = []

    for symbol in data["result"]["list"]:

        if (
            symbol["quoteCoin"] == "USDT"
            and symbol["status"] == "Trading"
        ):
            pairs.append(symbol["symbol"])

    return pairs


def get_data(symbol, interval="D", limit=250):

    interval_map = {
        "1d": "D",
        "1h": "60",
        "4h": "240"
    }

    url = BASE_URL + "/v5/market/kline"

    params = {
        "category": "spot",
        "symbol": symbol,
        "interval": interval_map.get(interval, "D"),
        "limit": limit
    }

    data = requests.get(url, params=params).json()

    candles = data["result"]["list"]

    candles.reverse()

    df = pd.DataFrame(candles, columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "turnover"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]

    df["time"] = pd.to_datetime(df["time"].astype(int), unit="ms")

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df
