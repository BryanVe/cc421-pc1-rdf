import re

import requests
from bs4 import BeautifulSoup

CHARACTERS = [
    'Gol_D._Roger'
]

BASE_URL = 'https://onepiece.fandom.com/wiki/'
CLEAN_VALUE_REGEX = r'\[[0-9]+\]'
VALUES_SEPARATOR_REGEX = r'\n|;'
REMOVE_PARENTHESIS_REGEX = r'\(.*\)'
HEIGHT_REGEX = r'[0-9]+ cm'
AGES_REGEX = r'([0-9]+)(\s\([A-z\s]+\))?'
STRING_IN_QUOTES_REGEX = r'"[A-z-.\s]+"'

IGNORED_KEYS = [
    'Funi eva',
    '4kids eva',
    'Odex eva',
    'epithet',
    'alias'
]


def format_value_by_key(key, div):
    value = div.find_all('div')[0].get_text()
    value = re.sub(CLEAN_VALUE_REGEX, '', value)

    if key == 'first':
        first = div.div.find_all('a', recursive=False)[1].get_text().replace('Episode ', '')

        return first
    elif key == 'affiliation':
        a_affiliations = div.find_all('a', attrs={"title": re.compile('.*')})
        affiliations = []

        for a_affiliation in a_affiliations:
            affiliations.append({
                "url": a_affiliation.get('href'),
                "value": a_affiliation.get_text()
            })

        return affiliations
    elif key == 'occupation':
        return [raw_occupation.split(' (')[0].strip() for raw_occupation in value.split(';')]
    elif key == 'residence':
        a_residences = div.find_all('a', attrs={"title": re.compile('.*')})
        residences = []

        for a_residence in a_residences:
            residences.append(a_residence.get_text())

        return residences
    elif key == 'bounty':
        return div.find_all('div')[0].get_text().split('[')[0]
    elif key == 'height':
        heights = re.findall(HEIGHT_REGEX, div.find_all('div')[0].get_text())

        return heights[len(heights) - 1]
    elif key == 'age':
        ages = re.findall(AGES_REGEX, value)
        last_age = ages[len(ages) - 1][0]

        return last_age
    elif key == 'real name':
        real_name = value.split(' (')[0]
        romaji = div.find_all(class_='t_nihongo_romaji')[0].get_text()

        return f'{real_name} ({romaji})'
    elif key == 'jva':
        a_jvas = div.find_all('a', attrs={'class': 'extiw'})
        jvas = []

        for a_jva in a_jvas:
            jvas.append(a_jva.get_text())

        return jvas
    elif key == "dfname":
        return {
            "url": div.div.a.get("href"),
            "value": value
        }
    elif key == "dftype":
        return {
            "url": div.div.a.get("href"),
            "value": value
        }

    return value


def get_character_details(character):
    page = requests.get(BASE_URL + character)
    soup = BeautifulSoup(page.content, 'html.parser')

    divs = soup.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')

    character_data = {}
    for div in divs:
        key = div.get('data-source')

        if key not in IGNORED_KEYS:
            character_data[key] = format_value_by_key(key, div)
            character_data["uriRef"] = BASE_URL + character

    return character_data
