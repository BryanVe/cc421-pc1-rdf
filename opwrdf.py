from rdflib import URIRef, Graph, Literal
from rdflib.namespace import ClosedNamespace, Namespace, RDFS

from constants import SHIPS, CHARACTERS
from graph_utils import convert_to_a_graph
from scrapper.character_details import get_character_details
from scrapper.ship import get_ship


class OpwRdf:
    def __init__(self):
        self.__closed_namespace = ClosedNamespace(
            uri=URIRef('https://onepiece.fandom.com/wiki/'),
            terms=["Blue_Sea", "rname", "ename", "first", "uriRef", "Ship", "status", "List_of_Canon_Characters"]
        )

        self.__root_namespace = Namespace("/")
        self.__graph = self.__initialize_graph()
        self.__a_graph = None

        self.__subject_properties = {
            "rname": URIRef("romaji_name"),
            "ename": URIRef("english_name"),
            "first": URIRef("first_episode"),
            "status": URIRef("status"),
            # TODO Affiliation must be another instance
            "affiliation": URIRef("affiliation"),
            # TODO Occupation must be another instance
            "occupation": URIRef("occupation"),
            "jname": URIRef("japanese_name"),
            # TODO Residence must be another instance
            "residence": URIRef("residence"),
            "age": URIRef("age"),
            "birth": URIRef("birthday"),
            "height": URIRef("height"),
            "blood type": URIRef("blood_type"),
            "bounty": URIRef("bounty"),
            # TODO Devil fruit must be another instance (?)
            "dfname": URIRef("devil_fruit_name"),
            # TODO Devil fruit english must be from another instance (?)
            "dfename": URIRef("devil_fruit_english_name"),
            # TODO Devil fruit meaning must be from another instance (?)
            "dfmeaning": URIRef("devil_fruit_meaning"),
            # TODO Devil fruit type must be another instance (?)
            "dftype": URIRef("devil_fruit_meaning"),
            "real name": URIRef("real_name")
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
        for ship in SHIPS:
            ship_object = get_ship(ship)
            ship_rdf = URIRef(ship_object["uriRef"])

            self.__graph.add((ship_rdf, RDFS.Class, self.__closed_namespace.Ship))

            for key in ship_object:
                if key not in ["uriRef", "affiliation"]:
                    self.__graph.add(
                        (ship_rdf, self.__subject_properties[key], Literal(ship_object[key])))

    def fill_characters(self):
        for character in CHARACTERS:
            character_object = get_character_details(character)
            character_rdf = URIRef(character_object["uriRef"])

            self.__graph.add((character_rdf, RDFS.Class, self.__closed_namespace.List_of_Canon_Characters))

            for key in character_object:
                if key not in ["uriRef", "jname", "jva", "age2", "dfname2", "dfename2", "dfmeaning2", "dftype2"]:
                    self.__graph.add(
                        (character_rdf, self.__subject_properties[key], Literal(character_object[key]))
                    )


opw_rdf = OpwRdf()
print("Loading ships ...")
opw_rdf.fill_ships()
print("Loading characters ...")
opw_rdf.fill_characters()
print("Creating image ...")
opw_rdf.save_as_image("test.png")
