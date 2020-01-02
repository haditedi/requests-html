import time
import re
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
from matplotlib import pyplot as plt
import csv
import myfunc
import json



max_date = timedelta(days=366)
todayDate = datetime.now()
while True:
    print("Please enter the start date (dd-mm-yy): ")
    inStartDate = input()
    try:
        start_date = datetime.strptime(inStartDate[:2]+'-'+inStartDate[3:5]+'-'+inStartDate[6:8], '%d-%m-%y')
        if start_date > todayDate and start_date < (todayDate+max_date):
            break
        else:
            print("date should be at least tommorrow and not exceed 1 year")
    except Exception as e:
        print(e)


end_Date_User = start_date+timedelta(days=27)

print("processing,,,\n")


storage_mon = ["Date", "Mon1bed"]
monarch1File = open('./data/Monarch1bed.csv', 'w', newline='')
mon1File = csv.writer(monarch1File)
mon1File.writerow(storage_mon)
storage_mon = []

storage_mon = ["Date", "Mon2bed"]
monarch2File = open('./data/Monarch2bed.csv', 'w', newline='')
mon2File = csv.writer(monarch2File)
mon2File.writerow(storage_mon)
storage_mon = []

storage_mon = ["Date", "MonS3bed"]
monarchs3File = open('./data/Monarchs3bed.csv', 'w', newline='')
mons3File = csv.writer(monarchs3File)
mons3File.writerow(storage_mon)
storage_mon = []

for i in range(9):  
    monstart_date = start_date.strftime("%Y-%m-%d")
    monend_date = end_Date_User.strftime("%Y-%m-%d")   

    r = myfunc.get_monarch(monstart_date, monend_date).text
    data = json.loads(r)
    dataloop = data[0]['room_types']

    for i in range(len(dataloop)):
        loop_room = dataloop[i]['room_type_dates']
        if dataloop[i]['name'] == 'One Bedroom Apartment':
            print(dataloop[i]['name'])
            
            for y in range(len(loop_room)):
                if loop_room[y]['available'] > 0:
                    datesplit = loop_room[y]['date'].split('-')
                    date1bed = datesplit[2]+'-'+datesplit[1]
                    storage_mon.insert(0,date1bed)
                    rate1bed = float(loop_room[y]['rate'])/1.2
                    rate1bed = round(rate1bed)
                    storage_mon.insert(1,rate1bed)
                    mon1File.writerow(storage_mon)
                    storage_mon = []
                    print(loop_room[y]['date'] + ' ' + str(rate1bed))
        
        if dataloop[i]['name'] == 'Two Bedroom Apartment': 
            print(dataloop[i]['name'])
            
            for y in range(len(loop_room)):
                if loop_room[y]['available'] > 0:
                    datesplit = loop_room[y]['date'].split('-')
                    date2bed = datesplit[2]+'-'+datesplit[1]
                    storage_mon.insert(0,date2bed)
                    rate2bed = float(loop_room[y]['rate'])/1.2
                    rate2bed = round(rate2bed)
                    storage_mon.insert(1,rate2bed)
                    mon2File.writerow(storage_mon)
                    storage_mon = []
                    print(loop_room[y]['date'] + ' ' + str(rate2bed))
        
        if dataloop[i]['name'] == 'Superior Three Bed':
            print(dataloop[i]['name'])
            
            for y in range(len(loop_room)):
                if loop_room[y]['available'] > 0:
                    datesplit = loop_room[y]['date'].split('-')
                    dates3bed = datesplit[2]+'-'+datesplit[1]
                    storage_mon.insert(0,dates3bed)
                    rates3bed = float(loop_room[y]['rate'])/1.2
                    rates3bed = round(rates3bed)
                    storage_mon.insert(1,rates3bed)
                    mons3File.writerow(storage_mon)
                    storage_mon = []                
                    print(loop_room[y]['date'] + ' ' + str(rates3bed))    
    start_date += timedelta(days=28)
    end_Date_User += timedelta(days=28)  

monarch1File.close()
monarch2File.close()
monarchs3File.close()