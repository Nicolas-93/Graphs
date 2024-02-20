from graphs.weighted import WeightedUndirectedGraph
from graphs import WeightedEdge, Vertex
from collections import defaultdict
import heapq
from typing import Optional, List

EdgeHeap = List[WeightedEdge]

def _store_valid_edges(
        graph: WeightedUndirectedGraph,
        start: Vertex,
        edges: EdgeHeap,
        pending: dict
    ) -> None:
    for neighbour in graph.get_neighbours_edges_with_weight(start):
        if pending[neighbour.v]:
            heapq.heappush(edges, neighbour)

def _extract_correct_edge(edges: EdgeHeap, pending: dict) -> Optional[WeightedEdge]:
    while edges:
        edge = heapq.heappop(edges)
        if pending[edge.u] != pending[edge.v]:
            return edge
    return None

def mwst_prim(graph: WeightedUndirectedGraph, start: Vertex) -> WeightedUndirectedGraph:
    tree = WeightedUndirectedGraph()
    tree.add_vertex(start)

    pending = defaultdict(lambda : True)
    pending[start] = False

    candidates = list()
    _store_valid_edges(graph, start, candidates, pending)

    while (
        (tree.get_nb_vertex() <= graph.get_nb_vertex()) and
        (edge := _extract_correct_edge(candidates, pending))
    ):
        if pending[edge.v]:
            edge = edge.opposite()
        tree.add_edge(edge)
        pending[edge.u] = False
        _store_valid_edges(graph, edge.u, candidates, pending)
    
    return tree
