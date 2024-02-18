from digraph import DirectedGraph
from typing import Optional, Iterable
from graph import Edge, WeightedEdge, Vertex
from weighted_graph import WeightedGraph
import graphviz as gv

class WeightedDirectedGraph(WeightedGraph, DirectedGraph):
    def __init__(self, edges: Optional[Iterable[WeightedEdge]] = None):
        super().__init__(self)

    def add_edge(self, edge: WeightedEdge):
        # Redefined for typing
        super().add_edge(self, edge)

    def get_edges(self) -> Iterable[WeightedEdge]:
        # Redefined for typing
        return super().get_edges() # Calls DirectedGraph's get_edges

    def as_dot(self) -> gv.Graph:
        dot = gv.Digraph()

        for edge in self.get_edges_with_weights():
            dot.edge(*edge.stringify(), label=str(edge.get_weight()))

        return dot
