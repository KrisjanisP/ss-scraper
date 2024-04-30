from bs4 import BeautifulSoup
import os
script_path = os.path.abspath(__file__)
html_path = os.path.join(os.path.dirname(script_path), "car_brand_select.html")

html = ""
with open(html_path) as file:
    html = file.read()
    brand_url_pairs = []   
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")
    for a in anchors:
        link = f'https://www.ss.lv{a.get("href")}'
        brand = a.text
        brand_url_pairs.append((brand, link))
    print(brand_url_pairs)
    
    