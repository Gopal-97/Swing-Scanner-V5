def calculate_score(last):

    score = 0

    # Trend
    if last["EMA20"] > last["EMA50"]:
        score += 20

    if last["EMA50"] > last["EMA200"]:
        score += 20

    # RSI
    if 50 <= last["RSI"] <= 70:
        score += 20

    # MACD
    if last["MACD"] > last["MACD_SIGNAL"]:
        score += 20

    # Price
    if last["close"] > last["EMA20"]:
        score += 20

    return score