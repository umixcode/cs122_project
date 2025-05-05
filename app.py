from flask import Flask, render_template, jsonify
# import os # keep this removed

# remove debug path checks - keep these commented out
# app_dir = ...
# code_dir_path = ...
# init_file_path = ...
# print("--- Path Check Debug ---")
# ...
# print("--- End Path Check Debug ---")

# import our function from the src module
from src.coinGecko import fetch_historical_data

app = Flask(__name__) # create flask app instance

# --- flask routes --- 

# route for the home page (trend viewer)
@app.route('/')
def index():
    # renders index.html
    return render_template('index.html')

# route for the comparison page
@app.route('/compare')
def compare():
    # renders compare.html
    return render_template('compare.html')

# --- api endpoint for chart data --- 
@app.route('/api/chart_data/<string:coin_id>')
def get_chart_data(coin_id):
    # api endpoint to fetch historical data for a given coin
    # print(f"fetching data for coin: {coin_id}") # optional log
    data = fetch_historical_data(coin_id) # call our function
    if data:
        # return data as json if successful
        return jsonify(data)
    else:
        # return error if fetch failed
        return jsonify({"error": f"could not fetch data for {coin_id}"}), 404

# allows running the app directly using 'python app.py'
if __name__ == '__main__':
    app.run(debug=True) # runs the development server (auto-reloads) 