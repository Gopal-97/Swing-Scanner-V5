def swing_signal_v3(last):

    score = 0

    # EMA Trend
    if last["EMA20"] > last["EMA50"] > last["EMA200"]:
        score += 1

    # RSI
    if 50 <= last["RSI"] <= 70:
        score += 1

    # MACD
    if last["MACD"] > last["MACD_SIGNAL"]:
        score += 1

    # ADX
    if last["ADX"] >= 25:
        score += 1

    # Volume
    if last["volume"] > last["VOL20"]:
        score += 1

    if score == 5:
        return "STRONG BUY"

    elif score == 4:
        return "BUY"

    elif score == 3:
        return "WATCH"

    else:
        return "IGNORE"