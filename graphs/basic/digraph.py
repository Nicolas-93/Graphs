from typing import Optional, Iterable
import graphviz as gv

from graphs import DEdge
from graphs.impl.adjacent_graph import AdjGraph

class DirectedGraph(AdjGraph):

    def __init__(self, edges: Optional[Iterable[DEdge]] = None):
        super().__init__(edges=edges)

    def add_edge(self, edge: DEdge):
        self._require_inexistant_edge(edge)
        super().add_edge(edge)

    def as_dot(self) -> gv.Graph:
        dot = gv.Digraph()
        dot.edges(e.stringify() for e in self.get_edges())
        return dot
