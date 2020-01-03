import pandas as pd 
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates

def run_plot1():
    df_ash = pd.read_csv('./data/ashburn.csv')
    df_che = pd.read_csv('./data/cheval.csv')
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
    plt.ylabel("Rate")
    plt.style.use("fivethirtyeight")
    plt.title("One Bed Comparison")
    plt.legend()
    dm_fmt = mdates.DateFormatter('%d-%m')
    ax.xaxis.set_major_formatter(dm_fmt)
    plt.xticks(rotation=45)
    
    plt.savefig('data/1bed.png')
    
    plt.show()
    
run_plot1()