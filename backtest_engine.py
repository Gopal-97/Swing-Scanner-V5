import pandas as pd

from swing_indicators_v3 import add_swing_indicators_v3
from swing_filter_v3 import swing_signal_v3
from swing_risk import calculate_trade


def run_backtest(df):

    df = add_swing_indicators_v3(df)

    trades = []

    # Indicators warm-up
    for i in range(200, len(df) - 1):

        last = df.iloc[i]

        signal = swing_signal_v3(last)

        if signal not in ["BUY", "STRONG BUY"]:
            continue

        trade = calculate_trade(
            last["close"],
            last["ATR"]
        )

        result = "OPEN"

        for j in range(i + 1, len(df)):

            high = df.iloc[j]["high"]
            low = df.iloc[j]["low"]

            if low <= trade["StopLoss"]:
                result = "LOSS"
                break

            if high >= trade["Target2"]:
                result = "WIN"
                break

            if high >= trade["Target1"]:
                result = "PARTIAL WIN"
                break

        trades.append({
            "Time": str(last["time"]),
            "Signal": signal,
            "Entry": trade["Entry"],
            "StopLoss": trade["StopLoss"],
            "Target1": trade["Target1"],
            "Target2": trade["Target2"],
            "Result": result
        })

    return pd.DataFrame(trades)
