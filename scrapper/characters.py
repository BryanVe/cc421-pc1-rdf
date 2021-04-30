import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com'
LIST_OF_CHARACTERS_PATH = '/wiki/List_of_Canon_Characters'
URL = BASE_URL + LIST_OF_CHARACTERS_PATH


def get_characters():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    t_bodies = soup.find_all('tbody')[:-1]

    characters = []

    for t_body in t_bodies:
        tr_elements = t_body.find_all('tr')

        for tr in tr_elements:
            try:
                td = tr.find_all('td')[1]
                a = td.find_all('a')[0]

                character_info = {
                    "name": a.get('title'),
                    "url": BASE_URL + a.get('href')
                }

                characters.append(character_info)
            except IndexError as e:
                pass

    return characters
