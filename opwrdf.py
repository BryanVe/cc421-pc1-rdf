from rdflib import URIRef, Graph, Literal, BNode
from rdflib.namespace import ClosedNamespace, Namespace, RDFS, RDF

import constants
from constants import SHIPS, CHARACTERS, ORGANIZATIONS, DEVIL_FRUITS, BASE_URL
from graph_utils import convert_to_a_graph
from scrapper.affiliation_details import get_affiliation_details
from scrapper.character_details import get_character_details
from scrapper.devil_fruit import get_devil_fruit
from scrapper.devil_fruit_type import get_devil_fruit_types
from scrapper.geography_data import get_geography_data
from scrapper.ship import get_ship


class OpwRdf:
    def __init__(self):
        self.__closed_namespace = ClosedNamespace(
            uri=URIRef('https://onepiece.fandom.com/wiki/'),
            terms=["Blue_Sea",
                   "Ship",
                   "List_of_Canon_Characters",
                   "Category:Organizations",
                   "Devil_Fruit",
                   "List_of_Locations"
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
            "affiliation": URIRef("opw/affiliation"),
            "captain": URIRef("opw/captain"),
            "occupation": URIRef("opw/occupation"),
            "jname": URIRef("opw/japanese_name"),
            "residence": URIRef("opw/residence"),
            "age": URIRef("opw/age"),
            "birth": URIRef("opw/birthday"),
            "height": URIRef("opw/height"),
            "blood type": URIRef("opw/blood_type"),
            "bounty": URIRef("opw/bounty"),
            "dfname": URIRef("opw/devil_fruit"),
            "name": URIRef("opw/name"),
            "extra1": URIRef("opw/meaning_fruit_type"),
            "meaning": URIRef("opw/meaning"),
            "type": URIRef("opw/type"),
            "real name": URIRef("opw/real_name"),
            "ship": URIRef("opw/ship"),
            "population": URIRef("opw/population"),
            "region": URIRef("opw/region")
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

    def fill_oceans(self):
        for ocean in constants.OCEANS:
            ocean_object = get_geography_data(ocean)
            ocean_rdf = URIRef(ocean_object["uriRef"])

            self.__graph.add((ocean_rdf, RDFS.Class, self.__closed_namespace.Blue_Sea))

            for key in ocean_object:
                if key != 'uriRef':
                    self.__graph.add((ocean_rdf, self.__subject_properties[key], Literal(ocean_object[key])))

    def fill_ships(self):
        for ship in SHIPS:
            ship_object = get_ship(ship)
            ship_rdf = URIRef(ship_object["uriRef"])

            self.__graph.add((ship_rdf, RDFS.Class, self.__closed_namespace.Ship))

            for key in ship_object:
                if key not in ["uriRef", "affiliation"]:
                    self.__graph.add(
                        (ship_rdf, self.__subject_properties[key], Literal(ship_object[key])))

    def fill_devil_type_fruit(self):
        devil_type_objects = get_devil_fruit_types()
        for devilType in devil_type_objects:
            devil_type_ = URIRef(devilType["url"])
            self.__graph.add((devil_type_, RDFS.Class, self.__closed_namespace.Devil_Fruit))
            for key in devilType.keys():
                if key != 'url':
                    self.__graph.add((
                        devil_type_,
                        self.__subject_properties[key],
                        Literal(devilType[key])
                    ))

    def fill_devil_fruit(self):
        for d_fruit in DEVIL_FRUITS:
            d_fruit_object = get_devil_fruit(d_fruit)
            d_fruit_rdf = URIRef(constants.BASE_URL + d_fruit_object['url'])

            self.__graph.add((
                d_fruit_rdf,
                RDF.type,
                URIRef(d_fruit_object['type_url'])
            ))

            for key in d_fruit_object.keys():
                if key not in ['type', 'type_url', 'user', 'url']:
                    self.__graph.add((
                        d_fruit_rdf,
                        self.__subject_properties[key],
                        Literal(d_fruit_object[key])
                    ))

    def fill_residence(self, residence_uri):
        if residence_uri == "Sky_Island":
            return

        residence_object = get_geography_data(residence_uri)
        residence_rdf = URIRef(residence_object["uriRef"])

        self.__graph.add((
            residence_rdf,
            RDFS.Class,
            self.__closed_namespace.List_of_Locations
        ))

        for key in residence_object:
            if key not in ["uriRef"]:
                if key == "region":
                    self.__graph.add((
                        residence_rdf,
                        self.__subject_properties[key],
                        URIRef(constants.BASE_URL_NO_WIKI + residence_object["region"])
                    ))

                    self.fill_residence(residence_object["region"].replace("/wiki/", ""))
                else:
                    self.__graph.add((
                        residence_rdf,
                        self.__subject_properties[key],
                        Literal(residence_object[key])
                    ))

    def fill_characters(self):
        for character in CHARACTERS:
            character_object = get_character_details(character)
            character_rdf = URIRef(character_object["uriRef"])

            self.__graph.add((character_rdf, RDFS.Class, self.__closed_namespace.List_of_Canon_Characters))

            for key in character_object:
                if key not in [
                    "uriRef",
                    "jname",
                    "jva",
                    "age2",
                    "dfname2",
                    "dfename2",
                    "dfmeaning2",
                    "dftype2",
                    "dftype",
                    "dfename",
                    "dfmeaning"
                ]:
                    if key == "affiliation":
                        for affiliation in character_object["affiliation"]:
                            self.__graph.add((
                                character_rdf,
                                self.__subject_properties[key],
                                URIRef(constants.BASE_URL_NO_WIKI + affiliation["url"])
                            ))
                    elif key == "occupation":
                        for occupation in character_object["occupation"]:
                            self.__graph.add(
                                (character_rdf, self.__subject_properties[key], Literal(occupation))
                            )
                    elif key == "dfname":
                        self.__graph.add((
                            character_rdf,
                            self.__subject_properties[key],
                            URIRef(constants.BASE_URL_NO_WIKI + character_object[key]["url"])
                        ))
                    elif key == "residence":
                        for residence in character_object["residence"]:
                            self.__graph.add((
                                character_rdf,
                                self.__subject_properties[key],
                                URIRef(constants.BASE_URL_NO_WIKI + residence["url"])
                            ))

                            self.fill_residence(residence["url"].replace("/wiki/", ""))
                    else:
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
                # have to iterate on ship list
                if key == 'ship':
                    for ship in value:
                        ship_name = ship.replace(' ', '_')
                        self.__graph.add((uri_ref, self.__subject_properties[key], URIRef(f'{BASE_URL}{ship_name}')))
                elif key == 'captain':
                    captain = value.replace(' ', '_')
                    self.__graph.add((uri_ref, self.__subject_properties[key], URIRef(f'{BASE_URL}{captain}')))
                else:
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
                    self.__graph.add((URIRef(url), RDFS.subClassOf, URIRef(superior_class)))

    def test_inferences(self):
        # get all the organizations
        print('All organizations')
        for s in self.__graph.transitive_subjects(RDFS.Class, URIRef(f'{BASE_URL}Category:Organizations')):
            print(s)

        # get super classes of Marines
        print('Super classes of Marines')
        for s in self.__graph.transitive_subjects(URIRef(f'{BASE_URL}Marines'), RDFS.Class):
            print(s)

        # get the first episode of Gasu Gasu no Mi
        print('First episode Gasu Gasu no Mi')
        for s in self.__graph.transitive_objects(URIRef(f'{BASE_URL}Gasu_Gasu_no_Mi'),
                                                 self.__subject_properties['first']):
            print(s)

        # get the type of Gasu Gasu no Mi
        print('Type Gasu Gasu no Mi')
        for s in self.__graph.transitive_objects(URIRef(f'{BASE_URL}Gasu_Gasu_no_Mi'), RDF.type):
            print(s)

        # get all the devil fruits type Paramecia
        print('Devil Fruits type Paramecia')
        for s in self.__graph.transitive_subjects(RDF.type, URIRef(f'{BASE_URL}Paramecia')):
            print(s)


def create_xml():
    f = open("test.xml", "w+")
    f.write(opw_rdf.get_serialized_xml_graph())
    f.close()


# Example SPARQL
def get_ships(graph):
    ship_class = URIRef("https://onepiece.fandom.com/wiki/Ship")

    sparql_query = """
        SELECT DISTINCT ?s
        WHERE {
        ?s ?p ?o .
        }
        """

    results = graph.query(sparql_query, initBindings={'o': ship_class})
    return [str(result[0]) for result in results]


def get_ship_details(graph, ship_uri):
    sparql_query = """
    SELECT ?p ?o
    WHERE {
    ?s ?p ?o .
    }
    """

    return graph.query(sparql_query, initBindings={'s': ship_uri})


opw_rdf = OpwRdf()
print("Loading organizations ...")
opw_rdf.fill_organizations()
print("Loading ships ...")
opw_rdf.fill_ships()
print("Loading type fruits ...")
opw_rdf.fill_devil_type_fruit()
print("Loading  fruits...")
opw_rdf.fill_devil_fruit()
print("Loading characters ...")
opw_rdf.fill_characters()
print("Loading oceans ...")
opw_rdf.fill_oceans()

create_xml()

print("Creating image ...")
opw_rdf.save_as_image("test.png")

# for ship in get_ships(opw_rdf.get_graph()):
#     print(ship, ':')
#     for detail in get_ship_details(opw_rdf.get_graph(), URIRef(ship)):
#         print('- ', detail)
#     print('')


opw_rdf.test_inferences()
# print(opw_rdf.get_serialized_turtle_graph())
