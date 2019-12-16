import time
import re
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
from matplotlib import pyplot as plt
import csv
import myfunc
import json


#getting and validating input for start date and end date (should not exceed 1 year)
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
#-----------------


ascstart_date = start_date
ascdep_date = end_Date_User
monstart_date = start_date.strftime("%Y-%m-%d")
monend_date = end_Date_User.strftime("%Y-%m-%d")
print(monstart_date)
print(monend_date)

r = myfunc.get_monarch(monstart_date, monend_date).text
results = json.loads(r)

disp = results[0]['room_types']

for x in range(len(disp)):
    if 'One Bedroom Apartment' in disp[x].values():
        for y in disp[x]['room_type_dates']:
            print(y['rate'])


    # if 'One Bedroom Apartment' in a.values():
    #     for y in disp[x]['room_type_dates']:
    #         print(disp[x]['room_type_dates'][y]['date'])



