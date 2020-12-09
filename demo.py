import numpy as np

from graph import *
from graph_explo import Graphexploration
from graph_cycles import Circle
from graph_dijkstra import *
from warnings import warn


try:
    from visu import Visu
    has_igraph = True
except ImportError:
    has_igraph = False
    warn(Warning("iGraph could not be imported! Are iGraph and icu v58 installed? Visualizations are skipped."))
    
    
# Create adjacency matrix for graph
mat_a = np.array([[0,2,0,0,1,0,0],
                    [1,0,9,1,1,0,0],
                    [0,8,0,0,0,0,0],
                    [0,0,2,0,0,0,0],
                    [0,8,0,2,0,0,0],
                    [0,1,0,1,0,0,1],
                    [0,0,0,0,0,0,0]], dtype=np.int32)
                    
adj_b = [("0","1",0.5), ("0","2",0.5), ("0","3",0.5), ("1","0",2.0), ("1","2",2.5), ("1","3",1.5), ("2","0",1.0), ("2","1",3.5), ("2","3",2.25), ("3","0",1.5), ("3","1",2.75), ("3","2",4.0)]
        
# If no node names are given in the matrix representation, the indices are used as node names
graph_a = Graph(mat_a, vertexNames=["0","1","2","3","4","5","6"])
# Even if names are predefined in the adjacency list representation, it is still very advisable to specify a vertex sequence. It is also possible to define isolated nodes (for which no entry in the adjacency list can be made) using the vertex name parameter.
graph_b = Graph(adj_b, vertexNames=["3","1","0","2"])
                    
# Create random graph
graph = random_graph(5,True, 0.5)
# Instantiate graphexploration
ex = Graphexploration(graph)
# Instantiate dijkstra
dijk = Dijkstra(graph)
# Create circle instance. The circle class can make use of already existing instances of the graphexploration and Dijkstra class, so that there is no need to perform multiple calculations.
circle = Circle(graph, explo=ex, dijkstra=dijk)
# Graph class:
print('---------------------Graph class--------------------------------------')
print('graph.return_num_vertices(): ' + str(graph.return_num_vertices()))
print('graph.return_num_edges(): ' + str(graph.return_num_edges()))
print('graph.return_outdeg(0): ' + str(graph.return_outdeg(0)))
print('graph.return_indeg(0): ' + str(graph.return_indeg(0)))
print('graph.return_weight(0,1): ' + str(graph.return_weight(0,1)))
print('graph.return_weightType(): ' + str(graph.return_weightType()))
print('graph.is_adjacent(0,1): ' + str(graph.is_adjacent(0,1)))
print('graph.return_adjacencies(0): ' + str(graph.return_adjacencies(0)))
print('graph.return_adjacencyMatrix():\n' + str(graph.return_adjacencyMatrix()))
print('graph.return_adjacencyList(): ' + str(graph.return_adjacencyList()))
print('graph.return_names(): ' + str(graph.return_names()))
print('graph.return_vertexIndex(1): ' + str(graph.return_vertexIndex(1)))
print('graph.return_vertexName(0): ' + str(graph.return_vertexName(0)))
if has_igraph:
    vis_graph = Visu(graph,w=800,h=800)
    vis_graph.visualize()
print('\n\n\n\n')

# Graph exploration class:
print('---------------------Graph exploration class--------------------------')
print('ex.return_dfsNum(): ' + str(ex.return_dfsNum()))
print('ex.return_finNum(): ' + str(ex.return_finNum()))
print('ex.return_dfs_tree().return_adjacencyMatrix():\n' + str(ex.return_dfs_tree().return_adjacencyMatrix()))
print('ex.return_bfsDist(): ' + str(ex.return_bfsDist()))
print('ex.return_bfsParent: ' + str(ex.return_bfsParent()))
print('ex.return_bfsSpanningTree().return_adjacencyMatrix():\n' + str(ex.return_bfsSpanningTree().return_adjacencyMatrix()))
print('ex.return_bfsSpanningTree().is_subgraph_of(graph): ' + str(ex.return_bfsSpanningTree().is_subgraph_of(graph)))
if has_igraph:
    dfs_tree = Visu(ex.return_dfs_tree(),w=800,h=800)
    dfs_tree.visualize()
    vis_graph.mark_subgraph(ex.return_dfs_tree())
    vis_graph.visualize()
    bfs_tree = Visu(ex.return_bfsSpanningTree(),w=800,h=800)
    bfs_tree.visualize()
    vis_graph.remove_marks()
    vis_graph.mark_subgraph(ex.return_bfsSpanningTree())
    vis_graph.visualize()
print('\n\n\n\n')

# Dijkstra class:
print('---------------------Dijkstra class-----------------------------------')
print('dijk.return_shortestPaths(0).return_adjacencyMatrix():\n' + str(dijk.return_shortestPaths(0).return_adjacencyMatrix()))
print(dijk.return_shortestPaths(0).return_names())
print('dijk.return_shortestPath(0,1).return_adjacencyMatrix():\n' + str(dijk.return_shortestPath(0,1).return_adjacencyMatrix()))
print(dijk.return_shortestPath(0,1).return_names())
print('dijk.return_shortestPathLengths(0): ' + str(dijk.return_shortestPathLengths(0)))
print('dijk.return_parent(0): ' + str(dijk.return_parent(0)))
if has_igraph:
    dijk_tree = Visu(dijk.return_shortestPaths(0),w=800,h=800)
    dijk_tree.visualize()
    vis_graph.remove_marks()
    vis_graph.mark_subgraph(dijk.return_shortestPaths(0), (0,255,255))
    vis_graph.visualize()
print('\n\n\n\n')

# Circle class:
print('---------------------Circle class-------------------------------------')
print('circle.is_acyclic(): ' + str(circle.is_acyclic()))
print('circle.return_numCircles(): ' + str(circle.return_numCircles()))
print('circle.return_circles():')
for circ in np.arange(circle.return_numCircles() if circle.return_numCircles() < 5 else 5):
    print(str(circle.return_circles()[circ].return_adjacencyMatrix()) + '\n' + str(circle.return_circles()[circ].return_names()))
    if has_igraph:
        vis_graph.remove_marks()
        vis_graph.mark_subgraph(circle.return_circles()[circ], (255,0,255))
        vis_graph.visualize()
print('\n\n\n\n')
