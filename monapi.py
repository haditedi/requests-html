import re
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
import myfunc
import csv
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

while True:
    print("Please enter end date (dd-mm-yy): ")
    inEndDate = input()
    try:
        end_Date_User = datetime.strptime(inEndDate[:2]+'-'+inEndDate[3:5]+'-'+inEndDate[6:8], '%d-%m-%y')
        if end_Date_User < start_date:
            print("End date should be greater than start date")
        elif end_Date_User > (start_date+max_date):
            print("End date should not be more than a year")
        else:
            break
    except Exception as e:
        print(e)
print("processing,,,\n")

num_days = (end_Date_User - start_date).days
num_days = round(num_days/14)+1
end_Date_User = start_date

storage_mon = ["Date", "Mon1bed"]
monarch1File = open('./data/Monarch1beda.csv', 'w', newline='')
mon1File = csv.writer(monarch1File)
mon1File.writerow(storage_mon)
storage_mon = []

storage_mon = ["Date", "Mon2bed"]
monarch2File = open('./data/Monarch2beda.csv', 'w', newline='')
mon2File = csv.writer(monarch2File)
mon2File.writerow(storage_mon)
storage_mon = []

storage_mon = ["Date", "MonS3bed"]
monarchs3File = open('./data/Monarchs3beda.csv', 'w', newline='')
mons3File = csv.writer(monarchs3File)
mons3File.writerow(storage_mon)
storage_mon = []

for i in range(num_days):  
    monstart_date = start_date.strftime("%Y-%m-%d")
    monend_date = end_Date_User.strftime("%Y-%m-%d")   

    r = myfunc.get_monarch(monstart_date, monend_date).text
    data = json.loads(r)
    dataloop = data[0]['room_types']

    loop_room = dataloop[4]['room_type_dates']
    loop_type = dataloop[4]['name'] 
                
    if loop_room[0]['available'] > 0:
        print(loop_type)
        datesplit = loop_room[0]['date'].split('-')
        date1bed = datesplit[2]+'-'+datesplit[1]
        storage_mon.insert(0,date1bed)
        rate1bed = float(loop_room[0]['rate'])/1.2
        rate1bed = round(rate1bed)
        storage_mon.insert(1,rate1bed)
        mon1File.writerow(storage_mon)
        storage_mon = []
        print(loop_room[0]['date'] + ' ' + str(rate1bed))
        
    
    loop_room = dataloop[7]['room_type_dates']
    loop_type = dataloop[7]['name']
    
    if loop_room[0]['available'] > 0:
        print(loop_type)
        datesplit = loop_room[0]['date'].split('-')
        date2bed = datesplit[2]+'-'+datesplit[1]
        storage_mon.insert(0,date2bed)
        rate2bed = float(loop_room[0]['rate'])/1.2
        rate2bed = round(rate2bed)
        storage_mon.insert(1,rate2bed)
        mon2File.writerow(storage_mon)
        storage_mon = []
        print(loop_room[0]['date'] + ' ' + str(rate2bed)) 
          

    loop_room = dataloop[5]['room_type_dates']
    loop_type = dataloop[5]['name']
    
    if loop_room[0]['available'] > 0:
        print(loop_type)
        datesplit = loop_room[0]['date'].split('-')
        dates3bed = datesplit[2]+'-'+datesplit[1]
        storage_mon.insert(0,dates3bed)
        rates3bed = float(loop_room[0]['rate'])/1.2
        rates3bed = round(rates3bed)
        storage_mon.insert(1,rates3bed)
        mons3File.writerow(storage_mon)
        storage_mon = []
        print(loop_room[0]['date'] + ' ' + str(rates3bed))    
   
    start_date += timedelta(days=14)
    end_Date_User = start_date 

monarch1File.close()
monarch2File.close()
monarchs3File.close()