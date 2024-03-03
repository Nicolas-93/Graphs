from ..basic import UndirectedGraph
from ..weighted import WeightedUndirectedGraph
from unionfind import unionfind
from graphs import UDEdge

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
