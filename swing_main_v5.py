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

buy_df = buy_df.head(10)

buy_df.to_csv("swing_signals_v5.csv", index=False)

print("\n========== TOP SWING V5 SIGNALS ==========")
print(buy_df.head(20).to_string(index=False))

if len(buy_df) == 0:
    send_telegram_message(
        "📉 Swing Scanner V5\n\nNo BUY signal found today."
    )
else:
    msg = "🚀 Swing Scanner V5\n\n"

    for _, row in buy_df.head(10).iterrows():
        msg += (
            f"📈 {row['Coin']}\n"
            f"Signal: {row['Signal']}\n"
            f"Score: {row['Score']}\n"
            f"Entry: {row['Entry']}\n"
            f"SL: {row['StopLoss']}\n"
            f"T1: {row['Target1']}\n"
            f"T2: {row['Target2']}\n\n"
        )

    send_telegram_message(msg)

print(f"\nTotal Signals : {len(buy_df)}")
print("\nSaved : swing_signals_v5.csv")
