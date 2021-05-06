import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com/wiki/'
MAIN_SHIPS = ['Nostra_Castello',
              'Red_Force',
              'Miss_Love_Duck',
              'Big_Top',
              'Going_Merry',
              'Hitsugibune',
              'Shark_Superb',
              'Striker',
              'Moby_Dick',
              'New_Witch%27s_Tongue',
              'Oro_Jackson',
              'Thousand_Sunny',
              'Thriller_Bark',
              'Piece_of_Spadille',
              'Polar_Tang',
              'Victoria_Punk',
              'Liberal_Hind',
              'Jewelry_Margherita',
              'Stay_Tune',
              'Grudge_Dolph',
              'Hanjomaru',
              'Perfume_Yuda',
              'Snapper_Head',
              'Sleeping_White_Horse_of_the_Forest',
              'Going_Luffy-senpai',
              'Naglfar',
              'Mammoth',
              'Queen_Mama_Chanter',
              'Tontatta_Pirates',
              'Saber_of_Xebec',
              'Numancia_Flamingo',
              'Wind_Granma']

ALL_SHIPS = []


def get_pirate_crews():
    for ship in MAIN_SHIPS:
        response = requests.get(BASE_URL + ship)
        html = BeautifulSoup(response.text, 'html.parser')
        data_dic = {}

        value = html.find("section", class_="pi-item pi-group pi-border-color")
        value2 = html.find_all("section", class_="pi-item pi-group pi-border-color")

        if len(value2) == 2:
            value = value2[1]

        for data in zip(value.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color"),
                        value.find_all("div", class_="pi-data-value pi-font")):
            data_source = data[0].attrs["data-source"]
            data_dic[data_source] = data[1].text

        # print(data_dic)

        if 'jname' in data_dic.keys():
            data_dic.pop('jname')
        if 'N/A' in data_dic['ename']:
            data_dic['ename'] = ship

        data_dic.setdefault('status', 'Unknown')
        if 'ename' not in data_dic.keys():
            if 'rname' in data_dic.keys():
                data_dic.setdefault('ename', data_dic['rname'])
            else:
                data_dic.setdefault('ename', 'Unknown')
        if 'first' not in data_dic.keys():
            data_dic.setdefault('first', 'Unknown')
        start = data_dic['first'].find('[')
        end = data_dic['first'].rfind(']')

        data_first = data_dic.get('first').replace(data_dic['first'][start:end + 1], '')
        data_t = data_first.split(', ') if (',' in data_first) else data_first.split('; ')

        if 'Chapter' in data_t[0]:
            data_dic['first'] = data_t[1]
        else:
            data_dic['first'] = data_t[0]

        ALL_SHIPS.append(data_dic)

    return ALL_SHIPS
