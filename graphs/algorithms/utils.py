from graphs.impl import Vertex, DEdge
from graphs.basic.digraph import DirectedGraph

def parents_to_tree(original_graph, parents: dict[Vertex, Vertex]):
    new_graph = type(original_graph)()
    new_graph.add_vertices(original_graph.get_vertices())

    for u, v in parents.items():
        new_graph.add_edge(DEdge(u, v, original_graph.get_weight(DEdge(u, v))))
    
    return new_graph
