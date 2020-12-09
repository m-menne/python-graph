import numpy as np
import math
from warnings import warn

from graph import Graph


class Dijkstra:
    
    def __init__(self, g: Graph):
        """Constructor of the Dijkstra class. 'g' should contain the graph to be considered."""
        self.__graph = g
        self.__min_length = [None for i in range(0,g.return_num_vertices())]
        self.__prev = [None for i in range(0,g.return_num_vertices())]
        self.__min_length_graphs = [None for i in range(0,g.return_num_vertices())]
        self.__shortest_paths = {}
        
        self.__warn_weighted = not np.any((self.__graph.return_adjacencyMatrix() != 0) * (self.__graph.return_adjacencyMatrix() != 1))
            
    def return_graph(self):
        """Returns the considered graph."""
        return self.__graph
        
    def return_shortestPaths(self, startVertex):
        """Returns a graph consisting of the shortest paths starting from the specified start vertex."""
        # Already computed results are stored and returned if required
        if self.__min_length_graphs[startVertex] != None:
            return self.__min_length_graphs[startVertex]
        else:
            self.__dijkstra(startVertex)
            return self.__min_length_graphs[startVertex]
        
    def return_shortestPath(self, startVertex, endVertex):
        """Returns a graph consisting of the shortest path between specified start and end vertex."""
        # Already computed results are stored and returned if required
        if (startVertex, endVertex) in self.__shortest_paths:
            return self.__shortest_paths[(startVertex, endVertex)]
        
        prev = self.return_parent(startVertex)
        # If no path exists:
        if prev[endVertex] == None or startVertex==endVertex:
            return Graph(np.zeros((0, 0), dtype=np.int),vertexNames="")
        
        # Build up path
        sub_mat = np.zeros((len(prev), len(prev)), dtype=np.int)
        sub_list = []
        j = endVertex
        i = prev[j]
        orig_mat = self.__graph.return_adjacencyMatrix()
        while i != None:
            sub_list.append((self.__graph.return_vertexName(i),self.__graph.return_vertexName(j),orig_mat[i][j]))
            j = i
            i = prev[j]
            
        # Inherit vertex order from the original graph:
        name_order = self.__graph.return_names()
        name_order = [x for x in name_order if x in list(zip(*sub_list))[0] or x in list(zip(*sub_list))[1]]
        out = Graph(sub_list, dtype=self.__graph.return_weightType(),  vertexNames=name_order)
        self.__shortest_paths[(startVertex, endVertex)] = out
        return out
            
    def return_shortestPathLengths(self, startVertex):
        """Returns a list of the shortest paths starting from the specified start vertex."""
        # Already computed results are stored and returned if required
        if self.__min_length[startVertex] != None:
            return self.__min_length[startVertex]
        else:
            self.__dijkstra(startVertex)
            return self.__min_length[startVertex]
        
    def return_parent(self, startVertex):
        """Returns a list of parent nodes for the shortest paths starting from the specified start vertex."""
        # Already computed results are stored and returned if required
        if self.__min_length[startVertex] != None:
            return self.__prev[startVertex]
        else:
            self.__dijkstra(startVertex)
            return self.__prev[startVertex]
        
    def __dijkstra(self, startVertex):
        """Executes Dijkstra's algorithm with the specified start vertex and creates a subgraph consisting of the shortest paths, a list of path lengths, and a list of parent vertices."""
        
        if self.__warn_weighted:
            warn(Warning("The given graph contains no weighted edges. A calculation of shortest paths is possible using the Dijkstra algorithm, but the use of the width search would be more useful here."))
        
        # Set of vertices not yet traversed, ordered by vertex indexes
        q   = list(range(0,self.__graph.return_num_vertices()))
        # List for the computed distances to the vertices
        dist = [[math.inf, i] for i in q]
        # List of the parent of the vertices on the shortest path
        prev = [None for i in range(0,self.__graph.return_num_vertices())]
        # The start vertex has a distance of 0
        dist[startVertex] = [0, startVertex]
        
        # While not all vertices have been traversed
        while len(q)>0:
            # Calculation of the intersection of q and dist with consideration of the vertex indices
            dist_intersects_q = [x for x in dist if x[1] in q]
            # Get index of vertex with minimum distance to start vertex
            u = dist_intersects_q[np.argmin([x[0] for x in dist_intersects_q])][1]
            # Remove this vertex from list q
            q.remove(u)
            for v in self.__graph.return_adjacencies(u):
                alt = dist[u][0] + v[1]
                if alt < dist[v[0]][0]:
                    dist[v[0]][0] = alt
                    prev[v[0]] = u

        # Create subgraph consting of the shortest paths
        sub_list = []
        orig_mat = self.__graph.return_adjacencyMatrix()
        for j in range(0,len(prev)):
            i = prev[j]
            if i!=None:
                sub_list.append((self.__graph.return_vertexName(i),self.__graph.return_vertexName(j),orig_mat[i][j]))
        if len(sub_list) > 0:
            # Inherit vertex order from the original graph:
            name_order = self.__graph.return_names()
            name_order = [x for x in name_order if x in list(zip(*sub_list))[0] or x in list(zip(*sub_list))[1]]
            self.__min_length_graphs[startVertex] = Graph(sub_list, dtype=self.__graph.return_weightType(), vertexNames=name_order)
        else:
            self.__min_length_graphs[startVertex] = Graph(np.array([[0]], dtype=self.__graph.return_weightType()), vertexNames=[self.__graph.return_vertexName(startVertex)])
        
        self.__min_length[startVertex] = tuple([x[0] for x in dist]) 
        self.__prev[startVertex] = tuple(prev)
