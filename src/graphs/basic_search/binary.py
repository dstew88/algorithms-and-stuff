from typing import List

from src.graphs.graph import Graph

def is_binary_search_tree(graph: Graph, starting_vertex: int) -> List[int]:

    if starting_vertex not in graph.get_definition():
        return True

    left = graph.get_definition()[starting_vertex][0]
    right = graph.get_definition()[starting_vertex][1]

    if left and left >= starting_vertex:
        return False

    if right and right <= starting_vertex:
        return False

    if not is_binary_search_tree(graph, left) or not is_binary_search_tree(graph, right):
        return False

    return True
