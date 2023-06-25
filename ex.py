from src.graphs.graph import Graph
from src.graphs.basic_search import breadth_first_search, depth_first_search, is_binary_search_tree
from src.sorting.quicksort import quicksort

g = Graph()
g.add_edge(0, 1)
g.add_edge(1, 0)
g.add_edge(1, 10)
g.add_edge(1, 10)
g.add_edge(1, 11)
g.add_edge(1, 12)
g.add_edge(0, 2)
g.add_edge(2, 4)
g.add_edge(2, 5)
g.add_edge(2, 6)
g.add_edge(0, 3)
g.add_edge(3, 7)
g.add_edge(3, 8)
g.add_edge(3, 9)

print(g.get_definition())

bfs_path = breadth_first_search(g, 1)
dfs_path = depth_first_search(g, 1)

print(bfs_path)
print(dfs_path)

binary_tree = Graph()
binary_tree.add_edge(5, 2)
binary_tree.add_edge(5, 6)
binary_tree.add_edge(2, 1)
binary_tree.add_edge(2, 3)
binary_tree.add_edge(6, 0)
binary_tree.add_edge(6, 7)

print(binary_tree.get_definition())

print(is_binary_search_tree(binary_tree, 5))


l = [4, 5, 1, 2, 7, 3, 4, 5]
print(l)
print(quicksort(l))