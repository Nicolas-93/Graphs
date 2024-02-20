from graphs import Vertex, Graph
from typing import Union, Tuple
from collections import deque, defaultdict
from graphs.utils import invert_dict

def is_bipartite(graph: Graph) -> Union[Tuple[Tuple[Vertex], Tuple[Vertex]], bool]:
    """Check if a graph is bipartite and return the two partitions if it is

    Args:
        graph (Graph): Graph to check

    Returns:
        Union[Tuple[Tuple[Vertex], Tuple[Vertex]], bool]: 
            - If the graph is bipartite, the two partitions
            - If the graph is not bipartite, False
    """

    queue = deque()
    bipartition = defaultdict(lambda : -1)
    start = graph.get_vertices()[0]
    
    queue.append(start)
    bipartition[start] = False

    while queue:
        u = queue.popleft()
        for v in graph.get_neighbours(u):
            if bipartition[v] == -1: # If not visited
                queue.append(v)
                bipartition[v] = not bipartition[u]
            elif bipartition[v] == bipartition[u]:
                return False

    d = invert_dict(bipartition)

    return tuple(d[False]), tuple(d[True])
