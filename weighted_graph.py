from graph import Edge, WeightedEdge, Graph
from typing import Dict, Iterable

class WeightedGraph(Graph):
    weights: Dict[Edge, float]

    def __init__(self, **kwargs):
        super().__init__()
        self.weights = dict()

    def add_edge(self, edge: WeightedEdge):
        #print(edge)
        import inspect
        print(inspect.stack()[1])
        self.weights[edge.as_edge()] = edge.get_weight()

    def remove_edge(self, edge: Edge):
        del self.weights[edge]

    def get_weight(self, edge: Edge) -> float:
        return self.weights[edge]

    def set_weight(self, edge: Edge, weight: float):
        self.weights[edge] = weight

    def get_edges_with_weights(self) -> Iterable[WeightedEdge]:
        weighted_edges = (
            WeightedEdge(*edge, self.get_weight(edge))
            for edge in self.get_edges()
        )
        return weighted_edges
