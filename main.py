import subprocess
from PageGetter import PageGetter
from bs4 import BeautifulSoup
import re
from jinja2 import Environment, FileSystemLoader

ss = PageGetter()

def open_in_browser(html_content:str):
    with open("response.html", "w") as file:
        file.write(html_content)
    subprocess.run(["firefox", "response.html"])
    
def extract_rows(html_content:str):
    row_regex = re.compile(r"tr_\d+")
    soup = BeautifulSoup(html_content, "html.parser")
    matching_rows = soup.find_all("tr",id=row_regex)
    return matching_rows

def extract_row_data(row):
    tds = row.find_all("td")
    return {
        "img_src": tds[1].find("img").get("src"),
        "description": row.find("a",id=re.compile(r"dm_\d+")).text,
        "ss_url": row.find("a",id=re.compile(r"dm_\d+")).get("href"),
        "model": tds[3].text,
        "year": tds[4].text,
        "engine": tds[5].text,
        "mileage": tds[6].text,
        "price": tds[7].text,
    }

rows = []

page = 1
while True:
    print(f"Processing page {page}")
    page_html = ss.get_page_html("audi", page)
    page_rows = extract_rows(page_html)
    if not page_rows:
        break
    rows.extend(page_rows)
    page += 1

data = [extract_row_data(row) for row in rows]

for i in range(len(rows)):
    data[i]["brand"] = "Audi"

environment = Environment(loader=FileSystemLoader("templates"))
results_filename = "results.html"
results_template = environment.get_template("table.html")

with open(results_filename, "w") as file:
    file.write(results_template.render(cars=data))