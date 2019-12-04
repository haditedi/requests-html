import time
import re
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
from matplotlib import pyplot as plt
import csv
import myfunc


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

#Storing formatted date string in a list. Date requests will be every 14 days and length of stay is 10 nights
#these are for Ashburn Court Apartments 
ascstart_date = start_date
ascdep_date = end_Date_User
monstart_date = start_date.strftime("%Y-%m-%d")
monend_date = end_Date_User.strftime("%Y-%m-%d")
print(monstart_date)
print(monend_date)

result = myfunc.get_monarch(monstart_date, monend_date)

for x in result:
    for y in x:
        print(["room_types"])