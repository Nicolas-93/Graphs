from typing import Optional, Iterable
import graphviz as gv

from graphs import WeightedEdge
from graphs.basic.digraph import DirectedGraph
from graphs.weighted.wgraph import WeightedGraph

class WeightedDirectedGraph(WeightedGraph, DirectedGraph):
    def __init__(self, edges: Optional[Iterable[WeightedEdge]] = None):
        WeightedGraph.__init__(self)
        DirectedGraph.__init__(self, edges=edges)
        # super().__init__(edges=edges)

    def add_edge(self, edge: WeightedEdge):
        # Redefined for typing
        DirectedGraph.add_edge(self, edge)
        WeightedGraph.add_edge(self, edge)

    def get_edges(self) -> Iterable[WeightedEdge]:
        # Redefined for typing
        return super().get_edges() # Calls DirectedGraph's get_edges

    def as_dot(self) -> gv.Graph:
        dot = gv.Digraph()

        for edge in self.get_edges_with_weights():
            dot.edge(*edge.stringify(), label=str(edge.get_weight()))

        return dot
