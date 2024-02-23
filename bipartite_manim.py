from collections import deque, defaultdict
from typing import Optional, Tuple

from manim import *

from graphs import Vertex, UDEdge
from graphs.basic import UndirectedGraph
from graphs.algorithms import is_bipartite
from graphs.utils import invert_dict

class LabeledModifiedGraph(Scene):
    def construct(self):
        edges = (
            UDEdge(0, 1),
            UDEdge(0, 2),
            UDEdge(0, 3),
            UDEdge(1, 4),
            UDEdge(2, 5),
            UDEdge(3, 5),
            UDEdge(5, 6),
            UDEdge(6, 4),
        )
        ug = UndirectedGraph(edges=edges)

        # Create base graph
        self.manim_graph = self._graph_to_manim(ug)
        self.play(Create(self.manim_graph))

        # Check if the graph is bipartite
        self._is_bipartite(ug)

        partitions = is_bipartite(ug)

        if partitions:
            self.clear()
            partitioned = self._graph_to_manim(ug, partitions, completed_partitions=True)
            self.play(ReplacementTransform(self.manim_graph, partitioned))

        self.wait(5)

    def _graph_to_manim(
            self,
            graph: UndirectedGraph,
            partitions: Optional[Tuple[Tuple[Vertex], Tuple[Vertex]]] = None,
            completed_partitions=False
        ):
        """
        Convert a graph to a manim graph
        """
        vertex_config = {}
        edge_config = {}
        if partitions:
            vertex_config = {v: {"fill_color": RED_C} for v in partitions[0]}
            vertex_config.update({v: {"fill_color": GREEN_C} for v in partitions[1]})

        return Graph(
            list(graph.get_vertices()),
            list(graph.get_edges_as_tuples()),
            layout='partite' if partitions and completed_partitions else 'circular',
            partitions=partitions,
            layout_scale=3,
            labels=True,
            vertex_config=vertex_config,
            edge_config=edge_config
        )

    def _is_bipartite(self, graph: Graph):
        """Check if a graph is bipartite and return the two partitions if it is

        Args:
            graph (Graph): Graph to check

        Returns:
            Union[Tuple[Tuple[Vertex], Tuple[Vertex]], bool]: 
                - If the graph is bipartite, the two partitions
                - If the graph is not bipartite, False
        """

        def _get_bipartition_as_list(bipartition: dict):
            d = invert_dict(bipartition)
            return tuple(d[False]), tuple(d[True])

        queue = deque()
        bipartition = defaultdict(lambda : -1)
        start = graph.get_vertices()[0]

        queue.append(start)
        bipartition[start] = False

        def not_visited(v: Vertex):
            return bipartition[v] == -1

        while queue:
            u = queue.popleft()
            u_center = self.manim_graph[u].get_center()

            for v in graph.get_neighbours(u):
                v_center = self.manim_graph[v].get_center()
                line = Arrow(
                    start=u_center,
                    end=v_center,
                    color=YELLOW,
                    stroke_color=YELLOW,
                )
                self.play(Create(line))

                if not_visited(v):
                    queue.append(v)
                    bipartition[v] = not bipartition[u]

                    new_graph = self._graph_to_manim(graph, _get_bipartition_as_list(bipartition))
                    self.play(ReplacementTransform(self.manim_graph, new_graph))
                    self.manim_graph = new_graph
                    self.wait()

                elif bipartition[v] == bipartition[u]:
                    line = LabeledArrow(
                        Text("Cycle impair !").scale(0.5),
                        start=u_center,
                        end=v_center,
                        color=RED,
                        stroke_color=RED,
                    )
                    self.play(Create(line))
                    return False

                self.remove(line)

        return _get_bipartition_as_list(bipartition)
