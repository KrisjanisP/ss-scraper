from car_brands import car_brands
import os
from tqdm import tqdm
from download_html import download_all_pages
from extract_data import extract_to_jsons
import json
import jinja2

script_dir = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(script_dir)
dist_path = os.path.join(root_path, "dist")

# download_all_pages(dist_path)

# extract_to_jsons(dist_path)

price_lb = 3000
price_ub = 12000
year_lb = 2005
year_ub = 2015
power_lb = 180
power_ub = 500
gearbox = "Automatic"

all_cars = []
for file in os.listdir(os.path.join(dist_path, "JSON")):
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
            if car["power"]<power_lb or car["power"]>power_ub:
                continue
            car["description"] = car["description"].strip()[:100].split("\n")[0]
            car["ss_url"] = f"https://www.ss.lv/msg/lv/transport/cars/{key}.html"
            all_cars.append(car)
# sort by price
all_cars.sort(key=lambda x: x["price"])

# load jinja2 template
templateLoader = jinja2.FileSystemLoader(searchpath=os.path.join(script_dir, "templates"))
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "table.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(cars=all_cars)
with open(os.path.join(dist_path, "index.html"), "w") as f:
    f.write(outputText)