from datetime import timedelta
from itertools import dropwhile, islice
from utils.utils import get_dom, days_lower, skip_empty_lines, on_workdays
from plugin import EbedkePlugin


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath("/html/body//div[@class='fck']/*[self::h3 or self::p]//text()")
    menu = dropwhile(lambda line: days_lower[day] not in line.lower(), menu)
    menu = islice(skip_empty_lines(menu), 1, 3)
    menu = list(menu)

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Gólvonal',
    id='gv',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=1),
    cards=[],
    groups=["corvin"]
)
