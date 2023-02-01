from pickle import TRUE
import requests
import sys
import json
import stockurl
import threading
from bs4 import BeautifulSoup
from csv import writer



def connection():
    try:    
        response= requests.get(stockurl.get_news_url()).text    
    except:
        sys.exit("Failed to connect!")

    soup = BeautifulSoup(response, "html.parser")
    tabl = soup.find("table", class_="table")  
    print(tabl)  
    return tabl

def remove_character(line):
    line = line.replace('\r', '')
    line = line.replace('\t', '')
    line = line.replace('\n', '')
    return line

def write_json(ls_dict):
    json_object = json.dumps(ls_dict, indent=4)
   # print(json_object)
    # Writing to sample.json
    with open("news.json", "w") as outfile:
        outfile.write(json_object)

def scrap():
    
    tabl = connection()

    try:
            ls_dict = []
            # Extract data from html table 
            
                #Generate a list of dictonary
            #    ls_dict.append(ds)
            # Write a list to a JSON file
           # json_object = json.dumps(ls_dict, indent=4)                    
            print("Writing JSON data to file.....")
           # write_json(ls_dict)
    except:
        sys.exit("Faild to extract data")
    return ls_dict
