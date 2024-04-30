from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from car_brands import car_brands
import os
import json
import re
from tqdm import tqdm

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

def extract_full_data(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    res = dict()
    msg_div = soup.find("div", id="msg_div_msg")
    if msg_div:
        res["description"] = msg_div.text
    # find all td with id tdo_*
    tds = soup.find_all("td", id=re.compile(r"tdo_\d+"))
    for td in tds:
        key = td.get("id")
        value = td.text
        res[key] = value
    return res
    
def extract_to_jsons(dist_path):
    for brand,link in tqdm(car_brands):
        ss_dict = dict()
        html_dir_path = os.path.join(dist_path,"HTML",brand)
        rows_path = os.path.join(html_dir_path,"rows")
        full_path = os.path.join(html_dir_path,"full")

        for file in os.listdir(rows_path):
            with open(os.path.join(rows_path,file),"r") as f:
                content = f.read()
                rows = extract_rows(content)
                for row in rows:
                    row_data = extract_row_data(row)
                    ss_url = row_data.ss_url
                    ss_id = ss_url.split("/")[-1].split(".")[0]
                    ss_dict[ss_id] = dict()
                    ss_dict[ss_id]["tiny_img_url"] = row_data.tiny_img_src
                    ss_dict[ss_id]["brand"] = brand
                    ss_dict[ss_id]["model"] = row_data.model
                    ss_dict[ss_id]["price"] = row_data.price
        
        for file in os.listdir(full_path):
            with open(os.path.join(full_path,file),"r") as f:
                content = f.read()
                ss_id = file.split(".")[0]
                data = extract_full_data(content)
                ss_dict[ss_id].update(data)
        ss_ids = list(ss_dict.keys())
        for ss_id in ss_ids:
            if "buy " in ss_dict[ss_id]["price"]:
                del ss_dict[ss_id]
                continue
            if "tdo_223" in ss_dict[ss_id]:
                if "Without" in ss_dict[ss_id]["tdo_223"]:
                    del ss_dict[ss_id]
                    continue
            if "tdo_1678" in ss_dict[ss_id]:
                del ss_dict[ss_id]["tdo_1678"]
            if "tdo_1714" in ss_dict[ss_id]:
                del ss_dict[ss_id]["tdo_1714"]
            del ss_dict[ss_id]["tdo_31"]
            if "tdo_18" not in ss_dict[ss_id]:
                # print(ss_dict[ss_id])
                del ss_dict[ss_id]
                continue
            year = ss_dict[ss_id]["tdo_18"][:4]
            del ss_dict[ss_id]["tdo_18"]
            if not year.isdigit():
                del ss_dict[ss_id]
                continue
            ss_dict[ss_id]["year"] = int(year)

            price = ss_dict[ss_id]["price"]
            if "\u20ac" not in price:
                del ss_dict[ss_id]
                continue
            price = price.split("\u20ac")[0].strip().replace(",","")
            if price == "-":    
                del ss_dict[ss_id]
                continue
            if not price.isdigit():
                del ss_dict[ss_id]
                continue
            ss_dict[ss_id]["price"] = int(price)
            
            if "tdo_35" not in ss_dict[ss_id]:
                del ss_dict[ss_id]
                continue
            if "tdo_16" not in ss_dict[ss_id]:
                del ss_dict[ss_id]
                continue
            mileage = ss_dict[ss_id]["tdo_16"]
            mileage = mileage.replace(" ","")
            if not mileage.isdigit():
                del ss_dict[ss_id]
                continue
            ss_dict[ss_id]["mileage"] = int(mileage)
            del ss_dict[ss_id]["tdo_16"]
            if "tdo_1716" in ss_dict[ss_id]:
                del ss_dict[ss_id]["tdo_1716"]
            if "tdo_17" not in ss_dict[ss_id]:
                del ss_dict[ss_id]
                continue
            color = ss_dict[ss_id]["tdo_17"].split("\u00a0")[0].strip()
            ss_dict[ss_id]["color"] = color
            del ss_dict[ss_id]["tdo_17"]
            
            if "tdo_8" in ss_dict[ss_id]:
                del ss_dict[ss_id]["tdo_8"]
            
            if "tdo_1293" in ss_dict[ss_id]:
                del ss_dict[ss_id]["tdo_1293"]
        
            # try to find kw 
            pattern = r'\d+\s*[kK][wW]'
            matches = re.findall(pattern, ss_dict[ss_id]["description"])
            if len(matches) == 1:
                kw = matches[0].split("k")[0].split("K")[0].strip()
                if kw.isdigit():
                    ss_dict[ss_id]["power"] = int(kw)
                else:
                    print(kw)
                    del ss_dict[ss_id]
                continue
            # try to find hp
            pattern = r'\d+\s*[hH][pP]'
            matches = re.findall(pattern, ss_dict[ss_id]["description"])
            if len(matches) == 1:
                hp = matches[0].split("h")[0].split("H")[0].strip()
                if hp.isdigit():
                    ss_dict[ss_id]["power"] = int(int(hp)/1.36)
                else:
                    print(hp)
                    del ss_dict[ss_id]
                continue
            # try to find zs (the same as hp)
            pattern = r'\d+\s*[zZ][sS]'
            matches = re.findall(pattern, ss_dict[ss_id]["description"])
            if len(matches) == 1:
                hp = matches[0].split("z")[0].split("Z")[0].strip()
                if hp.isdigit():
                    ss_dict[ss_id]["power"] = int(int(hp)/1.36)
                else:
                    print(hp)
                    del ss_dict[ss_id]
                continue
            del ss_dict[ss_id]
        
            
        json_dir_path = os.path.join(dist_path,"JSON")
        os.makedirs(json_dir_path,exist_ok=True)
        # save as json 
        with open(os.path.join(json_dir_path,f"{brand}.json"),"w") as f:
            json.dump(ss_dict,f) 