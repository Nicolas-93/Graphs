import inspect
import sys
from pprint import pprint
from manim import *
from graphs import Vertex, UDEdge
from graphs.weighted import WeightedUndirectedGraph
from graphs.algorithms import mwst_prim, PrimAnimStep
from typing import Optional, Tuple, Dict
from graphs.utils import set_anim_breakpoint_hook
from pprint import pprint as print

class MwstPrim(Scene):

    def _graph_to_manim(
            self,
            graph: WeightedUndirectedGraph,
            partitions: Optional[Tuple[Tuple[Vertex], Tuple[Vertex]]] = None
        ):
        """
        Convert a graph to a manim graph
        """
        vertex_config = {}
        # edge_config = {
        #     **{(u, v): {"label": str(n)} for u, v, n in graph.get_edges_with_weights_as_tuples()}
        # }
        edge_config = {}
        print(edge_config)
        if partitions:
            vertex_config = {v: {"fill_color": RED_C} for v in partitions[0]}
            vertex_config.update({v: {"fill_color": GREEN_C} for v in partitions[1]})

        mg = Graph(
            list(graph.get_vertices()),
            list(graph.get_edges_as_tuples()),
            layout='circular',
            partitions=partitions,
            layout_scale=3,
            labels=True,
            edge_config=edge_config,
            vertex_config=vertex_config,
        )

        self.play(Create(mg))

        labels = []
        for u, v, n in graph.get_weighted_edges():
            labels.append(Text(f"{n}").scale(0.6).next_to(mg.edges[u, v].get_center(), UP))

        self.play(*(Write(label) for label in labels))

        return mg

    def construct(self):
        wu_prim = WeightedUndirectedGraph(
            edges=[
                UDEdge(1, 4, 2),
                UDEdge(1, 0, 5),
                UDEdge(4, 0, 2),
                UDEdge(4, 3, 3),
                UDEdge(3, 0, 4),
                UDEdge(0, 2, 7),
                UDEdge(3, 2, 9),
                UDEdge(6, 4, 7),
                UDEdge(6, 3, 4),
                UDEdge(6, 5, 12),
                UDEdge(5, 3, 7),
                UDEdge(5, 2, 5)
            ]
        )

        self.manim_graph = self._graph_to_manim(wu_prim)
        self.anim_prim(wu_prim)
    
    def anim_prim(self, graph: WeightedUndirectedGraph):

        def takectx(state: PrimAnimStep, *args, **kwargs):
            print(state)
            variables = sys._getframe(2).f_locals

            if state == PrimAnimStep.PUSHED_EDGE:
                edge = variables['edge']
                self.play(FadeToColor(self.manim_graph.edges[edge.vertices()], color=BLUE))
            
            elif state == PrimAnimStep.REMOVE_INVALID_EDGE:
                edge = variables['edge']
                self.play(Uncreate(self.manim_graph.edges[edge.vertices()]))
            
            elif state == PrimAnimStep.CHOOSEN_EDGE:
                edge = variables['edge']
                self.play(
                    FadeToColor(self.manim_graph.edges[edge.vertices()], color=GREEN),
                    self.manim_graph[edge.v][0].animate.set_color(GREEN),
                    self.manim_graph[edge.v][1].animate.set_color(BLACK)
                )

        set_anim_breakpoint_hook(takectx)
        mwst_prim(graph=graph, start=0)

if __name__ == '__main__':
    with tempconfig({"quality": "medium_quality", "preview": True}):
        scene = MwstPrim()
        scene.render()
