import time
import re
from requests_html import AsyncHTMLSession
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import csv
from myfunc import run_mon, get_monarch, chc_calc, run_plot1bed, run_plot2bed


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


#getting data from Monarch House api
run_mon(start_date, end_Date_User)


#Storing formatted date string in a list. Date requests will be every 14 days and length of stay is 10 nights
#these are for Ashburn Court Apartments 
ascstart_date = start_date
ascdep_date = end_Date_User
monstart_date = start_date.strftime("%d-%m-%Y")
monend_date = end_Date_User.strftime("%d-%m-%Y")
print("start date: " + monstart_date)
print("end date: " + monend_date)
start_date_u=[]
ascdep_url=[]
num_nights = timedelta(days=10)
numdays = timedelta(days=14)
for i in range(365):
    if ascstart_date >= end_Date_User:
        start_date_u.append(end_Date_User.strftime("%Y-%m-%d"))
        ascdep_date = end_Date_User + num_nights
        ascdep_url.append(ascdep_date.strftime("%Y-%m-%d"))
        break
    else:
        start_date_u.append(ascstart_date.strftime("%Y-%m-%d"))
        ascdep_date = ascstart_date + num_nights
        ascdep_url.append(ascdep_date.strftime("%Y-%m-%d"))
        ascstart_date += numdays
#------------


#Storing formatted date string in a list. Date requests will be every 14 days and length of stay are 5 nights except for June onward is 21 nights min stay
#these are for Cheval Harrington Court 
chcstart_date =  start_date
chcstart_url=[]
chc_nights = []
chcnum_nights = 5
for i in range(365):
    if chcstart_date.month > 6:
        chcnum_nights = 21
    if chcstart_date >= end_Date_User:
        chcstart_url.append(end_Date_User.strftime("%Y-%m-%d"))
        chc_nights.append(chcnum_nights)        
        break
    else:
        chcstart_url.append(chcstart_date.strftime("%Y-%m-%d"))
        chcstart_date += numdays
        chc_nights.append(chcnum_nights)        


storage_che = ["Date", "Chc1bed"]
cheval1File = open('./data/cheval1bed.csv', 'w', newline='')
che1File = csv.writer(cheval1File)
che1File.writerow(storage_che)
storage_1che = []

storage_che = ["Date", "Chc2bed"]
cheval2File = open('./data/cheval2bed.csv', 'w', newline='')
che2File = csv.writer(cheval2File)
che2File.writerow(storage_che)
storage_2che = []

storage_ash = ["Date", "Ash1bed"]
ashburn1File = open('./data/ashburn1bed.csv', 'w', newline='')
ash1File = csv.writer(ashburn1File)
ash1File.writerow(storage_ash)
storage_1ash = []

storage_ash = ["Date", "Ash2bed"]
ashburn2File = open('./data/ashburn2bed.csv', 'w', newline='')
ash2File = csv.writer(ashburn2File)
ash2File.writerow(storage_ash)
storage_2ash = []


