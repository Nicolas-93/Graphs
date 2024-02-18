from adjacent_graph import AdjGraph
from typing import Optional, Iterable
from graph import Edge
import graphviz as gv

class DirectedGraph(AdjGraph):

    def __init__(self, edges: Optional[Iterable[Edge]] = None):
        super().__init__(edges=edges)

    def add_edge(self, edge: Edge):
        self._require_inexistant_edge(edge)
        super().add_edge(edge)

    def as_dot(self) -> gv.Graph:
        dot = gv.Digraph()
        dot.edges(e.stringify() for e in self.get_edges())
        return dot
