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



    

    