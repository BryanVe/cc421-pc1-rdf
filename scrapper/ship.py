from unicodedata import normalize

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com/wiki/'
MAIN_SHIPS = ['Nostra_Castello', 'Red_Force', 'Miss_Love_Duck', 'Big_Top', 'Going_Merry', 'Hitsugibune', 'Shark_Superb',
              'Striker', 'Moby_Dick', 'New_Witch%27s_Tongue', 'Oro_Jackson', 'Thousand_Sunny', 'Thriller_Bark',
              'Piece_of_Spadille',
              'Polar_Tang', 'Victoria_Punk', 'Liberal_Hind', 'Jewelry_Margherita', 'Stay_Tune', 'Grudge_Dolph',
              'Hanjomaru', 'Perfume_Yuda',
              'Snapper_Head', 'Sleeping_White_Horse_of_the_Forest', 'Going_Luffy-senpai', 'Naglfar', 'Mammoth',
              'Queen_Mama_Chanter',
              'Tontatta_Pirates', 'Saber_of_Xebec', 'Numancia_Flamingo', 'Wind_Granma']
ALL_SHIPS = []


def get_ship(ship):
    """
    ship: end about the core, BASE_URL+ship = Core Url
    :rtype: dict
    """
    response = requests.get(BASE_URL + ship)
    html = BeautifulSoup(response.text, 'html.parser')
    dataDic = {}

    value = html.find("section", class_="pi-item pi-group pi-border-color")
    value2 = html.find_all("section", class_="pi-item pi-group pi-border-color")

    if len(value2) == 2:
        value = value2[1]

    for data in zip(value.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color"),
                    value.find_all("div", class_="pi-data-value pi-font")):
        data_source = data[0].attrs["data-source"]
        dataDic[data_source] = data[1].text

    # print(dataDic)

    if 'jname' in dataDic.keys():
        dataDic.pop('jname')
    # if 'N/A' in dataDic['ename']:
    #     dataDic['ename'] = ship

    dataDic.setdefault('status', 'Unknown')
    if 'ename' not in dataDic.keys():
        if 'rname' in dataDic.keys():
            dataDic.setdefault('ename', dataDic['rname'])
        else:
            dataDic.setdefault('ename', 'Unknown')
    if 'first' not in dataDic.keys():
        dataDic.setdefault('first', 'Unknown')
    start = dataDic['first'].find('[')
    end = dataDic['first'].rfind(']')

    dataFirst = dataDic['first'].replace(dataDic['first'][start:end + 1], '')
    dataT = dataFirst.split(', ') if (',' in dataFirst) else dataFirst.split('; ')

    if 'Chapter' in dataT[0]:
        dataDic['first'] = dataT[1]
    else:
        dataDic['first'] = dataT[0]

    if "rname" in dataDic.keys():
        dataDic["rname"] = normalize('NFKD', dataDic["rname"]).encode('ASCII', 'ignore').decode("utf-8")

    # ALL_SHIPS.append(dataDic)
    dataDic["uriRef"] = BASE_URL + ship

    if "birthday" in dataDic.keys():
        del dataDic["birthday"]
    if "extra1" in dataDic.keys():
        del dataDic["extra1"]
    if "extra2" in dataDic.keys():
        del dataDic["extra2"]

    return dataDic
