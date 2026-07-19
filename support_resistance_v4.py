def calculate_support_resistance(df):

    support = round(df["low"].tail(20).min(), 4)

    resistance = round(df["high"].tail(20).max(), 4)

    return {
        "Support": support,
        "Resistance": resistance
    }