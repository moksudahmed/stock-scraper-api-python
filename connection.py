import requests
import sys
import stockurl
from bs4 import BeautifulSoup

def connect():
    try:    
        response= requests.get(stockurl.get_url()).text    
    except:
        sys.exit("Failed to connect!")

    soup = BeautifulSoup(response, "html.parser")
    tabl = soup.find("table", class_="table")
    return tabl