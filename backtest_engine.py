import pandas as pd

from swing_indicators_v3 import add_swing_indicators_v3
from swing_filter_v3 import swing_signal_v3
from swing_risk import calculate_trade


def run_backtest(df):

    df = add_swing_indicators_v3(df)

    trades = []

    # Indicators ko warm-up dene ke liye
    for i in range(200, len(df) - 1):

        last = df.iloc[i]

        signal = swing_signal_v3(last)

        if signal not in ["BUY", "STRONG BUY"]:
            continue

        trade = calculate_trade(
            last["close"],
            last["ATR"]
        )

        trades.append({
            "Time": str(last["time"]),
            "Signal": signal,
            "Entry": trade["Entry"],
            "StopLoss": trade["StopLoss"],
            "Target1": trade["Target1"],
            "Target2": trade["Target2"]
        })

    return pd.DataFrame(trades)