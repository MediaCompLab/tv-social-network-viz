import json
import networkx as nx
import numpy as np

def get_graph_diff(g1, g2):
    g1 = nx.node_link_graph(json.loads(g1))
    g2 = nx.node_link_graph(json.loads(g2))

    """
    for coexisting nodes and edges in g1 and g2, calculate the difference of their weight and addd it to the new graph
    for nodes and edges that only exist in g2, remain it in the new graph
    """
    g = nx.Graph()
    for node in g2.nodes:
        if g1.has_node(node):
            if g2.nodes[node]['count'] > g1.nodes[node]['count']:
                g.add_node(node, count=g2.nodes[node]['count'] - g1.nodes[node]['count'], x=g2.nodes[node]['x'], y=g2.nodes[node]['y'])
        else:
            g.add_node(node, count=g2.nodes[node]['count'], x=g2.nodes[node]['x'], y=g2.nodes[node]['y'])
    for u, v, data in g2.edges(data=True):
        if g1.has_edge(u, v):
            if data['weight'] > g1[u][v]['weight']:
                g.add_edge(u, v, weight=data['weight'] - g1[u][v]['weight'])
        else:
            g.add_edge(u, v, weight=data['weight'])
    
    # calculate the color scale for nodes and edges
    node_count = [data['count'] for node, data in g.nodes(data=True)]
    edge_weight = [data['weight'] for u, v, data in g.edges(data=True)]
    for node in g.nodes:
        g.nodes[node]['color'] = np.interp(g.nodes[node]['count'], (min(node_count), max(node_count)), (0.1, 1))
    for u, v, data in g.edges(data=True):
        data['color'] = np.interp(data['weight'], (min(edge_weight), max(edge_weight)), (0.1, 1))

    return nx.node_link_data(g)