from requests_html import HTMLSession
import pandas as pd 
from matplotlib import pyplot as plt


def chc_calc(total,chcnum_nights):
    total = total.replace(',','')
    result=(float(total))/1.2
    return round(result/chcnum_nights)

def get_monarch(start_date, end_date):
    session = HTMLSession()
    r = session.get(f"https://app.thebookingbutton.com/api/v1/properties/monarchhousedirect/rates.json?start_date={start_date}&end_date={end_date}")
    return r

def run_plot1():
    df_ash = pd.read_csv('./data/ashburn.csv')
    df_che = pd.read_csv('./data/cheval.csv')
    df_mon = pd.read_csv('./data/monarch1bed.csv')

    plt.grid(True)

    plt.plot(df_ash['Date'], df_ash['Ash1bed'], label='Ashburn 1 bed')
    # plt.plot(df_ash['Date'], df_ash['Ash2bed'], label='Ashburn 2 bed')
    # plt.plot(df_ash['Date'], df_ash['Ash3bed'], label='Ashburn 3 bed')
    plt.plot(df_che['Date'], df_che['Chc1bed'], label='Cheval 1 bed')
    plt.plot(df_mon['Date'], df_mon['Mon1bed'], label='Monarch 1 bed')
    #plt.scatter(df_che['Date'], df_che['Chc2bed'], label='Cheval 2 bed')

    plt.xlabel("Date")
    plt.ylabel("Rate")

    plt.style.use("fivethirtyeight")
    plt.title("One Bed Comparison")
    plt.legend()
    plt.savefig('.data/sample.png')
    plt.tight_layout()

    plt.show()

    #['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']


    