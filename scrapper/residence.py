import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://onepiece.fandom.com/wiki/'
RESIDENCE = ['Loguetown', 'Foosha_Village', 'Mt._Colubo', 'Rusukaina', 'Shimotsuki_Village', 'Kuraigana_Island',
             'Skypiea', 'Fish-Man_Island', 'G-5', 'Zou', 'Wano_Country',
             'Karai_Bari_Island', 'Baterilla', 'Orange_Town', 'Cocoyasi_Village', 'Weatheria', 'Syrup_Village',
             'Boin_Archipelago', 'Baratie', 'Germa_Kingdom', 'Momoiro_Island',
             'Drum_Island', 'Torino_Kingdom', 'Ohara', 'Arabasta_Kingdom', 'Baltigo', 'Water_7', 'Karakuri_Island',
             'Florian_Triangle', 'Namakura_Island', 'Fish-Man_District',
             'Mary_Geoise', 'Spider_Miles', 'Dressrosa', 'Komugi_Island', 'Flevance', 'Amazon_Lily', 'Udon', 'Kuri',
             'Arlong_Park', 'Gray_Terminal', 'Shells_Town', 'Fish-Man_Island',
             'Goat_Island', 'Goa_Kingdom', 'Mt._Colubo', 'Swallow_Island', 'Sphinx_(Location)', 'Sabaody_Archipelago']

ALL_RESIDENCE = []
def get_residence():
    for resid in RESIDENCE:
        response = requests.get(BASE_URL + resid)
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

        if 'affiliation' in dataDic.keys():
            dataDic.pop('affiliation')
        if 'log' in dataDic.keys():
            dataDic.pop('log')
        if 'population' in dataDic.keys():
            dataDic.pop('population')
        if 'jname' in dataDic.keys():
            dataDic.pop('jname')
        if 'type' in dataDic.keys():
            dataDic.pop('type')
        if 'status' in dataDic.keys():
            dataDic.pop('status')
        # print(dataDic)
        if 'N/A' in dataDic['ename']:
            dataDic['ename'] = resid

        dataTC = dataDic['ename'].split(';') if (';' in dataDic['ename']) else dataDic['ename'].split(',')
        dataDic['ename'] = dataTC
        if len(dataTC) > 1:
            dataTCArray = []
            for com in dataDic['ename']:
                start = com.find('(')
                end = com.find(')')
                dataC = com.replace(com[start:end + 1], '')
                if '\xa0*' in dataC:
                    dataC = dataC.replace('\xa0*', '')

                dataTCArray.append(dataC)

            dataDic['ename'] = dataTCArray

        else:
            if '\xa0*' in dataTC[0]:
                dataTC[0] = dataTC[0].split('\xa0*')
            dataDic['ename'] = dataTC[0]

        for k in dataDic.keys():
            dataT = []
            if '[' in dataDic[k]:
                # print(k)
                start = dataDic[k].find('[')
                end = dataDic[k].rfind(']')
                dataFirst = dataDic[k].replace(dataDic[k][start:end + 1], '')
                dataT = dataFirst.split(',') if (',' in dataFirst) else dataFirst.split(';')
                # print(dataT)
            elif ';' in dataDic[k]:
                dataT = dataDic[k].split(';')
            if len(dataT) > 1 and k == 'first':
                for epi in dataT:
                    if 'Chapter' not in epi:
                        dataDic['first'] = epi

            else:
                if k == 'first':
                    dataDic['first'] = dataT[0]
            if ';' in dataDic[k]:
                dataT = dataDic[k].split(';')
                dataDic[k] = dataT

        print(dataDic)
        ALL_RESIDENCE.append(dataDic)

    return  ALL_RESIDENCE