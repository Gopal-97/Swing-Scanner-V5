import ta


def add_swing_indicators_v3(df):

    # EMA
    df["EMA20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["EMA200"] = ta.trend.ema_indicator(df["close"], window=200)

    # RSI
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)

    # MACD
    macd = ta.trend.MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # ATR
    atr = ta.volatility.AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    # ADX
    adx = ta.trend.ADXIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["ADX"] = adx.adx()

    # 20-Day Average Volume
    df["VOL20"] = df["volume"].rolling(20).mean()

    return df