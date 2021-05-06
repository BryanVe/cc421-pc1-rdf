import requests
import re
from bs4 import BeautifulSoup

def get_geography_data(region):
  url = "https://onepiece.fandom.com/wiki/" + region

  response = requests.get(url)

  soup = BeautifulSoup(response.text, 'html.parser')
  region_data = {}
  statistics = soup.find_all("section", class_="pi-item pi-group pi-border-color")
  if len(statistics) == 2:
    del statistics[0]
  for data in zip(statistics[0].find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color"), statistics[0].find_all("div", class_="pi-data-value pi-font")):
    data_source = data[0].attrs["data-source"]
    region_data[data_source] = data[1].text

  
  del region_data["jname"]
  if "extra1" in region_data:
    del region_data["extra1"]
  if "extra2" in region_data:
    del region_data["extra2"]
  
  numbers = [s for s in re.findall(r'-?\d+\.?\d*', region_data.get("first"))]
  if len(numbers[-1]) == 1:
    del numbers[-1]
  region_data["first"] = numbers[-1]

  return region_data