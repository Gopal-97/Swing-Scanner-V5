import pandas as pd

from binance_api import get_usdt_pairs
from swing_scanner_v4 import scan_coin_v4
from telegram_v5 import send_telegram_message

results = []

coins = get_usdt_pairs()

print(f"Scanning {len(coins)} coins...")

for coin in coins:
    data = scan_coin_v4(coin)

    if data is not None:
        results.append(data)

df = pd.DataFrame(results)

print("\n========== DEBUG ==========")
print("Columns:", list(df.columns))
print("Total Results:", len(df))
print(df.head())
print("===========================\n")

if df.empty or "Signal" not in df.columns:
    print("❌ No valid scan results found.")

    send_telegram_message(
        "⚠️ Swing Scanner V5\n\nNo valid scan results generated."
    )

    exit()

buy_df = df[df["Signal"].isin(["BUY", "STRONG BUY"])]

buy_df = buy_df.sort_values(
    by=["Score", "ADX", "RR"],
    ascending=[False, False, False]
)

# Telegram me sirf Top 10
buy_df = buy_df.head(10)

# CSV me Top 10 save
buy_df.to_csv("swing_signals_v5.csv", index=False)

print("\n========== TOP SWING V5 SIGNALS ==========")
print(buy_df.to_string(index=False))

if len(buy_df) == 0:
    send_telegram_message(
        "📉 Swing Scanner V5\n\nNo BUY signal found today."
    )
else:
    msg = "🏆 TOP 10 SWING PICKS\n\n"

    for _, row in buy_df.iterrows():

        emoji = "🟢" if row["Signal"] == "STRONG BUY" else "🟡"

        msg += (
            f"📈 {row['Coin']}\n"
            f"{emoji} {row['Signal']}\n"
            f"⭐ Score : {row['Score']}\n"
            f"📊 ADX   : {row['ADX']}\n"
            f"⚖️ RR    : {row['RR']}\n"
            f"💰 Entry : {row['Entry']}\n"
            f"🛑 SL    : {row['StopLoss']}\n"
            f"🎯 Target 1 : {row['Target1']}\n"
            f"🎯 Target 2 : {row['Target2']}\n"
            f"━━━━━━━━━━━━\n\n"
        )

    send_telegram_message(msg)

print(f"\nTotal Signals : {len(buy_df)}")
print("\nSaved : swing_signals_v5.csv")