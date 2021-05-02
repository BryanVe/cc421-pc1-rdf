from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib import Graph, ConjunctiveGraph
from rdflib.namespace import RDF, FOAF,RDFS

from scrapper.character_details import get_character_details

GLOBAL_URL = 'https://onepiece.fandom.com/wiki/'
op = Namespace(GLOBAL_URL)

zoroDic = get_character_details(GLOBAL_URL+'Roronoa_Zoro')
print(zoroDic)

# Generate Graph

#opWorld = ConjunctiveGraph()
#opWorld = Graph()


## Characterostic

rname = URIRef('characteristic:rname')
ename = URIRef('characteristic:ename')
first = URIRef('characteristic:debut')
alias = URIRef('characteristic:alias')
## falta

# General categories

"""
 - Devil Fruit types
 - geograpphy (red line, blue line, new world)
  - Pirate Crews
"""

# Sub categories and

"""
 - Residence
 - Fruits 
 - Raza <- (falta)
 - Ocupation
 - ships
"""
# Non characters instances
"""
 - Residence
 - Fruits 
 - ships
"""

# Characters instances


# Properties
# RDFS.subPropertyO

# Labels definition


# generate triplet