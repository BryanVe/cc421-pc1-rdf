from rdflib import URIRef, Graph, Literal
from rdflib.namespace import ClosedNamespace, Namespace, RDFS

import constants
from graph_utils import convert_to_a_graph
from scrapper.ship import get_ship


class OpwRdf:
    def __init__(self):
        self.__closed_namespace = ClosedNamespace(
            uri=URIRef('https://onepiece.fandom.com/wiki/'),
            terms=["Blue_Sea", "rname", "ename", "first", "uriRef", "Ship", "status"]
        )

        self.__root_namespace = Namespace("/")
        self.__graph = self.__initialize_graph()
        self.__a_graph = None

        self.__subject_properties = {
            "rname": URIRef("rname"),
            "ename": URIRef("ename"),
            "first": URIRef("first"),
            "status": URIRef("status")
        }

    def get_graph(self):
        return self.__graph

    def __initialize_graph(self):
        __initial_graph = Graph()
        __initial_graph.bind("opw", self.__root_namespace)
        return __initial_graph

    def get_serialized_turtle_graph(self):
        return self.__graph.serialize(format="turtle").decode("utf-8")

    def get_serialized_xml_graph(self):
        return self.__graph.serialize(format="xml").decode("utf-8")

    def __set_a_graph(self):
        self.__a_graph = convert_to_a_graph(self.__graph)

    def save_as_image(self, name):
        self.__set_a_graph()
        self.__a_graph.draw(name)

    def fill_ships(self):
        for ship in constants.SHIPS:
            ship_object = get_ship(ship)
            ship_rdf = URIRef(ship_object["uriRef"])

            self.__graph.add((ship_rdf, RDFS.Class, self.__closed_namespace.Ship))

            for key in ship_object:
                if key not in ["uriRef", "affiliation"]:
                    self.__graph.add(
                        (ship_rdf, self.__subject_properties[key], Literal(ship_object[key])))


opw_rdf = OpwRdf()
opw_rdf.fill_ships()
opw_rdf.save_as_image("test.pdf")
