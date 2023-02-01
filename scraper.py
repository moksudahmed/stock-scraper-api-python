from pickle import TRUE
import requests
import sys
import json
import stockurl
import threading
from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime
import pytz

def connection():
    try:    
        response= requests.get(stockurl.get_url()).text    
    except:
        sys.exit("Failed to connect!")

    soup = BeautifulSoup(response, "html.parser")
    tabl = soup.find("table", class_="table")
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
    with open("stockdata.json", "w") as outfile:
        outfile.write(json_object)

def scrap():
    
    tabl = connection()

    try:
            ls_dict = []
            # Extract data from html table 
            for row in tabl.find_all('tr')[1:]:
                ds = {"SL":"",
                    "TRADING_CODE":"",
                    "LTP":"",
                    "HIGH":"",
                    "LOW":"",
                    "CLOSE":"",
                    "YCP":"",
                    "CHANGE":"",
                    "TRADE":"",
                    "VALUE":"",
                    "VOLUME":""
                    }
                td = row.find_all('td')            
                # Update data to a dictonary
                ds.update({ "SL":td[0].text,
                            "TRADING_CODE":remove_character(td[1].text), 
                            "LTP" : td[2].text, 
                            "HIGH" : td[3].text,
                            "LOW" : td[4].text,
                            "CLOSE" : td[5].text,
                            "YCP" : td[6].text,
                            "CHANGE" : td[7].text,
                            "TRADE" : td[8].text,
                            "VALUE" : td[9].text,
                            "VOLUME" : td[10].text
                        })
                #Generate a list of dictonary
                ls_dict.append(ds)
            # Write a list to a JSON file
           # json_object = json.dumps(ls_dict, indent=4)                    
            print("Writing JSON data to file.....")
            write_json(ls_dict)
    except:
        sys.exit("Faild to extract data")
    return ls_dict

def get_stock_details(trading_code):
    try:    
        response= requests.get("https://www.dse.com.bd/displayCompany.php?name="+trading_code).text    
    except:
        sys.exit("Failed to connect!")

    soup = BeautifulSoup(response, "html.parser")
   # tabl = soup.find("row", class_="row")
    table = soup.findAll('table', id = "company")
    
    #print(table[2])
    #print(table[1])
    return scrap_stock_details(table[1], table[2])

def scrap_table_title(tabl):  
    try:
            titles = []
            # Extract data from html table 
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
  
                if th[0].text !="52 Weeks' Moving Range":
                    titles.append(remove_character(th[0].text))
                    
                if th[0].text =="52 Weeks' Moving Range":
                    titles.append('')
            
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
                if remove_character(th[0].text) == "52 Weeks' Moving Range":
                    continue
                else:
                    titles.append(remove_character(th[1].text))                   
            
            return titles
    except:
        sys.exit("Faild to extract data")

def scrap_table_values(tabl):  
    try:
            values = []
            # Extract data from html table 
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
  
                if th[0].text !="52 Weeks' Moving Range":
                    values.append(remove_character(td[0].text))
                    
                if th[0].text =="52 Weeks' Moving Range":
                    values.append(remove_character(td[0].text))
      
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
                if remove_character(th[0].text) == "52 Weeks' Moving Range":
                    continue
                else:
                    values.append(remove_character(td[1].text))
                  
            return values
    except:
        sys.exit("Faild to extract data")

def scrap_stock_details(tabl, tabl2):  
    try:
            values_titles =[]
            values, titles = [], []            
            titles.append(scrap_table_title(tabl))
            values.append(scrap_table_values(tabl))
            values_titles = [{"name": t, "stock_value": s} for t, s in zip(scrap_table_title(tabl), scrap_table_values(tabl))]
            values_titles2 = [{"name": t, "stock_value": s} for t, s in zip(scrap_table_title(tabl2), scrap_table_values(tabl2))]
            for obj in values_titles2:
              values_titles.append({"name": obj['name'], "stock_value": obj['stock_value']}) 
            return values_titles

    except:
        sys.exit("Faild to extract data")
def Merge(dict_1, dict_2):
	result = dict_1 | dict_2
	return result

def scrap_stock_details3(tabl, tabl2):
  
    try:
            values, titles = [], []
            table = []
            table.append(scrap_table(tabl))
            table.append(scrap_table(tabl2))
            print(table)
            # Extract data from html table 
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
  
                if th[0].text !="52 Weeks' Moving Range":
                    titles.append(remove_character(th[0].text))
                    values.append(remove_character(td[0].text))
                    
                if th[0].text =="52 Weeks' Moving Range":
                    titles.append('')
                    values.append(remove_character(td[0].text))
      
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
                if remove_character(th[0].text) == "52 Weeks' Moving Range":
                    continue
                else:
                    titles.append(remove_character(th[1].text))
                    values.append(remove_character(td[1].text))
                    
            values_titles = [{"name": t, "stock_value": s} for t, s in zip(titles, values)]
            
            return values_titles
    except:
        sys.exit("Faild to extract data")

def scrap_stock_details2(tabl):
  
    try:
            final_ls_dict = []
            # Extract data from html table 
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
  
                if th[0].text !="52 Weeks' Moving Range":
                    ds={remove_character(th[0].text):remove_character(td[0].text)}
                if th[0].text =="52 Weeks' Moving Range":
                    ds={'':remove_character(td[0].text)}
                final_ls_dict.append(ds) 
  
            for row in tabl.find_all('tr')[0:]:
                th = row.find_all('th')    
                td = row.find_all('td')
                if remove_character(th[0].text) == "52 Weeks' Moving Range":
                    continue
                else:
                    ds={remove_character(th[1].text):remove_character(td[1].text)}
                    final_ls_dict.append(ds)                
            tables = ["a", "b", "c", "d", "e", "f", "g","h", "i", "j", "k", "l", "m"]
            data = {}
            i = 0
            for t in tables:     
                #for i in range(0, len(final_ls_dict)):   
                data[t] = final_ls_dict[i]
                i += 1
            #print(data)
            
            return data
    except:
        sys.exit("Faild to extract data")

def get_bd_current_local_time():
    bdTz = pytz.timezone("Asia/Dhaka") 
    timeInBD = datetime.now(bdTz)
    currentTimeInBD = timeInBD.strftime("%H:%M:%S")
    return currentTimeInBD
