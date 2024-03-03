from graphs.basic import UndirectedGraph
from graphs import Vertex
from typing import List, Tuple
from collections import defaultdict
from graphs.algorithms import traversal

def linked_components(graph: UndirectedGraph) -> Tuple[List[Vertex]]:
    res = list()
    visited = defaultdict(lambda : False)

    for v in graph.get_vertices():
        if not visited[v]:
            compos = list(traversal.depth_first(graph, v))
            for u in compos:
                visited[u] = True
            res.append(compos)

    return res
