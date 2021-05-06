from rdflib import Graph, Literal
from rdflib.namespace import URIRef, ClosedNamespace, RDFS, Namespace

from scrapper.geography_data import get_geography_data

oceans = ["North_Blue",
          "South_Blue",
          "East_Blue",
          "West_Blue",
          "Grand_Line"]

OPW = ClosedNamespace(
    uri=URIRef('https://onepiece.fandom.com/wiki/'),
    terms=["Blue_Sea", "rname", "ename", "first", "uriRef"]
)

ns1 = Namespace("/")

graphito = Graph()

r_name = URIRef("/rname")
e_name = URIRef("/ename")
first = URIRef("/first")

properties = {
    "rname": r_name,
    "ename": e_name,
    "first": first,
}


def get_oceans(g):
    for ocean in oceans:
        ocean_object = get_geography_data(ocean)
        ocean_ = URIRef(ocean_object["uriRef"])

        g.add((ocean_, RDFS.Class, OPW.Blue_Sea))

        for key in ocean_object:
            if key != 'uriRef':
                g.add((ocean_, properties[key], Literal(ocean_object[key])))

    return g


graphito = get_oceans(graphito)
graphito.bind("opw", ns1)
print(graphito.serialize(format="xml").decode("utf-8"))
