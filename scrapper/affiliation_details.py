import re
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup

CLEAN_VALUE_REGEX = r'\[[0-9]+\]'
IGNORED_KEYS = [
    'extra1',
    'residency',
    'jname',
    'leader',
    'occupation',
    'affiliation',
    'transportation',
    'extra2',
    'ename',
    'extra3'
]

def test(pattern, string):
    return bool(re.search(pattern, string))

def format_value_by_key(key, div):
    value = div.find_all('div')[0].get_text()
    value = re.sub(CLEAN_VALUE_REGEX, '', value)

    if key == 'first':
        first = div.find('a', attrs={"title": re.compile(r'Episode [0-9]+')}).get_text().replace('Episode ', '')

        return first
    elif key == 'bounty':
        return div.find_all('div')[0].get_text().split('[')[0]
    elif key == 'captain':
        a_captain = div.find('a', attrs={"title": re.compile('.*')})
        return a_captain.get_text()
    elif key == 'rname':
        return normalize('NFKD', value).encode('ASCII', 'ignore').decode("utf-8")
    elif key == 'ship':
        links = div.find_all('a', attrs={"title": re.compile(r'.*')})
        filtered_links = []

        for link in links:
            title = link.get('title')
            episode_regex = r'Episode [0-9]*'
            chapter_regex = r'Chapter [0-9]*'
            if not test(episode_regex, title) and not test(chapter_regex, title):
                filtered_links.append(link.get_text())

        return filtered_links
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