for i in range(len(start_date_u)):
    ascdate=start_date_u[i]
    store_date=ascdate.split('-')
    store_date=store_date[2] + '-' + store_date[1]
    ascdep_date = ascdep_url[i]
    asession = AsyncHTMLSession()
    
    async def getasc():
        r = await asession.get(f"https://booking.maykenbel.com/?chain=19159&template=maykenbel&shell=MKNBL2018&start=availresults&brand=maykenbe&currency=GBP&lang=1&arrive={ascdate[5:7]}%2F{ascdate[8:10]}%2F{ascdate[:4]}&depart={ascdep_date[5:7]}%2F{ascdep_date[8:10]}%2F{ascdep_date[:4]}&hotel=70825&dpArrive={ascdate[8:10]}%2F{ascdate[5:7]}%2F{ascdate[:4]}&dpDepart={ascdep_date[8:10]}%2F{ascdep_date[5:7]}%2F{ascdep_date[:4]}&rooms=1&adult=1&promo=")
        return r
    
    async def getchc():
        r = await asession.get(f"https://secure.chevalcollection.com/convert/site/Cheval%20Harrington%20Court[wsJsZoGCLg62hr_WrMSMy9dIwRklPItcNUhU30wAXMo]/en/results.php?checkin={chcstart_url[i]}&nights={chc_nights[i]}&currency=GBP&resultViewType=sda&viewtype=rateroom&partya=0")
        return r
        
    results = asession.run(getasc, getchc)
    
    for result in results:
        print(result)
        match=re.search("cheval",result.html.url)
        
        print("Date " + ascdate)
        
        if match:

            print("Cheval Harrington Court")       
            try:
                discchc1bed = result.html.find("#mbprice_4932506_15069_123", first=True).text
                if discchc1bed:
                    chc1bed = chc_calc(discchc1bed, chc_nights[i])
                    storage_1che.insert(1, chc1bed)
                    print("discount 1 bed " + str(chc1bed))
            except Exception as e:
                print(e)
                print("no data discchc1bed")
                try:
                    chc1bed = result.html.find("#mbprice_6152281_15070_123", first=True).text
                    chc1bed = chc_calc(chc1bed, chc_nights[i])
                    storage_1che.insert(1, chc1bed)
                    print('advance 1 bed ' + str(chc1bed))             
                except Exception as e:
                    print(e)         
                    print("no data chc1bed")         
                    try:
                        chc1bed = result.html.find("#mbprice_6152281_15069_123", first=True).text
                        chc1bed = chc_calc(chc1bed, chc_nights[i])
                        storage_1che.insert(1, chc1bed)
                        print('advance 1 bed 21 nights ' + str(chc1bed))             
                    except Exception as e:
                        print(e)         
                        print("no data chc1bed 21 nights")
            

            try:
                discchc2bed = result.html.find("#mbprice_4932506_15071_123", first=True).text
                if discchc2bed:
                    chc2bed = discchc2bed
                    chc2bed = chc_calc(chc2bed, chc_nights[i])
                    storage_2che.insert(2, chc2bed)
                    print("discount 2 bed " + str(chc2bed))
            except Exception as e:
                print(e)
                print("no data discchc2bed")
                try:
                    chc2bed = result.html.find("#mbprice_6152281_15071_123", first=True).text
                    chc2bed = chc_calc(chc2bed, chc_nights[i])
                    storage_2che.insert(2, chc2bed)
                    print('advance rate 2 bed ' + str(chc2bed))
                except Exception as e:
                    print(e)
                    print("no data chc2bed")            
                    try:
                        chc2bed = result.html.find("#mbprice_6152281_15071_123", first=True).text
                        chc2bed = chc_calc(chc2bed, chc_nights[i])
                        storage_2che.insert(2, chc2bed)
                        print('advance rate 2 bed 21 nights ' + str(chc2bed))
                    except Exception as e:
                        print(e)
                        print("no data chc2bed 21nights") 

            if storage_1che:                
                storage_1che.insert(0, store_date)
                print(storage_1che)
                che1File.writerow(storage_1che)
            storage_1che = []
            if storage_2che:                
                storage_2che.insert(0, store_date)
                print(storage_2che)
                che2File.writerow(storage_2che)
            storage_2che = []
       
              
        else:
     
            print("Ashburn Court")
            try:
                asc1bed = result.html.find("div.ProductsList div[data-room-code='A1F'] span[id*='PriceData']", first=True).text
                ascPrice1bed_exvat=asc1bed.replace(",","")
                ascPrice1bed=(float(ascPrice1bed_exvat))/1.2
                ascPrice1bed=round(ascPrice1bed)
                storage_1ash.insert(1, ascPrice1bed)
                print("Deluxe 1 bedroom -ASC- £ " + str(ascPrice1bed))
            except Exception as e:
                print(e)
                print("No data -ASC- Deluxe 1 Bed")
          
            try:
                asc2bed = result.html.find("div.ProductsList div[data-room-code='2BD'] span[id*='PriceData']", first=True).text
                ascPrice2bed_exvat=asc2bed.replace(",","")
                ascPrice2bed=(float(ascPrice2bed_exvat))/1.2
                ascPrice2bed=round(ascPrice2bed)
                storage_2ash.insert(2, ascPrice2bed)
                print("Deluxe 2 bedroom -ASC- £ " + str(ascPrice2bed))
            except Exception as e:
                print(e)
                print("No data -ASC- Deluxe 2 Bed")

            # try:
            #     asc3bed = result.html.find("div.ProductsList div[data-room-code='3BD'] span[id*='PriceData']", first=True).text
            #     ascPrice3bed_exvat=asc3bed.replace(",","")
            #     ascPrice3bed=(float(ascPrice3bed_exvat))/1.2
            #     ascPrice3bed=round(ascPrice3bed)
            #     storage_ash.insert(3, ascPrice3bed)
            #     print("Deluxe 3 bedroom- ASC- £ " + str(ascPrice3bed))
            # except Exception as e:
            #     print(e)
            #     print("No data -ASC- Deluxe 3 Bed")

            if storage_1ash:
                storage_1ash.insert(0, store_date)
                print(storage_1ash)
                ash1File.writerow(storage_1ash)
            storage_1ash = []
            if storage_2ash:
                storage_2ash.insert(0, store_date)
                print(storage_2ash)
                ash2File.writerow(storage_2ash)
            storage_2ash = []

   
        print("")
        print("processing ,,,")
        time.sleep(70)


cheval1File.close()
cheval2File.close()
ashburn1File.close()
ashburn2File.close()

time.sleep(10)

#plotting charts
run_plot1bed()
run_plot2bed()

input("press any key to terminate,,,")