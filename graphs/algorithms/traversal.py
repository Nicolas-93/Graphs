from graphs import Vertex, Graph
from typing import Iterable, Dict
from collections import deque, defaultdict
from graphs.basic.digraph import DirectedGraph
from graphs import DEdge

def _parents_to_tree(vertices: Iterable[Vertex], parents: Dict[Vertex, Vertex]) -> DirectedGraph:
    tree = DirectedGraph()
    tree.add_vertices(vertices)
    for v in vertices:
        if v in parents:
            tree.add_edge(DEdge(parents[v], v))
    return tree

def breadth_first(graph: Graph, start: Vertex) -> Iterable[Vertex]:
    """Breadth first traversal of the graph

    Args:
        graph (Graph): Graph to traverse
        start (Vertex): Traversal's root

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

        for neighbour in graph.get_neighbours(v):
            queue.append(neighbour)


def breadth_first_tree(graph: Graph, start: Vertex) -> DirectedGraph:
    """Breadth first traversal of the graph as a tree

    Args:
        graph (Graph): Graph to traverse
        start (Vertex): Traversal's root

    Returns:
        DirectedGraph: Traversal's tree
    """
    queue = deque()
    visited = set()
    queue.append(start)
    parents = defaultdict(lambda : start)

    while queue:
        if (u := queue.popleft()) in visited:
            continue
        visited.add(u)

        for neighbour in graph.get_neighbours(u):
            if neighbour not in visited:
                queue.append(neighbour)
                if parents[neighbour] == start:
                    parents[neighbour] = u

    return _parents_to_tree(graph.get_vertices(), parents)

def depth_first(graph: Graph, start: Vertex) -> Iterable[Vertex]:
    """Depth first traversal of the graph

    Args:
        graph (Graph): Graph to traverse
        start (Vertex): Traversal's root

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

        for neighbour in reversed(graph.get_neighbours(v)):
            stack.append(neighbour)


def depth_first_tree(graph: Graph, start: Vertex) -> Iterable[Vertex]:
    """Depth first traversal of the graph as a tree

    Args:
        graph (Graph): Graph to traverse
        start (Vertex): Traversal's root

    Yields:
        Iterator[Iterable[Vertex]]: Vertices in the order they are visited
    """
    stack = list()
    visited = set()
    stack.append(start)
    parents = defaultdict(lambda : start)

    while stack:
        if (u := stack.pop()) in visited:
            continue
        visited.add(u)

        for neighbour in graph.get_neighbours(u):
            if neighbour not in visited:
                stack.append(neighbour)
                if parents[neighbour] == start:
                    parents[neighbour] = u

    return _parents_to_tree(graph.get_vertices(), parents)
