def calculate_trade(price, atr):
    entry = round(price, 4)

    stop_loss = round(price - (2 * atr), 4)

    target1 = round(price + (2 * atr), 4)

    target2 = round(price + (4 * atr), 4)

    risk = round(entry - stop_loss, 4)
    reward = round(target1 - entry, 4)

    rr = round(reward / risk, 2) if risk > 0 else 0

    return {
        "Entry": entry,
        "StopLoss": stop_loss,
        "Target1": target1,
        "Target2": target2,
        "RR": rr
    }