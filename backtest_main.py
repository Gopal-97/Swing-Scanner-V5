import pandas as pd

from binance_api import get_usdt_pairs, get_data
from backtest_engine_v3 import run_backtest_v3

print("========== BACKTEST V3 ==========")

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

    trades = run_backtest_v3(df)

    if not trades.empty:
        trades["Coin"] = coin
        results.append(trades)

if len(results):
    final_df = pd.concat(results, ignore_index=True)
else:
    final_df = pd.DataFrame()

print("\n========== BACKTEST REPORT ==========")

if final_df.empty:
    print("No trades found.")
else:

    total = len(final_df)
    wins = len(final_df[final_df["Result"] == "WIN"])
    partial = len(final_df[final_df["Result"] == "PARTIAL WIN"])
    losses = len(final_df[final_df["Result"] == "LOSS"])
    open_trades = len(final_df[final_df["Result"] == "OPEN"])

    print(f"Total Trades : {total}")
    print(f"Wins         : {wins}")
    print(f"Partial Wins : {partial}")
    print(f"Losses       : {losses}")
    print(f"Open Trades  : {open_trades}")

    print("\n========== TOP TRADES ==========")
    print(final_df.head(20).to_string(index=False))

final_df.to_csv("backtest_results.csv", index=False)

print("\nSaved : backtest_results.csv")