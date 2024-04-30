from bs4 import BeautifulSoup
import re
from dataclasses import dataclass

@dataclass
class RowData:
    tiny_img_src: str
    desc: str
    ss_url: str
    model: str
    year: str
    engine: str
    mileage: str
    price: str

def extract_rows(html_content: str):
    row_regex = re.compile(r"tr_\d+")
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find_all("tr", id=row_regex)

def extract_row_data(row) -> RowData:
    tds = row.find_all("td")
    img_src = tds[1].find("img").get("src")
    description_link = row.find("a", id=re.compile(r"dm_\d+"))
    description = description_link.text
    ss_url = description_link.get("href")
    
    return RowData(
        tiny_img_src=img_src,
        desc=description,
        ss_url=ss_url,
        model=tds[3].text,
        year=tds[4].text,
        engine=tds[5].text,
        mileage=tds[6].text,
        price=tds[7].text
    )