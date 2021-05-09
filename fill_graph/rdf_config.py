from rdflib.namespace import URIRef, ClosedNamespace, Namespace

OPW = ClosedNamespace(
    uri=URIRef('https://onepiece.fandom.com/wiki/'),
    terms=[
        'Blue_Sea',
        'rname',
        'ename',
        'first',
        'url',
        'bounty',
        'captain',
        'Category:Organizations'
    ]
)

ns1 = Namespace("/")
