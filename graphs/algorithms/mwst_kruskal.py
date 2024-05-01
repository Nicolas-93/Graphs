from ..basic import UndirectedGraph
from ..weighted import WeightedUndirectedGraph
from unionfind import unionfind
from graphs import UDEdge
from itertools import chain


def mwst_kruskal(graph: WeightedUndirectedGraph) -> WeightedUndirectedGraph:
    forest = WeightedUndirectedGraph()
    forest.add_vertices(graph.get_vertices())
    classes = unionfind(graph.get_nb_vertex())

    vertices = {vertex : n for n, vertex in enumerate(graph.get_vertices())}

    print(vertices)

    for edge in sorted(graph.get_weighted_edges()):
        c_u, c_v = classes.find(vertices[edge.u]), classes.find(vertices[edge.v])
        if c_u != c_v:
            forest.add_edge(edge)
            classes.unite(c_u, c_v)

    return forest

def mwst_kruskal_natural_weights(graph: WeightedUndirectedGraph) -> WeightedUndirectedGraph:
    forest = WeightedUndirectedGraph()
    forest.add_vertices(graph.get_vertices())
    classes = unionfind(graph.get_nb_vertex())

    vertices = {vertex : n for n, vertex in enumerate(graph.get_vertices())}
    max_weight = max(graph.get_weighted_edges()).weight
    edges = [None for _ in range(max_weight + 1)]

    for edge in graph.get_weighted_edges():
        if edges[edge.weight] is None:
            edges[edge.weight] = []
        edges[edge.weight].append(edge)
    
    print(vertices)

    for edge in chain(*filter(lambda x: x is not None, edges)):
        c_u, c_v = classes.find(vertices[edge.u]), classes.find(vertices[edge.v])
        if c_u != c_v:
            forest.add_edge(edge)
            classes.unite(c_u, c_v)

    return forest

#define MAX(a, b) ((a) > (b) ? (a) : (b))