import requests
import time

url = "https://www.ss.lv/lv/transport/cars/filter/"


class PageGetter:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "Lizard"
        self.s.get(url, allow_redirects=True)

    def get_page_html(self, brand, page_no) -> str:
        url = f"https://www.ss.lv/en/transport/cars/audi/page{page_no}.html"
        r = self.s.get(url, allow_redirects=False)
        return r.text
