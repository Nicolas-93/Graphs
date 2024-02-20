from typing import Hashable, Iterable, Tuple, Sequence
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import deque, namedtuple
from functools import total_ordering
import graphviz as gv

Vertex = Hashable

@dataclass(frozen=True, eq=True)
class Edge:
    u: Vertex = field(hash=True, compare=True)
    v: Vertex = field(hash=True, compare=True)

    def opposite(self) -> 'Edge':
        return Edge(self.v, self.u)
    
    def vertices(self) -> Tuple[Vertex, Vertex]:
        return (self.u, self.v)
    
    as_tuple = vertices

    def __iter__(self):
        return iter(self.as_tuple())

    def __getitem__(self, index: int):
        return self.as_tuple()[index]
    
    def __len__(self):
        return 2
    
    def stringify(self) -> str:
        return (str(self.u), str(self.v))

    def ordered(self) -> 'Edge':
        return Edge(*sorted(self.vertices()))

@total_ordering
@dataclass(frozen=True, eq=True)
class WeightedEdge(Edge):
    weight: float = field(hash=None, compare=False)

    def as_edge(self) -> Edge:
        return Edge(self.u, self.v)

    def as_tuple(self) -> Tuple[Vertex, Vertex]:
        return (self.u, self.v, self.weight)

    def __len__(self):
        return 3

    def get_weight(self) -> float:
        return self.weight

    def opposite(self) -> 'WeightedEdge':
        return WeightedEdge(self.v, self.u, self.weight)

    def ordered(self) -> 'WeightedEdge':
        return WeightedEdge(*sorted(self.vertices()), self.weight)
    
    def __lt__(self, other):
        return self.weight < other.weight

