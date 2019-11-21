import time
import sys
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession, HTMLSession

session = HTMLSession()

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

#Storing formatted date string in a list. Date requests will be every 3 days and length of stay is 10 nights
#these are for Ashburn Court Apartments 
ascstart_date = start_date
ascdep_date = end_Date_User
ascstart_url=[]
ascdep_url=[]
num_nights = timedelta(days=10)
numdays = timedelta(days=3)
for i in range(365):
	if ascstart_date >= end_Date_User:
		ascstart_url.append(end_Date_User.strftime("%Y-%m-%d"))
		ascdep_date = end_Date_User + num_nights
		ascdep_url.append(ascdep_date.strftime("%Y-%m-%d"))
		break
	else:
		ascstart_url.append(ascstart_date.strftime("%Y-%m-%d"))
		ascdep_date = ascstart_date + num_nights
		ascdep_url.append(ascdep_date.strftime("%Y-%m-%d"))
		ascstart_date += numdays
#------------

#Storing formatted date string in a list. Date requests will be every 3 days and length of stay is 10 nights
#these are for Cheval Harrington Court 
chcstart_date =  start_date
chcstart_url=[]
for i in range(365):
	if chcstart_date >= end_Date_User:
		chcstart_url.append(end_Date_User.strftime("%Y-%m-%d"))
		break
	else:
		chcstart_url.append(chcstart_date.strftime("%Y-%m-%d"))
		chcstart_date += numdays
chcnum_nights = 2
#-------------

r = session.get(f"https://secure.chevalresidences.com/convert/site/Cheval%20Harrington%20Court[wsJsZoGCLg62hr_WrMSMy9dIwRklPItcNUhU30wAXMo]/en/results.php?checkin={chcstart_url[i]}&nights={chcnum_nights}&currency=GBP&resultViewType=mda&viewtype=rateroom&partya=0")

result = r.html.find("span[id^='mbprice_6152281_15070']", first=True).text
print(result)

