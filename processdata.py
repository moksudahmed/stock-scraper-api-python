import os
from pickle import FALSE, TRUE
import datetime
from datetime import datetime
import scraper
import json
import markettiming
def get_stock_data():
    with open('stockdata.json', 'r') as f:      
      data = json.load(f)     
    return data    

def get_stock_details(trading_code):
    data = scraper.get_stock_details(trading_code)
    return data    

def get_top10_gainer_data():
    with open('top_ten_gainer.json', 'r') as f:      
      data = json.load(f)     
    return data 

def get_top10_loser_data():
    with open('top_ten_loser.json', 'r') as f:      
      data = json.load(f)     
    return data 

def get_top20_share_data():
    with open('top_20_share.json', 'r') as f:      
      data = json.load(f)     
    return data 

def get_local_time():
    data = scraper.get_bd_current_local_time()
    return data    

def isModified():  
    # Path to the file
    path = "stockdata.json"
    # file modification timestamp of a file
    m_time = os.path.getmtime(path)
    # convert timestamp into DateTime object
    dt_m = datetime.fromtimestamp(m_time)
    #print('Last Modified on:', dt_m)    
    # in hours:minutes:seconds format
    delta = datetime.now() - dt_m        
    if delta.total_seconds() >= 300:
       scraper.scrap()
       return TRUE
    else:
       return FALSE


def isUpdated():  
    # Path to the file
    ds =[]
    path = "stockdata.json"
    # file modification timestamp of a file
    m_time = os.path.getmtime(path)
    dt_m = datetime.fromtimestamp(m_time)
    ds.append(dt_m)
    ds.append(markettiming.get_bd_current_local_time())
    # convert timestamp into DateTime object
    return ds

