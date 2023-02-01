import pytz
import time
from multiprocessing import Process
# Importing required libraries
from datetime import datetime   #To set date and time
#from playsound import playsound     #To play sound
import pytz
import time
import scraper_engine


bd_time_zone ="Asia/Dhaka"

def get_bd_current_local_time():
    bdTz = pytz.timezone(bd_time_zone) 
    timeInBD = datetime.now(bdTz)
    currentTimeInBD = timeInBD.strftime("%I:%M:%S %p")   
    print(currentTimeInBD)
    return currentTimeInBD


def get_bd_current_working_day():
    bdTz = pytz.timezone(bd_time_zone) 
    timeInBD = datetime.now(bdTz)
    current_day = timeInBD.strftime('%A')   
    if str(current_day) == "Friday" or str(current_day) == "Saturday":        
        return False
    else:
        return True 

def validate_time(alarm_time):
    if len(alarm_time) != 11:
        return "Invalid time format! Please try again..."
    else:
        if int(alarm_time[0:2]) > 12:
            return "Invalid HOUR format! Please try again..."
        elif int(alarm_time[3:5]) > 59:
            return "Invalid MINUTE format! Please try again..."
        elif int(alarm_time[6:8]) > 59:
            return "Invalid SECOND format! Please try again..."
        else:
            return "ok"


def end_timer(alarm_time):
    while True:               
        validate = validate_time(alarm_time.lower())
        if validate != "ok":
            print(validate)
        else:
            print(f"Setting alarm for {alarm_time}...")
            break

    alarm_hour = alarm_time[0:2]
    alarm_min = alarm_time[3:5]
    alarm_sec = alarm_time[6:8]
    alarm_period = alarm_time[9:].upper()

    while True:
        #now = datetime.now()
        bdTz = pytz.timezone(bd_time_zone) 
        now = datetime.now(bdTz)
        current_hour = now.strftime("%I")
        current_min = now.strftime("%M")
        current_sec = now.strftime("%S")
        current_period = now.strftime("%p")
        print("running", alarm_time, get_bd_current_local_time())
        #if get_bd_current_local_time() == alarm_time:
        if alarm_period == current_period:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                    #if alarm_sec == current_sec:
                    print("End Up!")
                       # playsound('D:/Development/Python/stock-market-data-scraper/alarm.wav')
                    break
                      #  return True
        while True:
            scraper_engine.scraper_engine()            
            print("Data Scraped")
            time.sleep(1800)
           # func()  1800          
            break
        pass
    

        #return False       


def time_processor(alarm_time, end_time):
    while True:        
        
        validate = validate_time(alarm_time.lower())
        if validate != "ok":
            print(validate)
        else:
            print(f"Waiting for Market Open on {alarm_time}...")
            break

    alarm_hour = alarm_time[0:2]
    alarm_min = alarm_time[3:5]
    alarm_sec = alarm_time[6:8]
    alarm_period = alarm_time[9:].upper()

    while True:
        bdTz = pytz.timezone(bd_time_zone) 
        now = datetime.now(bdTz)

        current_hour = now.strftime("%I")
        current_min = now.strftime("%M")
        current_sec = now.strftime("%S")
        current_period = now.strftime("%p")

        if alarm_period == current_period:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                    if alarm_sec == current_sec:
                        print("Market Open...")
                        #while True:    
                              
                        end_timer(end_time)
                        print("Finished!")
                       
                        # playsound('D:/Development/Python/stock-market-data-scraper/alarm.wav')
                        break       


def determine_market_timming(open, close):
    #while True:
        print("Waiting.....")
        if get_bd_current_working_day() == True:
            while get_bd_current_local_time() != open:
                time_processor(open, close)
                break
        else:
            print("Market is still closed.")    
        print("Market Closed on...", get_bd_current_local_time())


