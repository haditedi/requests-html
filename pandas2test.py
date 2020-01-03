import pandas as pd 
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates

def run_plot1():
    df_ash = pd.read_csv('./data/ashburn.csv')
    df_che = pd.read_csv('./data/cheval.csv')
    df_mon = pd.read_csv('./data/monarch2bed.csv')
    
    df_ash.Date = pd.to_datetime(df_ash.Date, format='%d-%m')
    df_mon.Date = pd.to_datetime(df_mon.Date, format='%d-%m')
    df_che.Date = pd.to_datetime(df_che.Date, format='%d-%m')
    
    df_che['Date_ffill'] = df_che['Date'].ffill()
    df_che['Chc2bed_ffill'] = df_che['Chc2bed'].ffill()
    
    df_ash['Date_ffill'] = df_ash['Date'].ffill()
    df_ash['Ash2bed_ffill'] = df_ash['Ash2bed'].ffill()
    

    register_matplotlib_converters()
    fig, ax = plt.subplots()  # figsize=(10, 6)
    ax.grid(True)
    ax.plot(df_ash['Date_ffill'], df_ash['Ash2bed_ffill'], label='Ashburn 2 bed')
    ax.plot(df_mon['Date'], df_mon['Mon2bed'], label='Monarch 2 bed')
    ax.plot(df_che['Date_ffill'], df_che['Chc2bed_ffill'], label='Cheval 2 bed')
    plt.xlabel("Date")
    plt.ylabel("Rate")
    plt.style.use("fivethirtyeight")
    plt.title("Two Bed Comparison")
    plt.legend()
    dm_fmt = mdates.DateFormatter('%d-%m')
    ax.xaxis.set_major_formatter(dm_fmt)
    plt.xticks(rotation=45)
    
    plt.savefig('data/2bed.png')
    
    plt.show()
    
run_plot1()