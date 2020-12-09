import unittest

from graph import *

class TestGraphClass(unittest.TestCase):

    def setUp(self):
        
        self.test_nums = 10 # Number of random test cases
        self.test_size = 50 # Mean number of vertices of created random graphs
        
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

        self.graph_a = Graph(self.mat_a, vertexNames=['a','b','c','d','e','f','g'])
        self.graph_b = Graph(self.adj_b, dtype=np.float64, vertexNames=["0","1","2","3"])
        self.graph_c = Graph(self.mat_c, vertexNames=['A','B','C','D','E','F','G'], dtype = np.int64)
    
 
    def test_numVertices(self):
        """Tests the getter-method for the number of vertices."""
        self.assertEqual(self.graph_a.return_num_vertices(), 7)
        self.assertEqual(self.graph_b.return_num_vertices(), 4)
        self.assertEqual(self.graph_c.return_num_vertices(), 7)
        
    def test_numEdges(self):
        """Tests the getter-method for the number of edges."""
        self.assertEqual(self.graph_a.return_num_edges(), 7)
        self.assertEqual(self.graph_b.return_num_edges(), 12)
        self.assertEqual(self.graph_c.return_num_edges(), 4)
    
    def test_outdeg(self):
        """Tests the getter-method for the number of outgoing edges."""
        self.assertEqual(self.graph_a.return_outdeg(0), 2)
        self.assertEqual(self.graph_b.return_outdeg(2), 3)
        self.assertEqual(self.graph_c.return_outdeg(3), 0)
        
    def test_indeg(self):
        """Tests the getter-method for the number of ingoing edges."""
        self.assertEqual(self.graph_a.return_indeg(1), 2)
        self.assertEqual(self.graph_b.return_indeg(3), 3)
        self.assertEqual(self.graph_c.return_indeg(4), 0)
    
    def test_weight(self):
        """Tests the getter-method for the weight of an edge."""
        self.assertEqual(self.graph_a.return_weight(0,1), 1)
        self.assertEqual(self.graph_b.return_weight(2,1), 3.5)
        self.assertEqual(self.graph_c.return_weight(4,5), 0)
    
    def test_weightType(self):
        """Tests the getter-method for the data type of an edge weight."""
        self.assertEqual(self.graph_a.return_weightType(), np.int32)
        self.assertEqual(self.graph_b.return_weightType(), np.float64)
        self.assertEqual(self.graph_c.return_weightType(), np.int64)
    
    def test_is_adjacent(self):
        """Tests the getter-method for adjacency of two vertices."""
        self.assertFalse(self.graph_a.is_adjacent(0,3))
        self.assertTrue(self.graph_b.is_adjacent(1,2))
        self.assertTrue(self.graph_c.is_adjacent(2,3))
    
    def test_adjacencies(self):
        """Tests the getter-method for adjacencies of a vertex."""
        self.assertEqual(self.graph_a.return_adjacencies(3),((4,1), (5,1), (6,1)))
        index3 = self.graph_b.return_vertexIndex('3')
        index1 = self.graph_b.return_vertexIndex('1')
        index0 = self.graph_b.return_vertexIndex('0')
        index2 = self.graph_b.return_vertexIndex('2')
        self.assertEqual(set(self.graph_b.return_adjacencies(index1)), set( ((index2, 2.5), (index3, 1.5), (index0, 2.0)) ))
        self.assertEqual(self.graph_c.return_adjacencies(5), ((6,5),))
    
    def test_adjacencyMatrix(self):
        """Tests the getter-method for the adjacency matrix."""
        self.assertEqual(np.any(np.bitwise_xor(self.graph_a.return_adjacencyMatrix(),[[0,1,1,0,0,0,0],
                               [0,0,0,1,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,1,1,1],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,1,0,0,0,0,0]])),False)        
        self.assertEqual(np.allclose(self.graph_b.return_adjacencyMatrix(), [[0.0, 0.5, 0.5, 0.5],
                                                                         [2.0, 0.0, 2.5, 1.5],
                                                                         [1.0, 3.5, 0.0, 2.25],
                                                                         [1.5, 2.75, 4.0, 0.0]]), True)
        self.assertEqual(np.any(np.bitwise_xor(self.graph_c.return_adjacencyMatrix(),[[0,0,3,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,10,0,2,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,5],
                               [0,0,0,0,0,0,0]])), False)
        
    def test_adjacencyList(self):
        """Tests the getter-method for the adjacency list."""
        self.assertEqual(self.graph_a.return_adjacencyList(), (((1,1), (2,1)), ((3,1),), (), ((4,1),(5,1),(6,1)), (), (), ((1,1),)) )
        self.assertEqual(self.graph_b.return_adjacencyList(), (((1, 0.5), (2, 0.5), (3, 0.5)), ((0, 2.0), (2, 2.5), (3, 1.5)), ((0, 1.0), (1, 3.5), (3, 2.25)), ((0, 1.5), (1, 2.75), (2, 4.0))) )
        self.assertEqual(self.graph_c.return_adjacencyList(), (((2,3),), (), ((1,10), (3,2)), (), (), ((6,5),), ()) )
        
    def test_names(self):
        """Tests the getter-method for the names."""
        self.assertEqual(self.graph_a.return_names(), ('a', 'b', 'c', 'd', 'e', 'f', 'g'))
        self.assertEqual(self.graph_b.return_names(), ('0', '1', '2', '3')) 
        self.assertEqual(self.graph_c.return_names(), ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
    
    def test_vertex_index(self):
        """Tests the getter-method for the index of a vertex."""
        self.assertEqual(self.graph_a.return_vertexIndex('b'), 1)
        self.assertEqual(self.graph_b.return_vertexIndex("1"), 1)
        self.assertEqual(self.graph_c.return_vertexIndex('C'), 2)
    
    def test_vertex_name(self):
        """Tests the getter-method for the name of a vertex."""
        self.assertEqual(self.graph_a.return_vertexName(0), 'a')
        self.assertEqual(self.graph_b.return_vertexName(3), '3')
        self.assertEqual(self.graph_c.return_vertexName(3), 'D')
        
    # Merges two unweighted graphs and inserts an additional vertex in the resulting graph so that the union builds a true superset of the two input graphs.
    def __merge_graphs_with_extra(self, g_a: Graph, g_b: Graph):
        m_a = g_a.return_adjacencyMatrix()
        m_b = g_b.return_adjacencyMatrix()
        size_diff = abs(m_a.shape[0]-m_b.shape[0])
        t_smaller, t_bigger = (m_a, m_b) if len(m_a)<len(m_b) else (m_b, m_a) # determine smaller and larger matrix
        # Adapt size and unite. Size is increased by one to guarantee that: mat != t_smaller != t_bigger
        t_smaller = np.lib.pad(t_smaller,(0,size_diff+1),'constant', constant_values=0)
        t_bigger = np.lib.pad(t_bigger,(0,1),'constant', constant_values=0)
        # Merge by applying bitwise-or to ensure that the weights remain either 0 or 1 (unweighted)
        mat = np.bitwise_or(t_smaller, t_bigger)
        return Graph(mat)
    
    def test_is_subgraph_of(self):
        """Tests the is_subgraph_of method of the graphs."""
        # Create random graphs
        for i in np.arange(self.test_nums):
            g_a = random_graph(random.randint(1,2*self.test_size), False, random.uniform(0, 1))
            g_b = random_graph(random.randint(1,2*self.test_size), False, random.uniform(0, 1))
            # Create union of the two graphs
            g_union = self.__merge_graphs_with_extra(g_a, g_b)
            # Check the the graphs are subgraphs of themselves
            self.assertEqual(g_a.is_subgraph_of(g_a), True)
            self.assertEqual(g_b.is_subgraph_of(g_b), True)
            self.assertEqual(g_union.is_subgraph_of(g_union), True)
            # Check that the created graphs are subgraphs of the union
            self.assertEqual(g_a.is_subgraph_of(g_union), True)
            self.assertEqual(g_b.is_subgraph_of(g_union), True)
            # Check that union is not a subgraph of the two graphs
            self.assertEqual(g_union.is_subgraph_of(g_a), False)
            self.assertEqual(g_union.is_subgraph_of(g_b), False)
