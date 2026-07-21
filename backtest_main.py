import pandas as pd

from binance_api import get_usdt_pairs
from swing_scanner_v4 import scan_coin_v4

print("========== BACKTEST V1 ==========")

coins = get_usdt_pairs()

print(f"Total Coins : {len(coins)}")

results = []

for coin in coins:

    print(f"Scanning {coin}...")

    data = scan_coin_v4(
        coin,
        interval="1day",
        limit=500
    
    )

    if data is not None:
        results.append(data)

df = pd.DataFrame(results)

print("\n========== RESULTS ==========")

print(df.head(20).to_string(index=False))

print(f"\nTotal Signals : {len(df)}")

df.to_csv("backtest_results.csv", index=False)

print("\nSaved : backtest_results.csv")