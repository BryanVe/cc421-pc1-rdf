import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com/wiki/'
DEVIL_FRUITS = ["Gasu_Gasu_no_Mi"]


def get_devil_fruit(url):
    page = requests.get(BASE_URL+url)
    soup = BeautifulSoup(page.content, 'html.parser')

    divs = soup.find_all('div', class_="pi-item pi-data pi-item-spacing pi-border-color")

    meaning_value = ""
    first_value = ""
    type_value = ""
    user_value = ""

    name = soup.find_all('h2', {"data-source": "title"})[0].get_text()

    for div in divs:
        if div.get('data-source') == 'meaning':
            meaning_div = div
            meaning_value = meaning_div.find_all('div')[0].get_text()
        elif div.get('data-source') == 'first':
            first_div = div
            first_value = int(first_div.find_all('a')[1].get_text().replace("Episode ", ""))
        elif div.get('data-source') == 'type':
            type_div = div
            type_value = type_div.find_all('a')[0].get_text()
            if 'Zoan' in type_value:
                type_value = 'Zoan'
        elif div.get('data-source') == 'user':
            user_div = div
            user_value = user_div.find_all('a')[0].get_text()

    type_url = f'{BASE_URL}{type_value}'
    devil_fruit_info = {
        "name": name,
        "meaning": meaning_value,
        "first": first_value,
        "type": type_value,
        "type_url": type_url,
        "user": user_value,
        "url": url
    }

    return devil_fruit_info

# print(get_devil_fruit('Fuku_Fuku_no_Mi'))