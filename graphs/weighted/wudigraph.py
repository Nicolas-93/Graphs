from graphs.basic.udigraph import UndirectedGraph
from graphs import Edge, WeightedEdge, Vertex
from graphs.weighted.wgraph import WeightedGraph

from typing import Optional, Iterable
import graphviz as gv

class WeightedUndirectedGraph(UndirectedGraph, WeightedGraph):
    def __init__(self, edges: Optional[Iterable[WeightedEdge]] = None):
        WeightedGraph.__init__(self)
        UndirectedGraph.__init__(self, edges=edges)

    def add_edge(self, edge: WeightedEdge):
        edge = edge.ordered()
        super().add_edge(edge)

    def remove_edge(self, edge: Edge):
        edge = edge.ordered()
        super().remove_edge(edge)

    def get_weight(self, edge: Edge) -> float:
        return super().get_weight(edge.ordered())

    def set_weight(self, edge: Edge, weight: float):
        super().set_weight(edge.ordered(), weight)

    def get_edges(self) -> Iterable[WeightedEdge]:
        # Redefined for typing
        return super().get_edges() # Calls UndirectedGraph's get_edges

    def as_dot(self) -> gv.Graph:
        dot = gv.Graph()

        for edge in self.get_edges_with_weights():
            dot.edge(*edge.stringify(), label=str(edge.get_weight()))

        return dot