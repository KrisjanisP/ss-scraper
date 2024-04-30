from car_brands import car_brands
from downl_brand_pages import download_brand_pages

for brand,link in car_brands:
    download_brand_pages(brand,link,"dist")    