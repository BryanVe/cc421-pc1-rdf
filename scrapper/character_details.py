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
    'Odex eva'
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
    elif key == 'occupation':
        raw_occupations = value.split(';')

        occupations = []
        for raw_occupation in raw_occupations:
            occupations.append(raw_occupation.split(' (')[0].strip())

        return occupations
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
    elif key == 'alias':
        alias = re.findall(STRING_IN_QUOTES_REGEX, value)
        romajis = div.find_all(class_='t_nihongo_romaji')

        results = []
        for index in range(len(romajis)):
            cleaned_alias = alias[index].replace('"', '')
            cleaned_romaji = romajis[index].get_text()

            results.append(f'{cleaned_alias} ({cleaned_romaji})')

        return results
    elif key == 'epithet':
        epithet = re.findall(STRING_IN_QUOTES_REGEX, value)
        romajis = div.find_all(class_='t_nihongo_romaji')

        results = []
        for index in range(len(romajis)):
            cleaned_epithet = epithet[index].replace('"', '')
            cleaned_romaji = romajis[index].get_text()

            results.append(f'{cleaned_epithet} ({cleaned_romaji})')

        return results
    elif key == 'jva':
        a_jvas = div.find_all('a', attrs={'class': 'extiw'})
        jvas = []

        for a_jva in a_jvas:
            jvas.append(a_jva.get_text())

        return jvas
    return value


def get_character_details(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    divs = soup.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color')

    character_data = {}
    for div in divs:
        key = div.get('data-source')

        if key not in IGNORED_KEYS:
            character_data[key] = format_value_by_key(key, div)

    return character_data