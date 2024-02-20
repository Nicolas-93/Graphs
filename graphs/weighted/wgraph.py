from graphs import Edge, Vertex, Graph, WeightedEdge

from typing import Dict, Iterable, Tuple

class WeightedGraph(Graph):
    weights: Dict[Edge, float]

    def __init__(self):
        # super().__init__(*args, **kwargs)
        self.weights = dict()

    def add_edge(self, edge: WeightedEdge):
        # print(edge)
        # import inspect
        # print(inspect.stack()[1])
        self.weights[edge.as_edge()] = edge.get_weight()

    def remove_edge(self, edge: Edge):
        del self.weights[edge]

    def get_weight(self, edge: Edge) -> float:
        return self.weights[edge]

    def set_weight(self, edge: Edge, weight: float):
        self.weights[edge] = weight

    def get_edges_with_weights(self) -> Iterable[WeightedEdge]:
        return (
            WeightedEdge(*edge, self.get_weight(edge))
            for edge in self.get_edges()
        )
    
    def get_edges_with_weights_as_tuples(self) -> Iterable[Tuple[Vertex, Vertex]]:
        return (edge.as_tuple() for edge in self.get_edges_with_weights())

    def get_neigbours_edges_with_weight(self, v: Vertex) -> Iterable[Edge]:
        """Get neighbours edges of a vertex with weight

        Args:
            v (Vertex): Vertex to get the neighbours from

        Returns:
            Iterable[Edge]: Vertex's neighbours edges with weight
        """
        return (WeightedEdge(*edge, self.get_weight(edge)) for edge in self.get_neigbours_edges(v))
