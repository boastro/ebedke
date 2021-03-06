from datetime import timedelta
from utils.utils import get_dom, on_workdays
from plugin import EbedkePlugin

URL = "http://www.gyorsetterem.hu/hetimenu.php"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, force_utf8=True)
    date = dom.xpath("/html/body//div[@class='maidatum']/text()")
    date = date.pop().strip() if date else None
    if date == today.strftime("%Y-%m-%d"):
        menu = dom.xpath("/html/body//div[@class='napimenu']/p/text()")
        menu = list(menu)
    else:
        menu = ''
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='JóAsszony',
    id='ja',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["szell", "corvin"]
)
