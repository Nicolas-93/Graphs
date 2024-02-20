from collections import defaultdict
from typing import Set, Optional, Iterable
from itertools import product, chain

from graphs import Vertex, Edge, Graph

class AdjGraph(Graph):
    vertices : Set[Vertex]
    edges : defaultdict[Vertex, Set[Vertex]]

    def __init__(self, edges: Optional[Iterable[Edge]] = None):
        super().__init__()
        self.vertices = set()
        self.edges = defaultdict(set)

        if edges:
            self.add_edges(edges)

    def add_edge(self, edge: Edge):
        super().add_edge(edge)
        self._add_vertex_if_inexistant(edge)

        left, right = edge.vertices()
        self.edges[left].add(right)

    def add_vertex(self, v: Vertex):
        super().add_vertex(v)
        self.vertices.add(v)
        self.edges.get(v)

    def get_edges(self) -> Iterable[Edge]:
        return map(lambda tup: Edge(*tup),
            sorted(
                chain.from_iterable(
                    list(product((u,), vn))
                    for u, vn in self.edges.items()
                )
            )
        )

    def get_vertices(self) -> Iterable[Vertex]:
        return sorted(self.vertices)

    def get_loops(self) -> Iterable[Vertex]:
        return filter(lambda v : self.has_edge((v, v)), self.vertices)

    def has_edge(self, edge: Edge) -> bool:
        left, right = edge.vertices()
        return (
            left  in self.edges and
            right in self.edges[left]
        )

    def has_vertex(self, v: Vertex) -> bool:
        return v in self.vertices

    def get_degree(self, v: Vertex) -> int:
        return len(self.edges[v])

    def get_nb_vertex(self) -> int:
        return len(self.vertices)

    def remove_edge(self, edge: Edge):
        super().remove_edge(edge)
        self._require_edge(edge)
        left, right = edge.vertices()

        self.edges[left].remove(right)

    def remove_vertex(self, v: Vertex):
        super().remove_vertex(v)
        self._require_vertex(v)

        for neighbours in self.edges.values():
            neighbours.discard(v)

        del self.edges[v]
        self.vertices.remove(v)

    def get_neighbours(self, v: Vertex) -> Iterable[Vertex]:
        self._require_vertex(v)

        return sorted(self.edges[v])
