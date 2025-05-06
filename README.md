# Crypto Analysis 
### Authors: Umar Memon, Hamza Khan
#### Data Collection and Storage Plan: Umar Memon
#### Analysis and Visualization Role: Hamza Khan
## Project Description 
Crypto Analysis takes data from CoinGecko, a website used to view live prices of top cryptocurrencies via crypto charts. Our project will be a GUI based application, where we pull data from CoinGecko and track historical coin prices within the month. Our project will display a chart that increases/decreases based on the visual trend of certain cryptocurrencies.

## Project Outline 
### Data Collection
- Use CoinGecko to get data for 30 days worth of tracking
- Get price, timestamp, market cap, volume
- Set up API call
- Use Panda to organize data and for the visual analyzer to use 
- Create functionality to save data to CSV file 
### Data Visualization 
- The landing page will prompt the user to select which crypto currency visual trend to check.
- Graph will display visual trends.
- A dropdown menu to display a select different crypto to see visual trends, which will be displayed on a different page.
- A component to compare cryptocurrencies (side-by-side comparison table)

## Future Implementations 
= Option to compare with another coin, which will be displayed on a different page. 
- Integrate a dropdown menu to select a different visualization of a different crypto price, and a button to confirm it or to compare it.  
## Install
conda install pycoingecko 
conda install pandas 
conda install matplotlib

