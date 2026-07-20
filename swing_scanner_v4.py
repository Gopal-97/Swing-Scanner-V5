import pandas as pd

from binance_api import get_data
from swing_indicators_v3 import add_swing_indicators_v3
from swing_filter_v3 import swing_signal_v3
from swing_risk import calculate_trade
from swing_score_v2 import calculate_score
from support_resistance_v4 import calculate_support_resistance


def scan_coin_v4(symbol, interval="1d", limit=300):
    try:

        df = get_data(symbol, interval=interval, limit=limit)

        # DEBUG
        print(symbol, len(df) if df is not None else "None")

        if df is None or len(df) < 200:
            return None

        df = add_swing_indicators_v3(df)

        last = df.iloc[-1]

        signal = swing_signal_v3(last)

        trade = calculate_trade(last["close"], last["ATR"])

        score = calculate_score(last)

        sr = calculate_support_resistance(df)

        return {
            "Coin": symbol,
            "Price": round(last["close"], 4),
            "Support": sr["Support"],
            "Resistance": sr["Resistance"],
            "RSI": round(last["RSI"], 2),
            "ADX": round(last["ADX"], 2),
            "Score": score,
            "Signal": signal,
            "Entry": trade["Entry"],
            "StopLoss": trade["StopLoss"],
            "Target1": trade["Target1"],
            "Target2": trade["Target2"],
            "RR": trade["RR"]
        }

    except Exception as e:
        print(f"{symbol}: {e}")
        return None
