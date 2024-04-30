from car_brands import car_brands
import os
from tqdm import tqdm
from download_html import download_all_pages
from extract_data import extract_to_jsons
import json

script_dir = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(script_dir)
dist_path = os.path.join(root_path, "dist")

# download_all_pages(dist_path)

# extract_to_jsons(dist_path)

price_lb = 3000
price_ub = 12000
year_lb = 2005
year_ub = 2015
power_lb = 200
gearbox = "Automatic"

all_cars = []
for file in tqdm(os.listdir(os.path.join(dist_path, "JSON"))):
    with open(os.path.join(dist_path, "JSON", file), "r") as f:
        content = f.read()
        data = json.loads(content)
        keys = list(data.keys())
        for key in keys:
            car = data[key]
            car["id"] = key
            if car["price"]>price_ub or car["price"]<price_lb:
                continue
            if car["year"]>year_ub or car["year"]<year_lb:
                continue
            if car["power"]<power_lb:
                continue
            all_cars.append(car)

print(len(all_cars))