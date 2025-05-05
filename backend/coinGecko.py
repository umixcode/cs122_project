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

class CryptoAnalysis:
    def __init__(self, selected_coin=None, data = None):
        self.selected_coin = selected_coin
        self.data = data


    # selected_coin = None    
    def set_selected_coin(self, coin_name):
        self.selected_coin = coin_name
        print(self.selected_coin)
        
        #get_data()
        #organize_data(selected_coin)


    def get_selected_coin(self):
        return self.selected_coin

    def set_data(self):
        #
        try:    
            cg = CoinGeckoAPI()
            cg.ping()

            data = cg.get_coin_market_chart_by_id(id=self.selected_coin, vs_currency='usd', days=30)

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
            
            self.data = df

            
            
        except Exception as e:
            print(f"Could not fetch {self.selected_coin}: {e}" )
            return None
        
    
    def get_data(self):
        return self.data

    # Get price, timestamp
    def organize_data(self):
        print(f"In the organized_data function: Selected coin set to: {self.selected_coin}")
        df = self.data
        
        try:
            csv_file = "CryptoPrices_" + self.selected_coin +".csv"
           # data = pd.read_csv(csv_file)
            df.to_csv(csv_file, index=False) # Write csv file for frontend to use 
            print(f"Got the csv file: {csv_file}")
            return csv_file # Returns file name for frontend to use open 
        except Exception as e:
            print(f"Could not open file {csv_file}. Exception: {e}")
