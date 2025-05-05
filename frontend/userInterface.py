import sys
import os
import tkinter as tk

# Adds backend directory for retrieval of data
sys.path.append(os.path.abspath('../backend'))

from coinGecko import organize_data, set_selected_coin

#data_date, data_price = organize_data("CryptoPrices_tether.csv")

root = tk.Tk()
root.title("Crypto Analysis")

coin_names = ['bitcoin', 'ethereum', 'tether', 'binance coin', 'solana']

def handle_click(coin_name):
    set_selected_coin(coin_name)
    

# Create and pack buttons
for coin in coin_names:
    button = tk.Button(root, text=coin.title(), width=20, command=lambda c=coin: handle_click(c))
    button.pack(pady=5)
    

# Run the app
root.mainloop()