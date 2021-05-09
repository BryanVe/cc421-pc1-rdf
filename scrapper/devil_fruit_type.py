import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com/wiki/'
DEVIL_FRUIT_TYPES = ["Logia", "Paramecia", "Zoan"]


def get_devil_fruit_types():
    devil_fruit_type_list = []

    for fruit in DEVIL_FRUIT_TYPES:
        page = requests.get(BASE_URL + fruit)
        soup = BeautifulSoup(page.content, 'html.parser')

        divs = soup.find_all('div', class_="pi-item pi-data pi-item-spacing pi-border-color")

        r_name_value = ""
        first_value = ""
        extra_1_value = ""

        for div in divs:
            if div.get('data-source') == 'rname':
                r_name_div = div
                r_name_value = r_name_div.find_all('i')[0].get_text()
            elif div.get('data-source') == 'first':
                first_div = div
                first_value = int(first_div.find_all('a')[1].get_text().replace("Episode ", ""))
            elif div.get('data-source') == 'extra1':
                extra_1_div = div
                extra_1_value = extra_1_div.find_all('div')[0].get_text()

        devil_fruit_type_info = {
            "rname": r_name_value,
            "first": first_value,
            "extra1": extra_1_value,
            "url": BASE_URL + fruit
        }

        devil_fruit_type_list.append(devil_fruit_type_info)

    return devil_fruit_type_list

