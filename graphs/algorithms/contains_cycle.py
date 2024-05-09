from graphs.basic import DirectedGraph
from graphs.impl import Vertex
from enum import Enum, auto
from collections import defaultdict
from typing import Optional, Dict

class VertexStatus(Enum):
    IN_PROGRESS = auto()
    FINISHED    = auto()
    INEXPLORED  = auto()

def contains_cycle_aux(
    graph: DirectedGraph,
    start: Vertex,
    status: Optional[Dict[Vertex, VertexStatus]]=None
) -> bool:
    """Recursive approach to detect a cycle in an oriented graph
    Complexity : $O(|V| + |E|)$

    Args:
        graph (DirectedGraph): Graph to test
        start (Vertex): Test if a cycle is detected by beginning from this vertex.
        As the graph is oriented, it is needed to test from all vertices
        for checking if the graph has a cycle
        status (Optional[Dict[Vertex, VertexStatus]], optional): Contains
        exploration status. Defaults to None.

    Returns:
        bool: True if a cycle is detected by starting exploration from
        the vertex 'start'
    """

    if status is None:
        status = defaultdict(lambda : VertexStatus.INEXPLORED)

    if status[start] == VertexStatus.IN_PROGRESS:
        return True

    if status[start] == VertexStatus.FINISHED:
        return False

    status[start] = VertexStatus.IN_PROGRESS

    for u in graph.get_neighbours(start):
        if contains_cycle_aux(graph, u, status):
            return True

    status[start] = VertexStatus.FINISHED

    return False

def contains_cycle(graph: DirectedGraph) -> bool:
    """Test if an directed has a cycle
    Complexity : $O(|V|² + |V| * |E|)$

    Args:
        graph (DirectedGraph): graph to check

    Returns:
        bool: True if a cycle is detected, False otherwise
    """
    return any(
        contains_cycle_aux(graph, v)
        for v in graph.get_vertices()
    )
