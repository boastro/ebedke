from datetime import datetime, timedelta
from io import BytesIO
from itertools import dropwhile, takewhile, islice
from unicodedata import normalize
from PIL import Image
from provider.utils import get_fb_post_attached_image, on_workdays, ocr_image, days_lower


FB_PAGE = "https://www.facebook.com/primacorvin/"
FB_ID = "515236985157143"

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "heti menü" in post['message'].lower()
    image = get_fb_post_attached_image(FB_ID, menu_filter)
    if image:
        image = Image.open(BytesIO(image)).convert('L')
        width, height = image.size
        cropbox = (0, round(height * 0.21), width, height - round(height * 0.14))
        image = image.crop(cropbox)

        f = BytesIO()
        image.save(f, format="png", optimize=True)
        menu = ocr_image(f).splitlines()
        if not menu:
            return ""
        day = today.weekday()
        remove_accents = lambda word: normalize('NFD', word).encode('ascii', 'ignore')
        menu = islice(dropwhile(lambda l: remove_accents(days_lower[day]) not in remove_accents(l.lower()), menu), 1, None)
        menu = takewhile(lambda l: not any(word in l.lower() for word in days_lower), menu)
        skip_words = ["menu", "menü", "fitnesz"] + days_lower
        menu = list(map(lambda l: l.replace("|", ""), filter(lambda l: not any(word in l.lower() for word in skip_words), menu)))
        menu = sorted(set(menu), key=menu.index)
        menu = "<br>".join(menu)
        return menu
    else:
        return ""


menu = {
    'name': 'CBA Corvin',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=24),
    'cards': ['bank', 'szep', 'erzs']
}
