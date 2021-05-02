import requests
from bs4 import BeautifulSoup


def get_new_world_statistics():
    url = "https://onepiece.fandom.com/wiki/New_World"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    new_world_data = {}
    statistics = soup.find("section", class_="pi-item pi-group pi-border-color")

    for data in zip(statistics.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color"),
                    statistics.find_all("div", class_="pi-data-value pi-font")):
        data_source = data[0].attrs["data-source"]
        new_world_data[data_source] = data[1].text

    del new_world_data["jname"]
    del new_world_data["extra1"]
    new_world_data["first"] = new_world_data.get("first")[-6:-3]

    return new_world_data
