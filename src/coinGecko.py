'''
gets historical prices over the last 30 days for specified coins.

coins:

bitcoin (btc)

etherum (eth)

tether (usdt)

binance coin (bnb)

solana (sol)

'''

from pycoingecko import CoinGeckoAPI
# from datetime import datetime # not needed
import pandas as pd

# initialize the client
cg = CoinGeckoAPI()

def fetch_historical_data(coin_id, days=30, currency='usd'):
    # fetches historical price data for a given coin id using pycoingecko
    try:
        # fetch data for the specific coin_id
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)

        # extract timestamps and prices
        prices_data = data.get('prices', [])

        if not prices_data: # handle case where no price data is returned
             print(f"no price data found for {coin_id}")
             return None

        # prepare data for charting libraries
        # timestamps are unix ms, prices are in the specified currency
        timestamps = [item[0] for item in prices_data]
        prices = [item[1] for item in prices_data]

        # return data suitable for json serialization
        return {'timestamps': timestamps, 'prices': prices}

    except Exception as e:
        # basic error handling for api call issues
        print(f"error fetching data for {coin_id} using pycoingecko: {e}")
        return None # return none on error

# --- commented out example usage ---
# if __name__ == '__main__':
#     # example usage:
#     btc_data = fetch_historical_data('bitcoin')
#     if btc_data:
#         # print(btc_data)
#         print(f"fetched {len(btc_data['prices'])} data points for bitcoin.")
#         # further processing or saving could go here
#     else:
#         print("failed to fetch bitcoin data.")

