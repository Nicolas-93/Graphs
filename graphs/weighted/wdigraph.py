from typing import Optional, Iterable
import graphviz as gv

from graphs import DEdge
from graphs.basic.digraph import DirectedGraph
from graphs.weighted.wgraph import WeightedGraph

class WeightedDirectedGraph(WeightedGraph, DirectedGraph):
    def __init__(self, edges: Optional[Iterable[DEdge]] = None):
        WeightedGraph.__init__(self)
        DirectedGraph.__init__(self, edges=edges)
        # super().__init__(edges=edges)

    def add_edge(self, edge: DEdge):
        DirectedGraph.add_edge(self, edge)
        WeightedGraph.add_edge(self, edge)

    def get_edges(self) -> Iterable[DEdge]:
        # Redefined for typing
        return super().get_edges() # Calls DirectedGraph's get_edges
    
    def get_weighted_edges(self) -> Iterable[DEdge]:
        return (
            DEdge(*e, self.get_weight(e))
            for e in self.get_edges()
        )

    def as_dot(self) -> gv.Graph:
        dot = gv.Digraph()

        for u, v, n in (e.stringify() for e in self.get_weighted_edges()):
            dot.edge(u, v, label=n)

        return dot
