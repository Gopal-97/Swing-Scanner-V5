import pandas as pd

from binance_api import get_usdt_pairs, get_data
from backtest_engine import run_backtest

print("========== BACKTEST V2 ==========")

coins = get_usdt_pairs()

print(f"Total Coins : {len(coins)}")

results = []

for coin in coins:

    print(f"Scanning {coin}...")

    df = get_data(
        coin,
        interval="1day",
        limit=500
    )

    if df is None or len(df) < 250:
        continue

    trades = run_backtest(df)

    if not trades.empty:
        trades["Coin"] = coin
        results.append(trades)

if len(results):
    final_df = pd.concat(results, ignore_index=True)
else:
    final_df = pd.DataFrame()

print("\n========== BACKTEST RESULTS ==========")

if not final_df.empty:
    print(final_df.head(20).to_string(index=False))
else:
    print("No trades found.")

print(f"\nTotal Trades : {len(final_df)}")

final_df.to_csv("backtest_results.csv", index=False)

print("\nSaved : backtest_results.csv")
