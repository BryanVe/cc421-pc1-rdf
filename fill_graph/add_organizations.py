from rdflib import Graph, Literal
from rdflib.namespace import URIRef, RDFS

import constants
from scrapper.affiliation_details import get_affiliation_details
from fill_graph.rdf_config import ns1, OPW

BASE_URL = 'https://onepiece.fandom.com/wiki/'

AVAILABLE_PROPERTIES = [
    'rname',
    'ename',
    'first',
    'status',
    'url',
    'bounty'
]

MAIN_CLASS = 'Category:Organizations'

g = Graph()


def fetch_data(organization):
    url = f'{BASE_URL}{organization}'
    data = get_affiliation_details(url)

    return url, data


def connect_main_class_and_characteristics(organization, graph):
    url, data = fetch_data(organization)
    uri_ref = URIRef(url)

    graph.add((uri_ref, RDFS.Class, OPW[MAIN_CLASS]))
    for key, value in data.items():
        if key != 'url':
            graph.add((uri_ref, URIRef(f'/{key}'), Literal(value)))

    return url, data


def map_organizations(graph):
    for organization_node in constants.ORGANIZATIONS:
        if isinstance(organization_node, str):
            connect_main_class_and_characteristics(organization_node, graph)

        elif isinstance(organization_node, dict):
            value = organization_node['value']
            sub_items = organization_node['sub_items']

            superior_class, _ = connect_main_class_and_characteristics(value, graph)

            for sub_item in sub_items:
                url, data = connect_main_class_and_characteristics(sub_item, graph)
                graph.add((URIRef(url), RDFS.Class, URIRef(superior_class)))

    return graph


g = map_organizations(g)
g.bind("opw", ns1)
print(g.serialize(format="n3").decode("utf-8"))
