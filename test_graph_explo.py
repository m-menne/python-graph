import unittest
import numpy as np
import math

from graph import Graph
from graph_explo import Graphexploration

class TestGraphExplorationClass(unittest.TestCase):

    def setUp(self):
        
        # Unweighted graph, normal
        self.mat_a = np.array([[0,1,1,0,0,0,0],
                               [0,0,0,1,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,1,1,1],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,1,0,0,0,0,0]], dtype=np.int32)
                               
        # Complete graph, weighted
        self.adj_b = [("0","1",0.5), ("0","2",0.5), ("0","3",0.5), ("1","0",2.0), ("1","2",2.5), ("1","3",1.5), ("2","0",1.0), ("2","1",3.5), ("2","3",2.25), ("3","0",1.5), ("3","1",2.75), ("3","2",4.0)]
        
        # Disjunct weighted graph
        self.mat_c = np.array([[0,0,3,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,10,0,2,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,5],
                               [0,0,0,0,0,0,0]], dtype=np.int64)

        # Graphs
        self.graph_a = Graph(self.mat_a, vertexNames=['a','b','c','d','e','f','g'])
        self.graph_b = Graph(self.adj_b, dtype=np.float64, vertexNames=["0","1","2","3"])
        self.graph_c = Graph(self.mat_c, vertexNames=['A','B','C','D','E','F','G'], dtype = np.int64)

        # Graph exploration instances
        self.explo_a = Graphexploration(self.graph_a)
        self.explo_b = Graphexploration(self.graph_b)
        self.explo_c = Graphexploration(self.graph_c)

    def test_dfsNum(self):
        """Tests the getter-method for the DFS-numbers."""
        self.assertEqual(self.explo_a.return_dfsNum(), (1.0, 2.0, 7.0, 3.0, 4.0, 5.0, 6.0))
        self.assertEqual(self.explo_b.return_dfsNum(1),(3.0, 1.0, 4.0, 2.0))
        self.assertEqual(self.explo_c.return_dfsNum(2),(4.0, 3.0, 1.0, 2.0, 5.0, 6.0, 7.0))
     
    def test_finNum(self):
        """Tests the getter-method for the FIN-numbers."""
        self.assertEqual(self.explo_a.return_finNum(), (7.0, 5.0, 6.0, 4.0, 1.0, 2.0, 3.0))
        self.assertEqual(self.explo_b.return_finNum(1),(2.0, 4.0, 1.0, 3.0))
        self.assertEqual(self.explo_c.return_finNum(2),(4.0, 2.0, 3.0, 1.0, 5.0, 7.0, 6.0))
        
    def test_backwardEdges(self):
        """Tests the getter-method for the backward edges."""
        self.assertEqual(self.explo_a.return_backwardedges(), ([6,1],))
        self.assertEqual(self.explo_b.return_backwardedges(1),([0,1], [2,0], [2,3], [2,1], [0,3], [3,1]))
        self.assertEqual(self.explo_c.return_backwardedges(2),())
        
    def test_nonTreeEdges(self):
        """Tests the getter-method for the non-tree edges."""
        self.assertEqual(self.explo_a.return_nontreeedges(), ([6,1],))
        self.assertEqual(self.explo_b.return_nontreeedges(1),([0,1], [2,0], [2,3], [2,1], [0,3], [3,1], [3,2], [1,0], [1,2]))
        self.assertEqual(self.explo_c.return_nontreeedges(2),([0,2],))   
        
    def test_dfsTree(self):
        """Tests the getter-method for the DFS-tree."""
        self.assertEqual(np.any(np.bitwise_xor(self.explo_a.return_dfs_tree().return_adjacencyMatrix(),[[0,1,1,0,0,0,0],
                                                                                                 [0,0,0,1,0,0,0],
                                                                                                 [0,0,0,0,0,0,0],
                                                                                                 [0,0,0,0,1,1,1],
                                                                                                 [0,0,0,0,0,0,0],
                                                                                                 [0,0,0,0,0,0,0],
                                                                                                 [0,0,0,0,0,0,0]])),False)
        self.assertEqual(np.allclose(self.explo_b.return_dfs_tree(1).return_adjacencyMatrix(),[[0.,0.,0.5,0.],
                                                                                        [0.,0.,0.,1.5],
                                                                                        [0.,0.,0.,0.],
                                                                                        [1.5,0.,0.,0.]]),True)
        self.assertEqual(np.any(np.bitwise_xor(self.explo_c.return_dfs_tree(2).return_adjacencyMatrix(),[[0,0,0,0,0],
                                                                                                  [10,0,2,0,0],
                                                                                                  [0,0,0,0,0],
                                                                                                  [0,0,0,0,5],
                                                                                                  [0,0,0,0,0]])),False)
        
    def test_bfsDist(self):
        """Tests the getter-method for the BFS-distances."""
        self.assertEqual(self.explo_a.return_bfsDist(), (0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0))
        self.assertEqual(self.explo_b.return_bfsDist(1),(1.0, 0.0, 1.0, 1.0))
        self.assertEqual(self.explo_c.return_bfsDist(2),(math.inf, 1.0, 0.0, 1.0, math.inf, math.inf, math.inf))
          
    def test_bfsParent(self):
        """Tests the getter-method for the BFS-parents."""
        self.assertEqual(self.explo_a.return_bfsParent(), (None, 0, 0, 1, 3, 3, 3))
        self.assertEqual(self.explo_b.return_bfsParent(1),(1, None, 1, 1))
        self.assertEqual(self.explo_c.return_bfsParent(2),(None, 2, None, 2, None, None, None))
        
    def test_bfsTree(self):
        """Tests the getter-method for the BFS-tree."""
        self.assertEqual(np.any(np.bitwise_xor(self.explo_a.return_bfsSpanningTree().return_adjacencyMatrix(),[[0,1,1,0,0,0,0],
                                                                                                      [0,0,0,1,0,0,0],
                                                                                                      [0,0,0,0,0,0,0],
                                                                                                      [0,0,0,0,1,1,1],
                                                                                                      [0,0,0,0,0,0,0],
                                                                                                      [0,0,0,0,0,0,0],
                                                                                                      [0,0,0,0,0,0,0]])),False)
        self.assertEqual(np.allclose(self.explo_b.return_bfsSpanningTree(1).return_adjacencyMatrix(),[[0.,0.,0.,0.],
                                                                                             [2.,0.,2.5,1.5],
                                                                                             [0.,0.,0.,0.],
                                                                                             [0.,0.,0.,0.]]),True)
        self.assertEqual(np.any(np.bitwise_xor(self.explo_c.return_bfsSpanningTree(2).return_adjacencyMatrix(),[[0,0,0],
                                                                                                       [10,0,2],
                                                                                                       [0,0,0]])),False)
        
    def test_shortestPath(self):
        """Tests the getter-method for the shortest path."""
        self.assertEqual(np.any(np.bitwise_xor(self.explo_a.return_shortestPath(0, 3).return_adjacencyMatrix(), [[0, 1, 0],
                                                                                                             [0, 0, 1],
                                                                                                             [0, 0, 0]])), False)
        self.assertEqual(np.allclose(self.explo_b.return_shortestPath(2, 3).return_adjacencyMatrix(), [[0., 2.25],
                                                                                                   [0., 0.]]), True)
        self.assertEqual(len(self.explo_c.return_shortestPath(2, 6).return_adjacencyMatrix()), 0)
        
    def test_Graph(self):
        """Tests the getter-method for the considered graph."""
        self.assertEqual(self.explo_a.return_graph(), self.graph_a)
        self.assertEqual(self.explo_b.return_graph(), self.graph_b)
        self.assertEqual(self.explo_c.return_graph(), self.graph_c)
