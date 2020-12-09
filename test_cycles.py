import unittest
from graph_explo import *
from graph_cycles import *
from graph import *
import numpy as np

class TestCircleClass(unittest.TestCase):

    def setUp(self):
        self.test_nums = 10 # Number of random test cases
        self.test_size = 25 # Mean number of vertices of created random graphs
        self.__random_graphs = [None for i in range(0, self.test_nums)]
        self.__explo = [None for i in range(0, self.test_nums)]
        self.__cycle= [None for i in range(0, self.test_nums)]
        for i in np.arange(self.test_nums):
            g = random_graph(random.randint(1,2*self.test_size), False, random.uniform(0.0, 1.0))
            self.__random_graphs[i] = g
            self.__explo[i] = Graphexploration(g)
            self.__cycle[i] = Circle(g, explo=self.__explo[i])
            
    # For each backward edge (startVertex=0) a circle should be found. Assuming that DFS is correctly implemented, len(backedges) should be == num_circles.
    def test_return_numCircles(self):
        """Tests the return_numCircles method of the Circle class."""
        for i in np.arange(self.test_nums):
            num_backedges = len(self.__explo[i].return_backwardedges(0))
            self.assertEqual(self.__cycle[i].return_numCircles(), num_backedges)
    
    def test_is_acyclic(self):
        """Tests the is_acyclic method of the Circle class."""
        for i in np.arange(self.test_nums):
            num_backedges = len(self.__explo[i].return_backwardedges(0))
            self.assertEqual(self.__cycle[i].is_acyclic(), num_backedges == 0)
            
    def __is_cycle(self, c: Graph):        
        """Checks if the given graph represents a circle."""
        size = c.return_num_vertices()
        self.assertEqual(size > 1, True)
        counted_size = 1
        start = 0
        j = 0
        while True:
            self.assertEqual(c.return_outdeg(j), 1)
            self.assertEqual(c.return_indeg(j), 1)
            j = c.return_adjacencies(j)[0][0]
            if start==j:
                break
            counted_size += 1

        self.assertEqual(counted_size, size)
    
    def test_return_circles(self):
        """Tests the return_circles method of the Circle class."""
        for i in np.arange(self.test_nums):
            g = self.__random_graphs[i]
            kreise = self.__cycle[i].return_circles()
            for c in kreise:
                self.__is_cycle(c)
                self.assertEqual(c.is_subgraph_of(g), True)
