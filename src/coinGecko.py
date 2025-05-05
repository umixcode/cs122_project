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
    # fetch historical price data for a coin
    try:
        # fetch data
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)

        # extract prices data
        prices_data = data.get('prices', [])

        # handle empty response
        if not prices_data:
             print(f"no price data found for {coin_id}")
             return None

        # create a pandas dataframe
        df = pd.DataFrame(prices_data, columns=['timestamp_ms', 'price'])

        # convert unix ms to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp_ms'], unit='ms')

        # prepare data for json (convert datetime to string)
        timestamps = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
        prices = df['price'].tolist()

        # return dict for json response
        return {'timestamps': timestamps, 'prices': prices}

    except Exception as e:
        print(f"error fetching data for {coin_id} using pycoingecko: {e}")
        return None

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

