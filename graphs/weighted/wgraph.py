from typing import Dict, Iterable, Tuple

from graphs import Edge, Vertex, Graph

class WeightedGraph(Graph):
    weights: Dict[Edge, float]

    def __init__(self):
        # super().__init__(*args, **kwargs)
        self.weights = dict()

    def add_edge(self, edge: Edge):
        if edge.get_weight() is None:
            raise ValueError(f"Non-weighted {edge}")
        self.weights[edge.vertices()] = edge.get_weight()

    def remove_edge(self, edge: Edge):
        del self.weights[edge]

    def get_weighted_edges(self) -> Iterable[Edge]:
        raise NotImplementedError()

    def get_weight(self, edge: Edge) -> float:
        return self.weights[edge.vertices()]

    def set_weight(self, edge: Edge, weight: float):
        self.weights[edge.vertices()] = weight