class Graph(ABC):
    @abstractmethod
    def add_edge(self, edge: Edge):
        """Add an edge to the graph

        Args:
            edge (Edge): Edge linking two vertices
            if one those vertices doesn't exists, they will be created
        """
        pass
    
    def _add_vertex_if_inexistant(self, edge: Edge):
        """Add vertices from edge if they are not already
        in the graph.

        Args:
            edge (Edge): Edge
        """

        if not self.has_vertex(edge.u):
            self.add_vertex(edge.u)

        if not self.has_vertex(edge.v):
            self.add_vertex(edge.v)

    def add_edges(self, edges: Iterable[Edge]):
        """Add multiple edges to the graph

        Args:
            edges (Iterable[Edge]): Edges to add
        """
        for edge in edges:
            self.add_edge(edge)

    @abstractmethod
    def add_vertex(self, v: Vertex):
        """Add a vertex to the graph

        Args:
            v (Vertex): Vertex to add
        """
        pass

    def add_vertices(self, vertices: Iterable[Vertex]):
        """Add multiple vertices to the graph

        Args:
            vertices (Iterable[Vertex]): Vertices to add
        """
        for v in vertices:
            self.add_vertex(v)

    @abstractmethod
    def get_edges(self) -> Iterable[Edge]:
        """Get all edges of the graph

        Returns:
            Iterable[Edge]: Edges of the graph
        """
        pass

    def get_edges_as_tuples(self) -> Iterable[tuple[Vertex, Vertex]]:
        """Get all graph's edges as tuples

        Returns:
            Iterable[tuple[Vertex, Vertex]]: Edges of the graph, as tuples of vertice
        """
        return (edge.vertices() for edge in self.get_edges())

    @abstractmethod
    def get_vertices(self) -> Iterable[Vertex]:
        """Get all vertices of the graph

        Returns:
            Iterable[Vertex]: Vertices of the graph
        """
        pass

    @abstractmethod
    def get_loops(self) -> Iterable[Vertex]:
        """Get all vertices with loops (edges linking a vertex to itself)

        Returns:
            Iterable[Vertex]: Vertices with loops
        """
        pass

    @abstractmethod
    def has_edge(self, edge: Edge) -> bool:
        """Check if an edge exists in the graph

        Args:
            edge (Edge): Edge to check

        Returns:
            bool: True if the edge exists, False otherwise
        """
        pass

    @abstractmethod
    def has_vertex(self, v: Vertex) -> bool:
        """Check if a vertex exists in the graph

        Args:
            v (Vertex): Vertex to check

        Returns:
            bool: True if the vertex exists, False otherwise
        """
        pass

    @abstractmethod
    def get_degree(self, v: Vertex) -> int:
        """Get the degree of a vertex

        Args:
            v (Vertex): Vertex to get the degree of

        Returns:
            int: Degree of the vertex
        """
        pass

    def get_nb_edges(self) -> int:
        """Get the number of edges in the graph

        Returns:
            int: Number of edges
        """
        return len(tuple(self.get_edges()))

    def get_nb_vertex(self) -> int:
        """Get the number of vertices in the graph

        Returns:
            int: Number of vertices
        """
        return len(tuple(self.get_vertices()))

    def get_nb_loops(self) -> int:
        """Get the number of loops in the graph

        Returns:
            int: Number of loops
        """
        return len(tuple(self.get_loops()))

    @abstractmethod
    def remove_edge(self, edge: Edge):
        pass

    @abstractmethod
    def remove_vertex(self, v: Vertex):
        """Remove a vertex from the graph
        and all edges linked to it

        Args:
            v (Vertex): Vertex to remove
        """
        pass

    @abstractmethod
    def get_neighbours(self, v: Vertex) -> Iterable[Vertex]:
        """Get the neighbours of a vertex

        Args:
            v (Vertex): Vertex to get the neighbours of

        Returns:
            Iterable[Vertex]: Neighbours of the vertex
        """
        pass

    def get_neighbours_edges(self, v: Vertex) -> Iterable[Edge]:
        """Get neighbours edges of a vertex

        Args:
            v (Vertex): Vertex to get the neighbours from

        Returns:
            Iterable[Edge]: Vertex's neighbours edges
        """
        return (Edge(v, neighbour) for neighbour in self.get_neighbours(v))

    def _require_vertex(self, v: Vertex):
        """Check if a vertex exists in the graph
        before doing an operation on it

        Args:
            v (Vertex): Vertex to check

        Raises:
            ValueError: If the vertex doesn't exists
        """
        if not self.has_vertex(v):
            raise ValueError(f"Inexistant vertex : {v}")

    def _require_edge(self, edge: Edge):
        """Check if an edge exists in the graph

        Args:
            edge (Edge): Edge to check

        Raises:
            ValueError: If the edge doesn't exists
        """
        if not self.has_edge(edge):
            raise ValueError(f"Edge {edge} doesn't exists")

    def _require_inexistant_edge(self, edge: Edge):
        if self.has_edge(edge):
            raise ValueError(f"Edge {edge} already exists")

    def as_dot(self) -> gv.Graph:
        pass

    def breadth_first_search(self, start: Vertex) -> Iterable[Vertex]:
        """Breadth first search of the graph

        Args:
            start (Vertex): Starting vertex

        Yields:
            Iterator[Iterable[Vertex]]: Vertices in the order they are visited
        """
        queue = deque()
        visited = set()
        queue.append(start)

        while queue:
            if (v := queue.popleft()) in visited:
                continue
            visited.add(v)

            yield v

            for neighbour in self.get_neighbours(v):
                queue.append(neighbour)

    def depth_first_search(self, start: Vertex) -> Iterable[Vertex]:
        """Depth first search of the graph

        Args:
            start (Vertex): Starting vertex

        Yields:
            Iterator[Iterable[Vertex]]: Vertices in the order they are visited
        """
        stack = list()
        visited = set()
        stack.append(start)

        while stack:
            if (v := stack.pop()) in visited:
                continue
            visited.add(v)

            yield v

            for neighbour in reversed(self.get_neighbours(v)):
                stack.append(neighbour)

    def get_inducted_subgraph(self) -> 'UndirectedGraph':
        pass
