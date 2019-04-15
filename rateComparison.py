import time
from datetime import datetime, timedelta
from requests_html import HTMLSession

todayDate = datetime.now()

#getting and validating input for start date and end date (should not exceed 1 year)
while True:
	print("Please enter the start date (dd-mm-yy): ")
	inStartDate = input()
	try:
		start_date = datetime.strptime(inStartDate[:2]+'-'+inStartDate[3:5]+'-'+inStartDate[6:8], '%d-%m-%y')
		if start_date > todayDate:
			break
		else:
			print("date should be at least tommorrow")
	except Exception as e:
		print(e)
while True:
	max_date = timedelta(days=366)
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


#Storing formatted date string in a list. Date requests will be every 10 days and lenght of stay is 5 
start_url=[]
for i in range(365):
	days = timedelta(days=10)
	if start_date >= end_Date_User:
		start_url.append(end_Date_User.strftime("%Y-%m-%d"))
		break
	else:
		start_url.append(start_date.strftime("%Y-%m-%d"))
		start_date = start_date + days


#Time to go out and get those datas
num_nights = 5
for i in range(len(start_url)):
	session = HTMLSession()
	r = session.get(f"https://secure.chevalresidences.com/portal/site/www.chevalresidences.com/en/results.php?checkin={start_url[i]}&nights={num_nights}&keyword=CHC")
	r.html.render()
	try:
		price1bed = r.html.find("span[id*='mbprice_'][id$='15070']", first=True).text
		price2bed = r.html.find("span[id*='mbprice_'][id$='15071']", first=True).text
		price1bed_exvat=float(price1bed.replace(",",""))/1.2
		price2bed_exvat=float(price2bed.replace(",",""))/1.2
		nprice1bed=price1bed_exvat/num_nights
		nprice2bed=price2bed_exvat/num_nights
		print("Date " + start_url[i])
		print("Superior One Bedroom " + nprice1bed)
		print("2 Bedroom Apartment " + nprice2bed)
		print("")
		time.sleep(70)
	except Exception as e:
		print(e)
		time.sleep(70)
		
	
