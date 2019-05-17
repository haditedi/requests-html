from requests_html import HTMLSession
from requests_html import AsyncHTMLSession


asession = AsyncHTMLSession()

async def getmk():
	r = await asession.get("https://booking.maykenbel.com/?chain=19159&template=maykenbel&shell= \
		MKNBL2018&start=availresults&brand=maykenbe&currency=GBP&lang=1&arrive=11%2F1%2F2019&depart= \
		11%2F11%2F2019&hotel=70824&dpArrive=01%2F11%2F2019&dpDepart=11%2F11%2F2019&rooms=1&adult=1&promo=")
	return r

async def getchc():
	r = await asession.get("https://secure.chevalresidences.com/portal/site/www.chevalresidences.com/en/results.php?checkin= \
		2019-11-01&nights=10&keyword=CHC")
	return r

results = asession.run(getmk, getchc)
print(results)

price1bed = results[1].html.find("span[id*='mbprice_'][id$='15070']", first=True).text
print(price1bed)

'''
one=r.html.find("div.ProductsList div[class*='HeaderPrice'] span[id*='V151_C1_AR_ctl00']",first=True).text
print(one)
'''