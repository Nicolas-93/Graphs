from typing import Tuple, Optional
from collections import defaultdict
from graphs.impl import Vertex
from graphs.weighted.wgraph import WeightedGraph
from graphs import UDEdge
from graphs.algorithms.utils import parents_to_tree

def extract_closest_vertex(
    pending: set[Vertex],
    dists: dict[Vertex, float]
) -> Optional[Vertex]:

    if not pending:
        return None

    ind : Tuple[int, Vertex] = min(
        enumerate(pending),
        key=lambda t: dists[t[1]]
    )
    pending.remove(ind[1])

    return ind[1]

def dijikstra(graph: WeightedGraph, start: Vertex) -> WeightedGraph:
    pending = set(graph.get_vertices())
    dists = defaultdict(lambda : float('inf'))
    dists[start] = 0

    parents = defaultdict(lambda : None)

    while pending:
        u = extract_closest_vertex(pending, dists)
        if u is None:
            return dists

        for v in graph.get_neighbours(u):
            m = min(
                dists[v],
                dists[u] + graph.get_weight(UDEdge(u, v))
            )
            if dists[v] != m:
                dists[v] = m
                parents[v] = u

    return parents_to_tree(graph, parents)
