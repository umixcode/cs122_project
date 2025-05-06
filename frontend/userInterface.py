import sys
import os
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd

# Adds backend directory for retrieval of data
sys.path.append(os.path.abspath('../backend'))
#from coinGecko import organize_data, set_selected_coin
from coinGecko import CryptoAnalysis

#data_date, data_price = organize_data("CryptoPrices_tether.csv")

class DataVisualization(CryptoAnalysis):
    def __init__(self, root):
        self.root = root
        self.coin_names = ['bitcoin', 'ethereum', 'tether', 'binance coin', 'solana']

    # When user clicks a button, it activates this function 
    def handle_click(self, coin_name):
        self.main(coin_name) # Main has all the functions 
        self.generate_graph(coin_name)
    
    def generate_graph(self, coin_name):
        csv_file = f"CryptoPrices_{coin_name}.csv"
        
        try:
            df = pd.read_csv(csv_file)
            
            
            
            # Plot data
            plt.figure(figsize = (10, 5))
            plt.plot(df['Date'], df['Price'], label = 'Price')
            
            plt.title(f"{coin_name.title()} Price (Last 30 days)")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.xticks(rotation=45) # Rotates the x-axis labels so the labels do not over lap 
            plt.grid(True)
            plt.tight_layout() # Adjust the spacing of the plot elements to prevent overlapping 
            plt.legend()
            plt.show()
        except Exception as e:
            print(f"File {csv_file} not found: {e}")
    
    

    # Create and pack buttons 
    def widgets(self):
        for coin in self.coin_names:
            button = tk.Button(root, text=coin.title(), width=20, command=lambda c=coin: self.handle_click(c))
            button.pack(pady=5)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualization(root)
    #app.landing_page()
 
    app.widgets()
    root.mainloop()

