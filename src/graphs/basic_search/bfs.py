from typing import List

from src.graphs.graph import Graph

def breadth_first_search(graph: Graph, starting_vertex: int) -> List[int]:

    # check vertex in graph
    if starting_vertex > graph.get_num_vertices() - 1:
        raise ValueError("Vertex does not exist in graph!")

    # list to hold traversal path
    final_path: List[int] = []

    # declare a queue and insert the starting vertex
    queue = []
    queue.append(starting_vertex)

    # initialise an array of visited vertices
    visited = (graph.get_num_vertices() + 1) * [False]
    # mark starting vertex as visited
    visited[starting_vertex] = True

    # traverse the graph until queue is emtpy
    while queue:
        # remove the first vertex in the queue
        vertex = queue.pop(0)
        final_path.append(vertex)

        # for all unvisited neighbour vertices, add to queue and mark as visited
        for neighbour_vertex in graph.get_definition()[vertex]:
            if not visited[neighbour_vertex]:
                queue.append(neighbour_vertex)
                visited[neighbour_vertex] = True

    return final_path
