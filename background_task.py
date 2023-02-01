from flask import Flask
import time
import markettiming
from flask import Flask , request, jsonify
import scraper_engine
import log

while True:
      scraper_engine.scraper_engine()            
      print("Data Scraped")
      data = {"Data Scraped":markettiming.get_bd_current_local_time()}
                    
      log.write_json(data)
            
      time.sleep(30)
      break