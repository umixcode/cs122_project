from flask import Flask, render_template, jsonify
# import os # not needed

# debug path checks (commented out)
# app_dir = ...
# code_dir_path = ...
# init_file_path = ...
# print("--- path check debug ---")
# ...
# print("--- end path check debug ---")

# import local function
from src.coinGecko import fetch_historical_data

app = Flask(__name__) # create flask app

# --- flask routes --- 

# home page route
@app.route('/')
def index():
    # render index.html
    return render_template('index.html')

# comparison page route
@app.route('/compare')
def compare():
    # render compare.html
    return render_template('compare.html')

# --- api endpoint for chart data --- 
@app.route('/api/chart_data/<string:coin_id>')
def get_chart_data(coin_id):
    # fetch historical data for the specified coin
    # print(f"fetching data for coin: {coin_id}") # optional log
    data = fetch_historical_data(coin_id) # call local function
    if data:
        # return json data
        return jsonify(data)
    else:
        # return error on failure
        return jsonify({"error": f"could not fetch data for {coin_id}"}), 404

# run app directly
if __name__ == '__main__':
    app.run(debug=True) # run dev server (auto-reloads) 