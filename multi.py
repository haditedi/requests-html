from requests_html import HTMLSession

session=HTMLSession()
r=session.get("https://booking.maykenbel.com/?chain=19159&template=maykenbel&shell= \
	MKNBL2018&start=availresults&brand=maykenbe&currency=GBP&lang=1&arrive=05%2F01%2F2019&depart= \
	05%2F11%2F2019&hotel=70824&dpArrive=01%2F05%2F2019&dpDepart=11%2F05%2F2019&rooms=1&adult=1&promo=")
r.html.render()

one=r.html.find("div.ProductsList div[class*='HeaderPrice'] span[id*='V151_C1_AR_ctl00']",first=True).text
print(one)