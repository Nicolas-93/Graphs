import inspect
from typing import Iterable, Optional
from collections import defaultdict
import graphviz as gv

from graphs import Vertex, Edge, UDEdge
from graphs.impl.adjacent_graph import AdjGraph

class UndirectedGraph(AdjGraph):

    vertices : set[Vertex]
    edges : defaultdict[Vertex, set[Vertex]]

    def __init__(self, edges: Optional[Iterable[Edge]] = None):
        super().__init__(edges=edges)

    def add_edge(self, edge: UDEdge):
        self._require_inexistant_edge(edge)
        self._require_inexistant_edge(edge.opposite())

        super().add_edge(edge)
        super().add_edge(edge.opposite())

    def get_edges(self) -> Iterable[UDEdge]:
        return map(
            lambda edge: UDEdge(*edge),
            filter(
                lambda edge : edge.u <= edge.v,
                super().get_edges()
            )
        )

    def get_neighbours_edges(self, v: Vertex) -> Iterable[UDEdge]:
        return (UDEdge(*edge) for edge in super().get_neighbours_edges(v))

    def has_edge(self, edge: UDEdge) -> bool:
        return (
            super().has_edge(edge)
            or
            super().has_edge(edge.opposite())
        )

    def remove_edge(self, edge: Edge):
        self._require_edge(edge)

        super().remove_edge(edge)
        super().remove_edge(edge.opposite())

    def as_dot(self) -> gv.Graph:
        dot = gv.Graph()
        dot.edges(e.stringify() for e in self.get_edges())
        return dot
