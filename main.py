from rdflib import URIRef, Graph
from rdflib.namespace import ClosedNamespace, RDF

OPW = ClosedNamespace(
    uri=URIRef('https://onepiece.fandom.com/wiki/'),
    terms=["List_of_Canon_Characters"]
)

g = Graph()

monkey_d_luffy = URIRef("https://onepiece.fandom.com/wiki/Monkey_D._Luffy")

g.add((monkey_d_luffy, RDF.type, OPW.List_of_Canon_Characters))

def update_graph_for_fruits(g):
    gomi_gomi = URIRef("")

    # TODO more properties

    g.add()

    return g

print(g.serialize(format="xml").decode("utf-8"))
