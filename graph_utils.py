import networkx as nx
from pygraphviz import AGraph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph


def convert_to_a_graph(rdf_graph):
    multi_di_graph = rdflib_to_networkx_multidigraph(rdf_graph)
    directed = multi_di_graph.is_directed()
    strict = nx.number_of_selfloops(multi_di_graph) == 0 and not multi_di_graph.is_multigraph()
    a_graph = AGraph(name=multi_di_graph.name, strict=strict, directed=directed)

    a_graph.graph_attr.update(multi_di_graph.graph.get("graph", {
        'label': 'Network Map',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
        'overlap': 'scalexy',
        'splines': 'true'
    }))
    a_graph.node_attr.update(multi_di_graph.graph.get("node", {
        'fontname': 'Helvetica',
        'fontcolor': 'white',
        'color': '#006699',
        'style': 'filled',
        'fillcolor': '#006699',
    }))
    a_graph.edge_attr.update(multi_di_graph.graph.get("edge", {
        'style': 'dashed',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '14',
        'fontcolor': 'white',
    }))

    a_graph.graph_attr.update(
        (k, v) for k, v in multi_di_graph.graph.items() if k not in ("graph", "node", "edge")
    )

    for n, node_data in multi_di_graph.nodes(data=True):
        a_graph.add_node(n)
        a = a_graph.get_node(n)
        a.attr.update({k: str(v) for k, v in node_data.items()})

    if multi_di_graph.is_multigraph():
        for u, v, key, edge_data in multi_di_graph.edges(data=True, keys=True):
            str_edge_data = {k: str(v) for k, v in edge_data.items() if k != "key"}
            a_graph.add_edge(u, v, headlabel=str(key))
            a = a_graph.get_edge(u, v)
            a.attr.update(str_edge_data)

    a_graph.layout()

    return a_graph
