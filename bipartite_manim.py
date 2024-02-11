from undirected_graph import UndirectedGraph
from manim import *
from graph_utils import invert_dict, is_bipartite
from collections import deque, defaultdict

class LabeledModifiedGraph(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4, 5, 6]
        edges = (
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (2, 5),
            (3, 5),
            (5, 6),
            (6, 4),
        )
        ug = UndirectedGraph(edges=edges)

        # Create base graph
        self.manim_graph = Graph(
            vertices, edges,
            layout="spring",
            partitions=None,
            layout_scale=3,
            labels=True,
            vertex_config={
                0: {"fill_color": RED_C}
            },
            edge_config={}
        )
        self.play(Create(self.manim_graph))
        
        # Check if the graph is bipartite
        self._is_bipartite(ug)
        self.add(self.manim_graph)

        partitions = is_bipartite(ug)
        
        if partitions:
            vertex_config = {v: {"fill_color": RED_C} for v in partitions[0]}
            vertex_config.update({v: {"fill_color": GREEN_C} for v in partitions[1]})
            partitioned = Graph(
                vertices, edges,
                layout="partite",
                partitions=partitions,
                layout_scale=3,
                labels=True,
                vertex_config=vertex_config,
                edge_config={}
            )
            self.play(Transform(self.manim_graph, partitioned))

        self.wait(5)

    def _is_bipartite(self, graph: Graph):
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

        not_visited = lambda v: bipartition[v] == -1

        while queue:
            u = queue.popleft()
            u_center = self.manim_graph[u].get_center()

            for v in graph.get_neigbours(u):
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
                    self.play(
                        self.manim_graph[v].animate.set_color(
                            GREEN_C if bipartition[v] else RED_C
                        )
                    )
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

        d = invert_dict(bipartition)

        return tuple(d[False]), tuple(d[True])
