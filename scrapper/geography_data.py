import re
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup


def get_geography_data(region):
    url = "https://onepiece.fandom.com/wiki/" + region

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    region_data = {}
    statistics = soup.find_all("section", class_="pi-item pi-group pi-border-color")
    if len(statistics) == 2:
        del statistics[0]

    for data in zip(statistics[0].find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color"),
                    statistics[0].find_all("div", class_="pi-data-value pi-font")):
        data_source = data[0].attrs["data-source"]

        if data_source == 'region':
            region_data[data_source] = data[0].find_all('a', attrs={"title": re.compile('.*')})[0].get("href")
        else:
            region_data[data_source] = data[1].text

    del region_data["jname"]
    if "extra1" in region_data:
        del region_data["extra1"]
    if "extra2" in region_data:
        del region_data["extra2"]
    if "first" in region_data:
        del region_data["first"]
    if "log" in region_data:
        del region_data["log"]

    unnormalized = region_data["rname"]

    region_data["rname"] = normalize('NFKD', unnormalized).encode('ASCII', 'ignore').decode("utf-8")
    region_data["uriRef"] = url

    return region_data
