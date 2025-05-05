'''
Gets 5 of the most popular crypto currency and its historical prices over the last 30 days 

Coins: 

Bitcoin (BTC)

Ethereum (ETH)

Tether (USDT)

Binance Coin (BNB)

Solana (SOL)

'''

from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd 

selected_coin = None    
def set_selected_coin(coin_name):
    global selected_coin
    selected_coin = coin_name
    print(f"Selected coin set to: {selected_coin}")
    get_data()


def get_selected_coin():
    return selected_coin

def get_data():
    try:    
        cg = CoinGeckoAPI()
        cg.ping()

        data = cg.get_coin_market_chart_by_id(id=selected_coin, vs_currency='usd', days=30)

        dates = []
        prices = []

        for i in data['prices']:
            timestamp = i[0] / 1000 # gets date
            date = datetime.fromtimestamp(timestamp).date().isoformat() # format date
            price = i[1] # get price
            
            dates.append(date)
            prices.append(price)
            
        # Create panda dataframe 
        df = pd.DataFrame({
            'Date':dates,
            'Price':prices
        })

        csv_file = df.to_csv('CryptoPrices_'+selected_coin+'.csv')
        
    except Exception as e:
        print(f"Could not fetch {selected_coin}: {e}" )
        return None
    
        

# Get price, timestamp
def organize_data(selected_coin):
    data = pd.read_csv(selected_coin)
    # Column 1: date
    # Column 2: Price
    data_date = data['Date']
    data_price = data['Price']
    return data_date, data_price


# gd = get_data()
# organize_data(selected_coin = "CryptoPrices_tether.csv")