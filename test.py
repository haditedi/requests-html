import time
import sys
from datetime import datetime, timedelta
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
async def get_cheval():
	r=await asession.get("https://secure.chevalresidences.com/portal/site/www.chevalresidences.com/en/results.php?checkin=2019-11-01&nights=10&keyword=CHC")
	await r.html.arender()
	return r

async def get_garden():
	s=await asession.get("https://be.synxis.com/?_ga=2.85469977.1228540469.1556119709-1038100479.1551104847&adult=1&arrive=2019-05-05&chain=21125&child=0&currency=GBP&depart=2019-05-06&hotel=3662&level=hotel&locale=en-GB&rooms=1&sbe_ri=0")
	await s.html.arender()
	return s

asession.run(get_cheval, get_garden)
onebed=s.html.find("div[data-rate-code='AP1'] span",first=True).text

