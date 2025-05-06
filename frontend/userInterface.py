import sys
import os
import tkinter as tk
from tkinter import ttk 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Get the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the backend directory
backend_path = os.path.join(script_dir, '..', 'backend')
# Adds backend directory for retrieval of data
sys.path.append(backend_path)
#from coinGecko import organize_data, set_selected_coin
from coinGecko import CryptoAnalysis

#data_date, data_price = organize_data("CryptoPrices_tether.csv")

class DataVisualization(CryptoAnalysis):
    def __init__(self, root):
        # initialize the CryptoAnalysis parent class
        super().__init__() # calls __init__ from CryptoAnalysis
        self.root = root
        # set window title
        self.root.title("Crypto Analysis") 
        self.coin_names = ['bitcoin', 'ethereum', 'tether', 'binance coin', 'solana']
        # string variable to hold the selected coin name (for analysis)
        self.selected_coin_var = tk.StringVar()
        # string variable to hold the coin to compare against
        self.compare_coin_var = tk.StringVar() 
        # create the widgets upon initialization
        self.widgets()
        
        
    # landing_page method is not needed since __init__ handles setup
    # def landing_page():
    #     root = tk.Tk()
    #     root.title("Crypto Analysis")


    def handle_click(self, coin_name):
        # this function is called when a button is clicked
        print(f"Fetching data for: {coin_name}") # print statement to check if button click works
        self.set_selected_coin(coin_name)
        self.set_data() # fetches data and stores in self.data
        # return the fetched dataframe
        df = self.get_data()
        # check if data fetching failed (get_data might return None)
        if df is None:
            print(f"Failed to get data for {coin_name}")
            return None
        # Ensure 'Price' column is numeric
        try:
            df['Price'] = pd.to_numeric(df['Price'])
        except KeyError:
            print("Error: 'Price' column not found in DataFrame.")
            return None
        except ValueError:
            print("Error: Could not convert 'Price' column to numeric.")
            return None
            
        return df
        

    # Create and pack widgets (label, dropdown, button)
    
    def widgets(self):
        # create a label
        label = tk.Label(self.root, text="Select Cryptocurrency:")
        label.pack(pady=5)

        # create a dropdown (combobox)
        coin_combobox = ttk.Combobox(self.root, textvariable=self.selected_coin_var, values=self.coin_names, width=18)
        # set default value
        if self.coin_names:
            self.selected_coin_var.set(self.coin_names[0]) # default to the first coin
        coin_combobox.pack(pady=5)

        # create an analyze button
        analyze_button = tk.Button(self.root, text="Analyze Data", width=20, command=self.trigger_analysis)
        analyze_button.pack(pady=5) # reduced padding

        # --- Widgets for Comparison ---
        # create a label for the comparison dropdown
        compare_label = tk.Label(self.root, text="Compare with:")
        compare_label.pack(pady=(10, 0)) # add padding top

        # create the second dropdown (combobox) for comparison
        compare_combobox = ttk.Combobox(self.root, textvariable=self.compare_coin_var, values=self.coin_names, width=18)
        # set default value (optional, maybe different from the first one)
        if len(self.coin_names) > 1:
            # default to the second coin if available
            self.compare_coin_var.set(self.coin_names[1]) 
        compare_combobox.pack(pady=5)

        # create a compare button
        compare_button = tk.Button(self.root, text="Compare Selected Coins", width=20, command=self.trigger_comparison)
        compare_button.pack(pady=10)

    def trigger_analysis(self):
        # get the selected coin from the combobox variable
        coin_name = self.selected_coin_var.get()
        if coin_name:
            print(f"Analyze button clicked for: {coin_name}")
            # call handle_click to get the dataframe
            df = self.handle_click(coin_name)

            # proceed only if data was fetched successfully
            if df is not None:
                # perform analysis (ensure this block is correctly indented)
                analysis_results = self.analyze_data(df)
                print("Analysis Results:", analysis_results)
                # check if analysis was successful before plotting
                if analysis_results:
                    # call visualization
                    self.plot_data(df, analysis_results)
                else:
                    print("Analysis failed, skipping plot.")
            else:
                # explicit message when data fetching fails
                print("Data fetching failed, skipping analysis and plot.") 

        else:
            print("No coin selected.")

    def analyze_data(self, df):
        # calculate basic statistics and linear trend
        try:
            # ensure the dataframe isn't empty and price column exists
            if df.empty or 'Price' not in df.columns:
                print("DataFrame is empty or 'Price' column missing for analysis.")
                return None
            
            prices = df['Price'].values # get prices as numpy array
            mean_price = np.mean(prices)
            min_price = np.min(prices)
            max_price = np.max(prices)

            # --- Trend Calculation ---
            # create numerical indices for dates (0, 1, 2...)
            x_indices = np.arange(len(df))
            # calculate linear trend (degree 1 polynomial fit)
            # polyfit returns [slope, intercept]
            slope, intercept = np.polyfit(x_indices, prices, 1)


            # return results as dictionary
            results = {
                'mean': mean_price,
                'min': min_price,
                'max': max_price,
                'trend_slope': slope,      # added slope
                'trend_intercept': intercept # added intercept for plotting
            }
            return results
            
        except Exception as e:
            # handle potential errors during analysis (e.g., non-numeric data despite earlier check)
            print(f"Error during data analysis: {e}")
            tk.messagebox.showerror("Analysis Error", f"Could not analyze data.\nError: {e}")
            return None

    def plot_data(self, df, analysis_results):
        # create a new top-level window for the plot
        plot_window = tk.Toplevel(self.root)
        coin_title = self.selected_coin.title() if self.selected_coin else "Crypto"
        plot_window.title(f"{coin_title} Price Trend")

        # --- plotting logic ---
        try:
            # create a matplotlib figure and axes
            fig, ax = plt.subplots(figsize=(8, 5)) # adjusted figure size

            # plot the price data
            # convert date strings to datetime objects for better plotting
            # indices for trend calculation
            dates = pd.to_datetime(df['Date'])
            prices = df['Price']
            ax.plot(dates, prices, label='Price', marker='.', linestyle='-') # added marker

            # --- Trend Line Plotting ---
            # get trend details from analysis results
            slope = analysis_results.get('trend_slope')
            intercept = analysis_results.get('trend_intercept')
            
            if slope is not None and intercept is not None:
                # generate x values (indices) for the trend line
                x_trend = np.arange(len(df))
                # calculate y values for the trend line
                y_trend = slope * x_trend + intercept
                # plot the trend line
                ax.plot(dates, y_trend, label=f'Trend (Slope: {slope:.2f})', linestyle='--', color='red')
                # add legend to show labels for price and trend
                ax.legend()


            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            mean_price = analysis_results.get('mean', 'N/A')
            # format mean price for title
            mean_price_str = f"{mean_price:.2f}" if isinstance(mean_price, (int, float)) else "N/A"
            ax.set_title(f"{coin_title} Price (30 Days)\nMean: ${mean_price_str}")

            # improve date formatting on x-axis
            plt.xticks(rotation=45, ha='right')
            ax.xaxis.set_major_locator(plt.MaxNLocator(10)) # show fewer date labels
            fig.tight_layout() # adjust plot to prevent labels overlapping

            # --- Embedding in Tkinter ---
            # embed the plot in the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            # pack the canvas widget *after* the toolbar and stats frame are set up for the bottom
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # add the matplotlib navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, plot_window)
            toolbar.update()
            # pack the toolbar *before* the stats frame
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)

            # --- Displaying Stats Text ---
            # display analysis results as text
            stats_frame = tk.Frame(plot_window)
            # pack the stats frame at the bottom, it will appear above the toolbar
            stats_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5) 
            min_price = analysis_results.get('min', 'N/A')
            max_price = analysis_results.get('max', 'N/A')
            trend_slope_str = f"{slope:.4f}" if slope is not None else "N/A" # format slope
            min_str = f"{min_price:.2f}" if isinstance(min_price, (int, float)) else "N/A"
            max_str = f"{max_price:.2f}" if isinstance(max_price, (int, float)) else "N/A"

            # update stats label to include trend slope
            stats_label = tk.Label(stats_frame, text=f"Min: ${min_str} | Max: ${max_str} | Trend Slope: {trend_slope_str}")
            stats_label.pack()
            
        except Exception as e:
            # show error message if plotting fails
            print(f"Error plotting data: {e}")
            tk.messagebox.showerror("Plot Error", f"Could not plot data for {coin_title}.\nError: {e}", parent=plot_window)

    def trigger_comparison(self):
        # get the names of the two coins selected
        coin1_name = self.selected_coin_var.get()
        coin2_name = self.compare_coin_var.get()

        # basic validation
        if not coin1_name or not coin2_name:
            print("Please select two coins to compare.")
            tk.messagebox.showwarning("Selection Missing", "Please select two coins to compare.")
            return
        
        if coin1_name == coin2_name:
            print("Please select two *different* coins to compare.")
            tk.messagebox.showwarning("Selection Error", "Please select two *different* coins to compare.")
            return
        
        print(f"Compare button clicked for: {coin1_name} vs {coin2_name}")
        # fetch data for the first coin
        df1 = self.handle_click(coin1_name)
        # fetch data for the second coin
        df2 = self.handle_click(coin2_name)

        # check if both dataframes were fetched successfully
        if df1 is not None and df2 is not None:
            # call the comparison plotting function
            self.plot_comparison(coin1_name, df1, coin2_name, df2)
        else:
            print("Failed to fetch data for one or both coins for comparison.")
            tk.messagebox.showerror("Data Error", "Could not fetch data for one or both selected coins.")

    def plot_comparison(self, coin1_name, df1, coin2_name, df2):
        # create a new top-level window for the comparison plot
        comp_window = tk.Toplevel(self.root)
        title1 = coin1_name.title()
        title2 = coin2_name.title()
        comp_window.title(f"Comparison: {title1} vs. {title2}")

        try:
            # create figure and axes
            fig, ax = plt.subplots(figsize=(8, 5))

            # plot data for coin 1
            dates1 = pd.to_datetime(df1['Date'])
            prices1 = df1['Price']
            ax.plot(dates1, prices1, label=title1, marker='.', linestyle='-')

            # plot data for coin 2 on the same axes
            dates2 = pd.to_datetime(df2['Date'])
            prices2 = df2['Price']
            # use a different color for the second line
            ax.plot(dates2, prices2, label=title2, marker='.', linestyle='-', color='green') 
            
            # add labels, title, legend
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.set_title(f"{title1} vs. {title2} Price (30 Days)")
            ax.legend() # display legend to identify lines

            # formatting
            plt.xticks(rotation=45, ha='right')
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))
            fig.tight_layout()

            # embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=comp_window)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # add toolbar
            toolbar = NavigationToolbar2Tk(canvas, comp_window)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        except Exception as e:
            print(f"Error plotting comparison: {e}")
            tk.messagebox.showerror("Plot Error", f"Could not plot comparison data.\nError: {e}", parent=comp_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualization(root)
    # app.widgets() called in __init__ so no need to call here
    root.mainloop()

