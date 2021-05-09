from rdflib import Graph, Literal
from rdflib.namespace import URIRef, ClosedNamespace, RDFS, Namespace, RDF

from scrapper.devil_fruit import get_devil_fruit
from scrapper.devil_fruit_type import get_devil_fruit_types


BASE_URL = 'https://onepiece.fandom.com/wiki/'
DEVIL_FRUITS = ["Gasu_Gasu_no_Mi","Gomu_Gomu_no_Mi","Bara_Bara_no_Mi","Hana_Hana_no_Mi","Mane_Mane_no_Mi",
                "Bane_Bane_no_Mi","Ito_Ito_no_Mi","Yomi_Yomi_no_Mi","Horo_Horo_no_Mi","Hito_Hito_no_Mi",
                "Uo_Uo_no_Mi,_Model:_Seiryu","Ryu_Ryu_no_Mi,_Model:_Pteranodon","Zou_Zou_no_Mi,_Model:_Mammoth",
                "Ryu_Ryu_no_Mi,_Model:_Allosaurus","Wara_Wara_no_Mi","Beta_Beta_no_Mi","Hira_Hira_no_Mi",
                "Ishi_Ishi_no_Mi","Mochi_Mochi_no_Mi","Nagi_Nagi_no_Mi","Yami_Yami_no_Mi","Gura_Gura_no_Mi",
                "Ope_Ope_no_Mi","SMILE","Shiro_Shiro_no_Mi","Tori_Tori_no_Mi,_Model:_Phoenix","Nikyu_Nikyu_no_Mi",
                "Horu_Horu_no_Mi","Mero_Mero_no_Mi","Suna_Suna_no_Mi","Magu_Magu_no_Mi","Toki_Toki_no_Mi",
                "Pika_Pika_no_Mi","Zushi_Zushi_no_Mi","Mera_Mera_no_Mi","Fuku_Fuku_no_Mi",
                "Hie_Hie_no_Mi","Doru_Doru_no_Mi"]

name = URIRef("/rname")
meaning = URIRef("/meaning")
first = URIRef("/first")

properties = {
    "name": name,
    "first": first,
    "meaning": meaning,
}

OPW = ClosedNamespace(
    uri=URIRef('https://onepiece.fandom.com/wiki/'),
    terms=["Devil_Fruit","name", "meaning", "first", "type", "type_url", "user","url"]
)
'''
        "name": name,
        "meaning": meaning_value,
        "first": first_value,
        "type": type_value,
        "type_url": type_url,
        "user": user_value,
        "url": url
'''

def get_devilFruitG(graph):
    for dfruit in DEVIL_FRUITS:
        dfruit_object = get_devil_fruit(dfruit)
        dfruit_url = URIRef(dfruit_object['url'])
        print(dfruit_object['type_url'])
        print(dfruit)
        graph.add((dfruit_url,RDF.type,OPW.Devil_Fruit))
        for key in dfruit_object.keys():
            if key != 'url':
                if key == 'type':
                    graph.add((dfruit_url,RDF.type,URIRef(dfruit_object['type_url'])))
                if key not in ['type','type_url','user']:
                    graph.add((dfruit_url,properties[key],Literal(dfruit_object[key])))
    return graph


ns1 = Namespace("/")

devilFGraph = Graph()
devilFGraph = get_devilFruitG(devilFGraph)
devilFGraph.bind("opw", ns1)
print(devilFGraph.serialize(format="xml").decode("utf-8"))
