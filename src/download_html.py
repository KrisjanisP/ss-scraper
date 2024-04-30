from extract_data import extract_rows, extract_row_data
from car_brands import car_brands
import requests
import os

def download_brand_pages(brand,link,dist_dir):
    page_no=1
    while True:
        rows_link = f"{link}page{page_no}.html"
        print(f"Downloading {brand} page {page_no} from {rows_link}")
        response = requests.get(rows_link,allow_redirects=False)
        if response.status_code != 200:
            print(f"Done")
            break
        html = response.text
        if not html:
            print(f"Done")
            break
        path = f"{dist_dir}/{brand}/rows/{page_no}.html"
        # create dir
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.write(html)
        rows = extract_rows(html)
        pages_set = set()
        for _, row in enumerate(rows):
            row_data = extract_row_data(row)
            page = row_data.ss_url.split("/")[-1].split(".")[0]
            if page in pages_set:
                continue
            pages_set.add(page)
            path = f"{dist_dir}/{brand}/full/{page}.html"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(f"Downloading {brand} page {page}")
            page_html = requests.get("https://www.ss.lv"+row_data.ss_url).text
            with open(path, "w") as file:
                file.write(page_html)
        page_no += 1

def download_all_pages(dist_dir):
    for brand,link in car_brands:
        download_brand_pages(brand,link,dist_dir)