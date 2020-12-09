import numpy as np

from graph import Graph
from graph_explo import Graphexploration
from graph_dijkstra import Dijkstra

class Circle:
    
    def __init__(self, g: Graph, **optional):
        """Constructor for the circle class. 'g' should contain the graph to be considered. The optional parameter 'explo' should be set to a graph exploration class instance to avoid redundant computations. If minimal (by edge weight) circles instead of small circles are desired, the 'dijkstra' parameter should be set to an instance of the Dijkstra class."""
        self.__graph = g
        if "explo" in optional:
            self.__explo = optional["explo"]
            if not isinstance(self.__explo, Graphexploration):
                raise TypeError("The given \'explo\' argument contains no instance of the graph exploration class.")
            elif self.__explo.return_graph() != g:
                raise ValueError("The given graph exploration class does not consider the given graph.")
        else:
            self.__explo = Graphexploration(g)
        if "dijkstra" in optional:
            self.__path_mode = optional["dijkstra"]
            if not isinstance(self.__path_mode, Dijkstra):
                raise TypeError("The given \'dijkstra\' argument contains no instance of the Dijkstra class.")
            elif self.__path_mode.return_graph() != g:
                raise ValueError("The given dijkstra class does not consider the given graph.")
        else:
            self.__path_mode = self.__explo
            
        self.__cycles = []
        self.__num_cycles = -1
        
    def return_graph(self):
        """Returns the considered graph."""
        return self.__graph
    
    def is_acyclic(self):
        """Returns 'True' if the graph does not contain circles."""
        return self.return_numCircles() == 0
    
    def return_numCircles(self):
        """Returns the number of found minimal circles. Under certain circumstances not all circles are found."""
        if self.__num_cycles >= 0:
            return self.__num_cycles
        else:
            self.__extract_cycles()
            return self.__num_cycles       
    
    def return_circles(self):
        """Returns a list of all found minimal circles. Under certain circumstances not all circles are found."""
        if self.__num_cycles >=0:
            return self.__cycles
        else:
            self.__extract_cycles()
            return self.__cycles
            
    def __extract_cycles(self):
        """Function to extract the minimum circles contained in the graph g."""
        backedges = self.__explo.return_backwardedges()
        for back in backedges:
            forward_path = self.__path_mode.return_shortestPath(back[1], back[0])
            cycle_mat = np.copy(forward_path.return_adjacencyMatrix())
            # Use names to convert the indices, because the node indices are not the same, since a path does not necessarily have the same adjacency matrix as the origin graph.
            i_path = forward_path.return_vertexIndex(self.__graph.return_vertexName(back[0]))
            j_path = forward_path.return_vertexIndex(self.__graph.return_vertexName(back[1]))
            cycle_mat[i_path, j_path] = self.__graph.return_weight(back[0], back[1])
            self.__cycles.append(Graph(cycle_mat, vertexNames=forward_path.return_names()))
            
        self.__cycles = tuple(self.__cycles)
        self.__num_cycles = len(backedges)
