from rdflib import URIRef, Graph
from rdflib.namespace import ClosedNamespace, Namespace


class OpwRdf:
    def __init__(self):
        self.public_namespace = ClosedNamespace(
            uri=URIRef('https://onepiece.fandom.com/wiki/'),
            terms=["Blue_Sea", "rname", "ename", "first", "uriRef"]
        )

        self.root_namespace = Namespace("/")
        self.graph = self.__initialize_graph()

        self.properties = {
            "rname": URIRef("/rname"),
            "ename": URIRef("/ename"),
            "first": URIRef("/first"),
        }

    def __initialize_graph(self):
        __initial_graph = Graph()
        __initial_graph.bind("opw", self.root_namespace)
        return __initial_graph

    def get_serialized_graph(self):
        return self.graph.serialize(format="xml").decode("utf-8")

