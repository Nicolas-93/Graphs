from collections import defaultdict
import heapq
from typing import Optional, List
from graphs.weighted import WeightedUndirectedGraph
from graphs import WeightedEdge, Vertex, Edge
from enum import Enum
from graphs.utils import abreakpoint

class PrimAnimStep(str, Enum):
    INIT = "Algorithme initialisé"
    CHOOSEN_EDGE = "Nouvelle arrête choisie"
    PUSHED_EDGE = "Arrête ajoutée au tas"
    REMOVE_INVALID_EDGE = "Arrête minimum ignorée et supprimée du tas"


EdgeHeap = List[WeightedEdge]

def _store_valid_edges(
        graph: WeightedUndirectedGraph,
        start: Vertex,
        edges: EdgeHeap,
        pending: dict
    ) -> None:
    for v in graph.get_neighbours(start):
        if pending[v]:
            edge = WeightedEdge(start, v, graph.get_weight(Edge(start, v)))
            heapq.heappush(edges, edge)
            abreakpoint(PrimAnimStep.PUSHED_EDGE)

def _extract_correct_edge(edges: EdgeHeap, pending: dict) -> Optional[WeightedEdge]:
    while edges:
        edge = heapq.heappop(edges)
        if pending[edge.u] != pending[edge.v]:
            return edge
        abreakpoint(PrimAnimStep.REMOVE_INVALID_EDGE)
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

        abreakpoint(PrimAnimStep.CHOOSEN_EDGE)

        if pending[edge.v]:
            edge = edge.opposite()
        tree.add_edge(edge)

        pending[edge.u] = False
        _store_valid_edges(graph, edge.u, candidates, pending)

    return tree
