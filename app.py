from flask import Flask
import threading
import time

from flask import Flask , request, jsonify
import processdata
import scraper_engine
import log
from time import sleep
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return jsonify(processdata.isUpdated())

@app.route('/api/stock/all', methods=['GET'])
def api_stockall():
   # processdata.isModified() 
    return jsonify(processdata.get_stock_data())    

@app.route('/api/stock/details')
def with_parameters():
    trading_code = request.args.get('trading_code')
    output = processdata.get_stock_details(trading_code)
  #  print(output)
    return jsonify(output)
 
@app.route('/api/stock/get_top10_gainer_data', methods=['GET'])
def api_get_top10_gainer_data():
   # processdata.isModified() 
    return jsonify(processdata.get_top10_gainer_data())    

@app.route('/api/stock/get_top10_loser_data', methods=['GET'])
def api_get_top10_loser_data():
   # processdata.isModified() 
    return jsonify(processdata.get_top10_loser_data())    

@app.route('/api/stock/get_top20_share_data', methods=['GET'])
def api_get_top20_share_data():
   # processdata.isModified() 
    return jsonify(processdata.get_top20_share_data())    

@app.route('/api/stock/get_local_time', methods=['GET'])
def api_get_local_time():
    return jsonify(processdata.get_local_time())    


if __name__ == "__main__":
    app.run(use_reloader=False)
    