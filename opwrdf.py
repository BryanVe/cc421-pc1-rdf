from rdflib import URIRef, Graph, Literal
from rdflib.namespace import ClosedNamespace, Namespace, RDFS

from constants import SHIPS, CHARACTERS, ORGANIZATIONS, BASE_URL
from graph_utils import convert_to_a_graph
from scrapper.affiliation_details import get_affiliation_details
from scrapper.character_details import get_character_details
from scrapper.ship import get_ship


class OpwRdf:
    def __init__(self):
        self.__closed_namespace = ClosedNamespace(
            uri=URIRef('https://onepiece.fandom.com/wiki/'),
            terms=["Blue_Sea",
                   "Ship",
                   "List_of_Canon_Characters",
                   "Category:Organizations",
                   "Devil_Fruit"
                   ]
        )

        self.__root_namespace = Namespace("opw/")
        self.__graph = self.__initialize_graph()
        self.__a_graph = None

        self.__subject_properties = {
            "rname": URIRef("opw/romaji_name"),
            "ename": URIRef("opw/english_name"),
            "first": URIRef("opw/first_episode"),
            "status": URIRef("opw/status"),
            # TODO Affiliation must be another instance
            "affiliation": URIRef("opw/affiliation"),
            "captain": URIRef("opw/captain"),
            # TODO Occupation must be another instance
            "occupation": URIRef("opw/occupation"),
            "jname": URIRef("opw/japanese_name"),
            # TODO Residence must be another instance
            "residence": URIRef("opw/residence"),
            "age": URIRef("opw/age"),
            "birth": URIRef("opw/birthday"),
            "height": URIRef("opw/height"),
            "blood type": URIRef("opw/blood_type"),
            "bounty": URIRef("opw/bounty"),
            # TODO Devil fruit must be another instance (?)
            "dfname": URIRef("opw/devil_fruit_name"),
            # TODO Devil fruit english must be from another instance (?)
            # "dfename": URIRef("opw/devil_fruit_english_name"),
            "dfirst": URIRef("opw/devil_fruit_debut"),
            # TODO Devil fruit meaning must be from another instance (?)
            "dfmeaning": URIRef("opw/devil_fruit_meaning"),
            # TODO Devil fruit type must be another instance (?)
            # "dftype": URIRef("opw/devil_fruit_type"),
            "real name": URIRef("opw/real_name")
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

    def __connect_main_class_and_characteristics(self, organization):
        url = f'{BASE_URL}{organization}'
        data = get_affiliation_details(url)
        uri_ref = URIRef(url)

        self.__graph.add((uri_ref, RDFS.Class, self.__closed_namespace['Category:Organizations']))
        for key, value in data.items():
            if key != 'url':
                self.__graph.add((uri_ref, self.__subject_properties[key], Literal(value)))

        return url, data

    def fill_organizations(self):
        for organization in ORGANIZATIONS:
            if isinstance(organization, str):
                self.__connect_main_class_and_characteristics(organization)

            elif isinstance(organization, dict):
                value = organization['value']
                sub_items = organization['sub_items']

                superior_class, _ = self.__connect_main_class_and_characteristics(value)

                for sub_item in sub_items:
                    url, data = self.__connect_main_class_and_characteristics(sub_item)
                    self.__graph.add((URIRef(url), RDFS.Class, URIRef(superior_class)))


opw_rdf = OpwRdf()
print("Loading organizations ...")
opw_rdf.fill_organizations()
print("Loading ships ...")
opw_rdf.fill_ships()
print("Loading characters ...")
opw_rdf.fill_characters()
print(opw_rdf.get_serialized_turtle_graph())
# print("Creating image ...")
# opw_rdf.save_as_image("test.png")
