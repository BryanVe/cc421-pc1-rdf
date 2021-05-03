import re
import requests
from bs4 import BeautifulSoup

AFFILIATIONS = [
    'Beasts_Pirates'
]

BASE_URL = 'https://onepiece.fandom.com/wiki/'
CLEAN_VALUE_REGEX = r'\[[0-9]+\]'

IGNORED_KEYS = [
    'ename',
    'extra1',
    'residency'
]


def format_value_by_key(key, div):
    value = div.find_all('div')[0].get_text()
    value = re.sub(CLEAN_VALUE_REGEX, '', value)

    if key == 'first':
        first = div.find_all('a')[1].get_text().replace('Episode ', '')

        return first
    elif key == 'affiliation':
        a_affiliations = div.find_all('a', attrs={"title": re.compile('.*')})
        affiliations = []

        for a_affiliation in a_affiliations:
            affiliations.append(a_affiliation.get_text())

        return affiliations
    elif key == 'bounty':
        return div.find_all('div')[0].get_text().split('[')[0]
    elif key == 'jva':
        a_jvas = div.find_all('a', attrs={'class': 'extiw'})
        jvas = []

        for a_jva in a_jvas:
            jvas.append(a_jva.get_text())

        return jvas
    return value


def get_affiliation_details(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    divs = soup.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')

    affiliation_data = {}
    for div in divs:
        key = div.get('data-source')

        if key not in IGNORED_KEYS:
            affiliation_data[key] = format_value_by_key(key, div)

    affiliation_data['url'] = url
    return affiliation_data
