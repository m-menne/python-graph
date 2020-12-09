import unittest
from graph_explo import *
from graph_dijkstra import *
from graph import *
import numpy as np
from math import isclose

class TestDijkstra(unittest.TestCase):
    
    def setUp(self):
        self.test_nums = 10 # Number of random test cases
        self.test_size = 25 # Mean number of vertices of created random graphs
        self.__random_graphs = [None for i in range(0, self.test_nums)]
        # self.__explo = [None for i in range(0, self.test_nums)]
        self.__dijkstra= [None for i in range(0, self.test_nums)]
        for i in np.arange(self.test_nums):
            g = random_graph(random.randint(1,2*self.test_size), True, random.uniform(0.0, 1.0))
            self.__random_graphs[i] = g
            self.__dijkstra[i] = Dijkstra(g)
            
    # Checks if the Dijkstra procedure correctly creates a tree, which is the case if DFS does not find any non-tree edges in the tree (with startVertex as the root).
    # In addition, it is necessary to check whether the DFS tree and the tree to be tested are the same.
    def __is_tree(self, t: Graph, wurzel_name):
        wurzel_index = t.return_vertexIndex(wurzel_name)
        dfs = Graphexploration(t)
        dfs_tree = dfs.return_dfs_tree(wurzel_index)
        self.assertEqual(len(dfs.return_nontreeedges(wurzel_index)), 0)
        self.assertEqual(dfs_tree.is_subgraph_of(t), True)
        self.assertEqual(t.is_subgraph_of(dfs_tree), True) 
        
        # To automatically check the implementation of Dijkstra's algorithm, the method described in the answer to the following math.stackexchange question is used:
        # https://math.stackexchange.com/questions/425521/how-to-verify-a-shortest-path-tree-with-ove-running-time-by-giving-nodes-pre
        
        # Computes a Dijkstra tree with all possible start vertices and checks if the paths found are indeed the shortest paths, if the tree is actually a tree and if everything fits with the determined path lengths and parents.
        """Tests the implementation of Dikjstra's algorithm. return_shortestPaths, return_shortestPath, return_shortestPathLengths, are hereby tested."""
        for d in self.__dijkstra:
            graph = d.return_graph()
            num_vertices = graph.return_num_vertices()
            for s in range(0, num_vertices): # s := start vertex
                t = d.return_shortestPaths(s)
                dist = d.return_shortestPathLengths(s)
                self.__is_tree(t, graph.return_vertexName(s)) # Check if t is a correct tree
                
                # Checks if t contains the shortest paths
                for i in range(0, num_vertices):
                    adj_g = graph.return_adjacencies(i)
                    for j in adj_g:
                        # distance i->j (edgeWeight)
                        d_i_j = j[1]
                        d_s_i = dist[i]
                        d_s_j = dist[j[0]]
                        # If d_s_j would be larger, there would be a shorter path, which can not be.
                        self.assertEqual(d_s_j <= d_s_i+d_i_j, True) 
                        
            # To verify that the computed distance are correct, it is checked whether for each edge (u, v, weight) of the Dijkstra-tree it holds: dist(v) = dist(u) + weight
            for s in range(0, num_vertices): # s := Start vertex
                t = d.return_shortestPaths(s)
                num_vertices_tree = t.return_num_vertices()
                dist = d.return_shortestPathLengths(s)
                self.assertEqual(dist[s], 0) # Check start vertex: dist(0) has to be zero.
                for i in range(0, num_vertices_tree):
                    # Iterate over edges of the Dijkstra-tree
                    adj_t = t.return_adjacencies(i)
                    for j in adj_t:
                        # distanz i->j (edgeWeight)
                        # Convert index
                        i_ind = graph.return_vertexIndex(t.return_vertexName(i))
                        j_ind = graph.return_vertexIndex(t.return_vertexName(j[0]))
                        d_i_j = j[1]
                        d_s_i = dist[i_ind]
                        d_s_j = dist[j_ind]
                        self.assertEqual(isclose(d_s_j, d_s_i+d_i_j), True)
