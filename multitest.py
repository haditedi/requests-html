import time
import re
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
from matplotlib import pyplot as plt
import csv


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

storage = ["Date","Chc1bed","Chc2bed","Ash1bed", "Ash2bed"]

chevalFile = open('cheval.csv', 'w', newline='')
chFile = csv.writer(chevalFile)
chFile.writerow(storage)


#Requesting data from Cheval Harrington Court and Ashburn Court
for i in range(len(start_date_u)):
    ascdate=start_date_u[i]
    ascdep_date = ascdep_url[i]
    asession = AsyncHTMLSession()
    
    async def getasc():
        r = await asession.get(f"https://booking.maykenbel.com/?chain=19159&template=maykenbel&shell=MKNBL2018&start=availresults&brand=maykenbe&currency=GBP&lang=1&arrive={ascdate[5:7]}%2F{ascdate[8:10]}%2F{ascdate[:4]}&depart={ascdep_date[5:7]}%2F{ascdep_date[8:10]}%2F{ascdep_date[:4]}&hotel=70825&dpArrive={ascdate[8:10]}%2F{ascdate[5:7]}%2F{ascdate[:4]}&dpDepart={ascdep_date[8:10]}%2F{ascdep_date[5:7]}%2F{ascdep_date[:4]}&rooms=1&adult=1&promo=")
        return r
    
    async def getchc():
        r = await asession.get(f"https://secure.chevalresidences.com/convert/site/Cheval%20Harrington%20Court[wsJsZoGCLg62hr_WrMSMy9dIwRklPItcNUhU30wAXMo]/en/results.php?checkin={chcstart_url[i]}&nights={chcnum_nights}&currency=GBP&resultViewType=mda&viewtype=rateroom&partya=0")
        return r
        
    results = asession.run(getasc, getchc)
    
    for result in results:
        match=re.search("cheval",result.html.url)
        print("Date " + ascdate)
        
        if match:
            try:
                storage = []
                
                discchc1bed = result.html.find("#mbprice_4539166_15070_123", first=True).text
                chc1bed = result.html.find("#mbprice_6152281_15070_123", first=True).text
                discchc2bed = result.html.find("#mbprice_4539166_15071_123", first=True).text
                chc2bed = result.html.find("#mbprice_6152281_15071_123", first=True).text
                
                asc1bed = result.html.find("div.ProductsList div[data-room-code='A1F'] span[id*='PriceData']", first=True).text
                asc2bed = result.html.find("div.ProductsList div[data-room-code='2BD'] span[id*='PriceData']", first=True).text
                
                if discchc1bed:
                    chc1bed = discchc1bed
                if discchc2bed:
                    chc2bed = discchc2bed
                
                print("chc1bed " + chc1bed)
                print("chc2bed " + chc2bed)
                chc1bed = chc1bed.replace(",","")
                chc1bed=(float(chc1bed))/1.2
                chc1bed=round(chc1bed/chcnum_nights)
                chc2bed = chc2bed.replace(",","")                
                chc2bed=(float(chc2bed))/1.2
                chc2bed=round(chc2bed/chcnum_nights)

                print("ash1bed " + asc1bed)
                print("ash2bed " + asc2bed)
                ascPrice1bed_exvat=asc1bed.replace(",","")
                ascPrice1bed=(float(ascPrice1bed_exvat))/1.2
                ascPrice1bed=round(ascPrice1bed)



                storage.append(ascdate)
                storage.append(chc1bed)
                storage.append(chc2bed)
                chFile.writerow(storage)
                            
            except Exception as e:
                print(e)
                
            
        
        # else:
        #     try:
        #         asc1bed = result.html.find("div.ProductsList div[data-room-code='A1F'] span[id*='PriceData']", first=True).text
        #         ascPrice1bed_exvat=asc1bed.replace(",","")
        #         ascPrice1bed=(float(ascPrice1bed_exvat))/1.2
        #         ascPrice1bed=round(ascPrice1bed)
        #         s_date_asc1bed.append(ascdate)
        #         s_rate_asc1bed.append(ascPrice1bed)
        #         print("Deluxe 1 bedroom -ASC- £ " + str(ascPrice1bed))
        #     except Exception as e:
        #         print(e)
        #         print("No availability -ASC- Deluxe 1 Bed")
                            
        #     try:
        #         asc2bed = result.html.find("div.ProductsList div[data-room-code='2BD'] span[id*='PriceData']", first=True).text
        #         ascPrice2bed_exvat=asc2bed.replace(",","")
        #         ascPrice2bed=(float(ascPrice2bed_exvat))/1.2
        #         ascPrice2bed=round(ascPrice2bed)
        #         s_date_asc2bed.append(ascdate)
        #         s_rate_asc2bed.append(ascPrice2bed)
        #         print("Deluxe 2 bedroom -ASC- £ " + str(ascPrice2bed))
        #     except Exception as e:
        #         print(e)
        #         print("No availability -ASC- Deluxe 2 Bed")
                           
        #     try:
        #         asc3bed = result.html.find("div.ProductsList div[data-room-code='3BD'] span[id*='PriceData']", first=True).text
        #         ascPrice3bed_exvat=asc3bed.replace(",","")
        #         ascPrice3bed=(float(ascPrice3bed_exvat))/1.2
        #         ascPrice3bed=round(ascPrice3bed)
        #         s_date_asc3bed.append(ascdate)
        #         s_rate_asc3bed.append(ascPrice3bed)
        #         print("Deluxe 3 bedroom- ASC- £ " + str(ascPrice3bed))
        #     except Exception as e:
        #         print(e)
        #         print("No availability -ASC- Deluxe 3 Bed")
   
        print("")
        time.sleep(70)





chevalFile.close()

# ashburnFile = open('ashburn.csv', 'w', newline='')
# outFile = csv.writer(ashburnFile)
# outFile.writerow(s_date_asc1bed)
# outFile.writerow(s_rate_asc1bed)
# outFile.writerow(s_date_asc2bed)
# outFile.writerow(s_rate_asc2bed)
# outFile.writerow(s_date_asc3bed)
# outFile.writerow(s_rate_asc3bed)
# ashburnFile.close()



# plt.plot(s_date_chc1bed, s_rate_chc1bed, label="cheval 1 bed")
# plt.plot(s_date_chc2bed, s_rate_chc2bed, label="cheval 2 bed")
# plt.plot(s_date_asc1bed, s_rate_asc1bed, label="Ashburn 1 bed")
# plt.plot(s_date_asc2bed, s_rate_asc2bed, label="Ashburn 2 bed")
# plt.plot(s_date_asc3bed, s_rate_asc3bed, label="Ashburn 3 bed")

# plt.xlabel("date")
# plt.ylabel("rate")
# plt.title("Rate Shopper")

# plt.style.use("fivethirtyeight")
# plt.savefig("pic.png")
# plt.legend()
# plt.show()

# plt.tight_layout()


input("press any key to terminate,,,")