from datetime import timedelta
from utils.utils import get_dom, on_workdays
from plugin import EbedkePlugin

URL = "http://dezsoba.hu/hu/heti-menue"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div[@class="sppb-menu-text"]')
    if len(menu) < 4:
        menu = []
    else:
        menu = menu[day].xpath("text()")

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Dezső bá',
    id='db',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=20),
    cards=[],
    groups=["corvin"]
)
