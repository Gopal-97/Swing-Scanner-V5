import requests
import pandas as pd

BASE_URL = "https://api.kucoin.com"


def get_usdt_pairs():

    url = BASE_URL + "/api/v2/symbols"

    response = requests.get(url)
    data = response.json()

    pairs = []

    if data["code"] != "200000":
        raise Exception(data)

    for symbol in data["data"]:
        if (
            symbol["quoteCurrency"] == "USDT"
            and symbol["enableTrading"]
        ):
            pairs.append(symbol["symbol"].replace("-", ""))

    return pairs


def get_data(symbol, interval="1day", limit=250):

    # Binance style -> KuCoin style
    kc_symbol = symbol.replace("USDT", "-USDT")

    url = BASE_URL + "/api/v1/market/candles"

    params = {
        "symbol": kc_symbol,
        "type": interval
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["code"] != "200000":
        return None

    candles = data["data"][:limit]

    candles.reverse()

    df = pd.DataFrame(candles, columns=[
        "time",
        "open",
        "close",
        "high",
        "low",
        "volume",
        "turnover"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]

    df["time"] = pd.to_datetime(df["time"].astype(int), unit="s")

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df
