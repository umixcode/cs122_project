import sys
import os
import tkinter as tk

# Adds backend directory for retrieval of data
sys.path.append(os.path.abspath('../backend'))
#from coinGecko import organize_data, set_selected_coin
from coinGecko import CryptoAnalysis

#data_date, data_price = organize_data("CryptoPrices_tether.csv")

class DataVisualization(CryptoAnalysis):
    def __init__(self, root):
        self.root = root
        self.coin_names = ['bitcoin', 'ethereum', 'tether', 'binance coin', 'solana']
        
        
    def landing_page():
        root = tk.Tk()
        root.title("Crypto Analysis")


    def handle_click(self, coin_name):

        self.set_selected_coin(coin_name)
        self.set_data()
        self.get_data()
        self.organize_data()
        

    # Create and pack buttons
    
    def widgets(self):
        for coin in self.coin_names:
            button = tk.Button(root, text=coin.title(), width=20, command=lambda c=coin: handle_click(c))
            button.pack(pady=5)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualization(root)
    root.mainloop()

