from typing import Hashable, Sequence, Iterable, Tuple, Optional
from collections import defaultdict
from itertools import product, chain
from graph import Graph, Vertex, Edge
from adjacent_graph import AdjGraph
import graphviz as gv

class UndirectedGraph(AdjGraph):

    vertices : set[Vertex]
    edges : defaultdict[Vertex, set[Vertex]]
    __slots__ = tuple(__annotations__)

    def __init__(self, edges: Optional[Iterable[Edge]] = None):
        super().__init__(edges=edges)

    def add_edge(self, edge: Edge):
        super().add_edge(edge)
        super().add_edge(edge.opposite())

    def get_edges(self) -> Iterable[Edge]:

        return filter(
            lambda edge : edge.v1 <= edge.v2,
            super().get_edges()
        )

        # return sorted(
        #     chain.from_iterable(
        #         list(product((v1,), filter(lambda x : x <= v1, vn)))
        #         for v1, vn in self.edges.items()
        #     )
        # )

    def has_edge(self, edge: Edge) -> bool:
        return (
            super().has_edge(edge)
            and
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
