from requests_html import HTMLSession
import pandas as pd 
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import csv
import json
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates


def chc_calc(total,chcnum_nights):
    total = total.replace(',','')
    result=(float(total))/1.2
    return round(result/chcnum_nights)

def get_monarch(start_date, end_date):
    session = HTMLSession()
    r = session.get(f"https://app.thebookingbutton.com/api/v1/properties/monarchhousedirect/rates.json?start_date={start_date}&end_date={end_date}")
    return r

def run_mon(start_date, end_Date_User):

    num_days = (end_Date_User - start_date).days
    num_days = round(num_days/14)+1
    end_Date_User = start_date

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

    for i in range(num_days):  
        monstart_date = start_date.strftime("%Y-%m-%d")
        monend_date = end_Date_User.strftime("%Y-%m-%d")   

        r = get_monarch(monstart_date, monend_date).text
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


def run_plot1bed():
    df_ash = pd.read_csv('./data/ashburn1bed.csv')
    df_che = pd.read_csv('./data/cheval1bed.csv')
    df_mon = pd.read_csv('./data/monarch1bed.csv')
    
    df_ash.Date = pd.to_datetime(df_ash.Date, format='%d-%m')
    df_mon.Date = pd.to_datetime(df_mon.Date, format='%d-%m')
    df_che.Date = pd.to_datetime(df_che.Date, format='%d-%m')    

    register_matplotlib_converters()
    fig, ax = plt.subplots()  # figsize=(10, 6)
    ax.grid(True)
    ax.plot(df_ash['Date'], df_ash['Ash1bed'], label='Ashburn 1 bed')
    ax.plot(df_mon['Date'], df_mon['Mon1bed'], label='Monarch 1 bed')
    ax.plot(df_che['Date'], df_che['Chc1bed'], label='Cheval 1 bed')
    plt.xlabel("Date")
    plt.ylabel("Rate (£) - exclude vat")
    plt.style.use("fivethirtyeight")
    plt.title("One Bed Rate Comparison")
    plt.legend()
    dm_fmt = mdates.DateFormatter('%d-%m')
    ax.xaxis.set_major_formatter(dm_fmt)
    plt.xticks(rotation=45)
    
    plt.savefig('data/1bed.png')
    
    plt.show()
    

def run_plot2bed():
    df_ash = pd.read_csv('./data/ashburn2bed.csv')
    df_che = pd.read_csv('./data/cheval2bed.csv')
    df_mon = pd.read_csv('./data/monarch2bed.csv')
    
    df_ash.Date = pd.to_datetime(df_ash.Date, format='%d-%m')
    df_mon.Date = pd.to_datetime(df_mon.Date, format='%d-%m')
    df_che.Date = pd.to_datetime(df_che.Date, format='%d-%m')   

    register_matplotlib_converters()
    fig, ax = plt.subplots()  # figsize=(10, 6)
    ax.grid(True)
    ax.plot(df_ash['Date'], df_ash['Ash2bed'], label='Ashburn 2 bed')
    ax.plot(df_mon['Date'], df_mon['Mon2bed'], label='Monarch 2 bed')
    ax.plot(df_che['Date'], df_che['Chc2bed'], label='Cheval 2 bed')
    plt.xlabel("Date")
    plt.ylabel("Rate (£) - exclude vat")
    plt.style.use("fivethirtyeight")
    plt.title("Two Bed Rate Comparison")
    plt.legend()
    dm_fmt = mdates.DateFormatter('%d-%m')
    ax.xaxis.set_major_formatter(dm_fmt)
    plt.xticks(rotation=45)
    
    plt.savefig('data/2bed.png')
    
    plt.show()



    

    