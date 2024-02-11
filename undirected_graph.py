from typing import Hashable, Sequence, Iterable, Tuple, Optional
from collections import defaultdict
from itertools import product, chain
from graph import Graph, Vertex, Edge

class UndirectedGraph(Graph):

    vertices : set[Vertex]
    edges : defaultdict[Vertex, set[Vertex]]
    __slots__ = tuple(__annotations__)

    def __init__(self, edges: Optional[Iterable[Edge]] = None):
        self.vertices = set()
        self.edges = defaultdict(set)

        if edges:
            self.add_edges(edges)

    def add_edge(self, edge: Edge):
        for v in filter(lambda x : not self.has_vertex(x), edge):
            self.add_vertex(v)

        left, right = edge
        self.edges[left].add(right)
        self.edges[right].add(left)

    def add_vertex(self, v: Vertex):
        self.vertices.add(v)
        self.edges[v]

    def get_edges(self) -> Iterable[Edge]:
        return sorted(
            chain.from_iterable(
                list(product((v1,), filter(lambda x : x <= v1, vn)))
                for v1, vn in self.edges.items()
            )
        )

    def get_vertices(self) -> Iterable[Vertex]:
        return sorted(self.vertices)

    def get_loops(self) -> Iterable[Vertex]:
        return filter(lambda v : self.has_edge((v, v)), self.vertices)

    def has_edge(self, edge: Edge) -> bool:
        left, right = edge
        return (
            (
                self.left  in self.edges and
                self.right in self.edges[left]
            )
            and
            (
                self.right in self.edges and
                self.left  in self.edges[right]
            )
        )

    def has_vertex(self, v: Vertex) -> bool:
        return v in self.vertices

    def get_degree(self, v: Vertex) -> int:
        return len(self.edges[v])

    def get_nb_vertex(self) -> int:
        return len(self.vertices)

    def remove_edge(self, edge: Edge):
        self._require_edge(edge)

        self.edges[left].remove(right)
        self.edges[right].remove(left)

    def remove_vertex(self, v: Vertex):
        self._require_vertex(v)

        for neigbours in self.edges.values():
            neigbours.discard(v)

        del self.edges[v]
        self.vertices.remove(v)

    def get_neigbours(self, v: Vertex) -> Iterable[Vertex]:
        self._require_vertex(v)

        return sorted(self.edges[v])
