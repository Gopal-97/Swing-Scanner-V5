import pandas as pd

from swing_indicators_v3 import add_swing_indicators_v3
from swing_filter_v3 import swing_signal_v3
from swing_risk import calculate_trade


def run_backtest_v3(df):

    df = add_swing_indicators_v3(df)

    trades = []

    for i in range(200, len(df) - 1):

        candle = df.iloc[i]

        signal = swing_signal_v3(candle)

        if signal not in ["BUY", "STRONG BUY"]:
            continue

        trade = calculate_trade(
            candle["close"],
            candle["ATR"]
        )

        result = "OPEN"
        exit_price = candle["close"]

        for j in range(i + 1, len(df)):

            next_candle = df.iloc[j]

            high = next_candle["high"]
            low = next_candle["low"]

            # Stop Loss
            if low <= trade["StopLoss"]:
                result = "LOSS"
                exit_price = trade["StopLoss"]
                break

            # Target 2
            if high >= trade["Target2"]:
                result = "WIN"
                exit_price = trade["Target2"]
                break

            # Target 1
            if high >= trade["Target1"]:
                result = "PARTIAL WIN"
                exit_price = trade["Target1"]
                break

        pnl = round(
            ((exit_price - trade["Entry"]) / trade["Entry"]) * 100,
            2
        )

        trades.append({
            "Time": str(candle["time"]),
            "Signal": signal,
            "Entry": trade["Entry"],
            "StopLoss": trade["StopLoss"],
            "Target1": trade["Target1"],
            "Target2": trade["Target2"],
            "Exit": exit_price,
            "PnL%": pnl,
            "Result": result
        })

    return pd.DataFrame(trades)
