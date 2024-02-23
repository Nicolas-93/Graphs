from typing import Optional, Iterable
import graphviz as gv

from graphs.basic.udigraph import UndirectedGraph
from graphs import Edge, Vertex, UDEdge
from graphs.weighted.wgraph import WeightedGraph

class WeightedUndirectedGraph(UndirectedGraph, WeightedGraph):
    def __init__(self, edges: Optional[Iterable[UDEdge]] = None):
        WeightedGraph.__init__(self)
        UndirectedGraph.__init__(self, edges=edges)

    def add_edge(self, edge: UDEdge):
        super().add_edge(edge)

    def remove_edge(self, edge: Edge):
        super().remove_edge(edge)

    def get_weighted_edges(self) -> Iterable[UDEdge]:
        return (
            UDEdge(*e, self.get_weight(e))
            for e in self.get_edges()
        )

    def get_weight(self, edge: Edge) -> float:
        return super().get_weight(edge)

    def set_weight(self, edge: Edge, weight: float):
        super().set_weight(edge, weight)

    def get_edges(self) -> Iterable[UDEdge]:
        return UndirectedGraph.get_edges(self)

    def as_dot(self) -> gv.Graph:
        dot = gv.Graph()

        for u, v, n in (e.stringify() for e in self.get_weighted_edges()):
            dot.edge(u, v, label=n)

        return dot
