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

def schedule_scraping_and_saving():
    while True:
        now = time.localtime()
        day_of_week = now.tm_wday
        hour = now.tm_hour
        minute = now.tm_min
        print("Start.....")
        if day_of_week >= 0 and day_of_week <= 3:  # Sunday to Wednesday
            if (hour == 10 and minute >= 0) or (hour >= 11 and hour < 18) or (hour == 18 and minute <= 30):
                print("Working.....")
               # scrape_data()
                scraper_engine.scraper_engine()
                time.sleep(60)  # Wait for 5 minutes between scrapes
            elif hour == 18 and minute > 30:
                save_to_json()
                print('Wait for 1 hour at the end of the market day')
               # time.sleep(3600)  # Wait for 1 hour at the end of the market day
            else:
                print('Sleep for 1 minute if outside market hours')
                time.sleep(60)  # Sleep for 1 minute if outside market hours
        else:
            print('leep for 24 hours on Thursday, then restart on Sunday')
            time.sleep(86400)  # Sleep for 24 hours on Thursday, then restart on Sunday
    print("Finished..")

if __name__ == "__main__":
    schedule_scraping_and_saving_thread = threading.Thread(target=schedule_scraping_and_saving)
    schedule_scraping_and_saving_thread.start()

    # Start the Flask app in a separate thread
    app.run(host="0.0.0.0", port=5000)
