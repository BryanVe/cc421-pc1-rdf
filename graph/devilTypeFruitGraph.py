from rdflib import Graph, Literal
from rdflib.namespace import URIRef, ClosedNamespace, RDFS, Namespace

from scrapper.devil_fruit_type import get_devil_fruit_types,DEVIL_FRUIT_TYPES


OPW = ClosedNamespace(
    uri=URIRef('https://onepiece.fandom.com/wiki/'),
    terms=["Devil_Fruit","rname", "first", "extra1", "url"]
)

'''
            "rname": r_name_value,
            "first": first_value,
            "extra1": extra_1_value,
            "url": BASE_URL + fruit
'''
r_name = URIRef("/rname")
first = URIRef("/first")
extra1 = URIRef("/extra1")

properties = {
    "rname": r_name,
    "extra1":extra1,
    "first": first
}
devilType_objects = get_devil_fruit_types()

def get_devilTypeFruitG(g):
    for devilType in devilType_objects:
        devilType_ = URIRef(devilType["url"])
        g.add((devilType_, RDFS.Class,OPW.Devil_Fruit))
        for key in devilType.keys():
            if key != 'url':
                g.add((devilType_, properties[key], Literal(devilType[key])))

    return g


ns1 = Namespace("/")
graphito = Graph()
graphito = get_devilTypeFruitG(graphito)
graphito.bind("opw", ns1)
print(graphito.serialize(format="xml").decode("utf-8"))
