import numpy as np
from copy import deepcopy
from warnings import warn
import math

from graph import Graph


class Graphexploration:

    def __init__(self, graph: Graph):
        """Constructor of the graph exploration class."""
        self.__graph = graph
        
        # Overview of already existing data for certain start vertices
        # The first digit indicates the status regarding DFS data and the second digit regarding BFS data
        # Example:  02 = no DFS data is available, BFS tree is available
        #           12 = Data from depth search available, BFS tree available
        # 2 - DFS tree is available
        # 1 - Data from the depth search are available
        # 0 - No data available
        # 1 - Data from the breath search are available
        # 2 - BFS tree is available

        self.__data_check = np.zeros(self.__graph.return_num_vertices())
        
        # Data storage
        self.__dfsNum = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__finNum = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__treeEdges = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__nonTreeEdges = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__backEdges = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__dfs_tree = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__bfs_dist = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__bfs_parent = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__bfs_tree = [None for i in range(0,self.__graph.return_num_vertices())]
        self.__shortest_paths = {}

    # Getter-methods for data of the DFS
    def return_dfsNum(self, startVertex = 0):
        """Returns DFS-numbers to given start vertex."""
        if self.__data_check[startVertex]//10 > 0:
            return self.__dfsNum[startVertex]
        else:
            self.__depthsearch(startVertex)
            return self.__dfsNum[startVertex]
        
    def return_finNum(self, startVertex = 0):
        """Returns DFS-numbers to given start vertex."""
        if self.__data_check[startVertex]//10 > 0:
            return self.__finNum[startVertex]
        else:
            self.__depthsearch(startVertex)
            return self.__finNum[startVertex]
            
    def return_nontreeedges(self, startVertex = 0):
        """Returns the non-tree egdes of the DFS tree with the given start vertex."""
        if self.__data_check[startVertex]//10 > 0:
            return self.__nonTreeEdges[startVertex]
        else:
            self.__depthsearch(startVertex)
            return self.__nonTreeEdges[startVertex]
    
    def return_backwardedges(self, startVertex = 0):
        """Returns the backward egdes of the DFS tree with the given start vertex."""
        if self.__data_check[startVertex]//10 > 0:
            return self.__backEdges[startVertex]
        else:
            self.__depthsearch(startVertex)
            return self.__backEdges[startVertex]
            
    def return_dfs_tree(self, startVertex = 0):
        """Returns DFS-tree to given start vertex."""
        if self.__data_check[startVertex]//10 == 2:
            return self.__dfs_tree[startVertex]
        elif self.__data_check[startVertex]//10 == 1:
            self.__create_dfs_Tree(startVertex)
            return self.__dfs_tree[startVertex]
        else:
            self.__depthsearch(startVertex)
            self.__create_dfs_Tree(startVertex)
            return self.__dfs_tree[startVertex]
	
    # Getter-methods for data of the BFS
    def return_bfsDist(self, startVertex = 0):
        """Returns BFS-distances to given start vertex."""
        if self.__data_check[startVertex] % 10 > 0:
            return self.__bfs_dist[startVertex]
        else:
            self.__breathsearch(startVertex)
            return self.__bfs_dist[startVertex]
            
    def return_bfsParent(self, startVertex = 0):
        """Returns parent vertex of each vertex of the BFS-tree with given start vertex as the root vertex."""
        if self.__data_check[startVertex] % 10 > 0:
            return self.__bfs_parent[startVertex]
        else:
            self.__breathsearch(startVertex)
            return self.__bfs_parent[startVertex]
        
    def return_bfsSpanningTree(self, startVertex = 0):
        """Returns BFS-tree to given start vertex."""
        if self.__data_check[startVertex] % 10 == 2:
            return self.__bfs_tree[startVertex]
        elif self.__data_check[startVertex] % 10 == 1:
            self.__create_bfs_spanningTree(startVertex)
            return self.__bfs_tree[startVertex]
        else:
            self.__breathsearch(startVertex)
            self.__create_bfs_spanningTree(startVertex)
            return self.__bfs_tree[startVertex]
        
    def return_shortestPath(self, startVertex, endVertex):
        """Returns a graph consisting of the shortest path between the given start and end vertex with respect to the number of edges."""
        if (startVertex, endVertex) in self.__shortest_paths:
            return self.__shortest_paths[(startVertex, endVertex)]
        
        prev = self.return_bfsParent(startVertex)
        # If no path exists:
        if prev[endVertex] == None :
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
            
        name_order = self.__graph.return_names()
        name_order = [x for x in name_order if x in list(zip(*sub_list))[0] or x in list(zip(*sub_list))[1]]
        out = Graph(sub_list, dtype=self.__graph.return_weightType(),  vertexNames=name_order)
        self.__shortest_paths[(startVertex, endVertex)] = out
        return out
        
    def return_graph(self):
        """Returns the considered graph."""
        return self.__graph
        
    # Subfunctions for DFS
    def __root(self, s, dfsNum, dfsPos):
        dfsNum[s] = dfsPos
        dfsPos += 1
        return dfsPos
        
    def __traverseNonTreeEdge(self, v, w, dfsNum, finNum, nonTreeEdges, backEdges):
        # Store non-tree and backward edges
        nonTreeEdges.append([v,w])
        if (not dfsNum[v] < dfsNum[w]) and (not finNum[w] < finNum[v]) and finNum[w] == 0:
            backEdges.append([v,w])
    
    def __traverseTreeEdge(self, v, w, dfsNum, dfsPos, treeEdges):
        dfsNum[w] = dfsPos
        dfsPos += 1
        # Store tree edge
        treeEdges.append([v,w])
        return dfsPos
        
    def __backtrack(self, u, v, finNum, finPos):
        finNum[v] = finPos
        finPos += 1
        return finPos
        
    def __dfs(self, u, v, dfsNum, dfsPos, finNum, finPos, treeEdges, nonTreeEdges, backEdges): # erkunde v, von u kommend
        """Performs the actual DFS prozedure."""
        if dfsNum[v] == 0: # If v has not been marked, mark v as active
            dfsNum[v] = dfsPos
            dfsPos += 1
        # Iterate over all outgoing edges of v. If edges are weighted, traverse edge with minimal weight first
        for w in sorted(self.__graph.return_adjacencies(v), key=lambda edge: edge[1]):
            if dfsNum[w[0]] != 0: # If w has already been traversed:
                self.__traverseNonTreeEdge(v,w[0], dfsNum, finNum, nonTreeEdges, backEdges)
            else: # If w has not been traversed yet
                dfsPos = self.__traverseTreeEdge(v, w[0], dfsNum, dfsPos, treeEdges)
                dfsPos, finPos = self.__dfs(v, w[0], dfsNum, dfsPos, finNum, finPos, treeEdges, nonTreeEdges, backEdges)
        finPos = self.__backtrack(u, v, finNum, finPos) # Knoten v als beendet markieren
        return dfsPos, finPos
    
    def __dfs_init(self, dfsNum, finNum, dfsPos, finPos, treeEdges, nonTreeEdges, backEdges, startVertex):
        vertexList = list(np.arange(self.__graph.return_num_vertices()))
        vertexList.remove(startVertex)
        vertexList = [startVertex] + vertexList
        for s in vertexList:
            if dfsNum[s] == 0:
                dfsPos = self.__root(s, dfsNum, dfsPos)
                dfsPos, finPos = self.__dfs(s, s, dfsNum, dfsPos, finNum, finPos, treeEdges, nonTreeEdges, backEdges)
    
    def __depthsearch(self, startVertex):
        """Executes the depth search with given start vertex on the graph."""
        # Arrays to store the temporal DFS-numbers, the final DFS-numbers as well as all tree, non-tree and backward edges
        dfsNum = np.zeros(self.__graph.return_num_vertices())
        finNum = np.zeros(self.__graph.return_num_vertices())
        treeEdges = []
        nonTreeEdges = []
        backEdges = []

        dfsPos = 1
        finPos = 1
        self.__dfs_init(dfsNum, finNum, dfsPos, finPos, treeEdges, nonTreeEdges, backEdges, startVertex)
        # Store computed values
        self.__dfsNum[startVertex] = tuple(dfsNum)
        self.__finNum[startVertex] = tuple(finNum)
        self.__treeEdges[startVertex] = tuple(treeEdges)
        self.__nonTreeEdges[startVertex] = tuple(nonTreeEdges)
        self.__backEdges[startVertex] = tuple(backEdges)
        self.__data_check[startVertex] = 10 + self.__data_check[startVertex]%10
        
    def __create_dfs_Tree(self, startVertex):
        """Creates a DFS-tree with the given start vertex."""
        sub_list = []
        orig_mat = self.__graph.return_adjacencyMatrix()
        edges = self.__treeEdges[startVertex]
        for e in edges:
            sub_list.append( (self.__graph.return_vertexName(e[0]),self.__graph.return_vertexName(e[1]),orig_mat[e[0]][e[1]]) )
            
        # Store computed values
        if len(sub_list) > 0:
            name_order = self.__graph.return_names()
            name_order = [x for x in name_order if x in list(zip(*sub_list))[0] or x in list(zip(*sub_list))[1]]
            self.__dfs_tree[startVertex] = Graph(sub_list, dtype=self.__graph.return_weightType(), vertexNames=name_order)
        else: # Special case: No edges
            self.__dfs_tree[startVertex] =  Graph(np.array([[0]], dtype=self.__graph.return_weightType()), vertexNames=[self.__graph.return_vertexName(startVertex)])
        
        self.__data_check[startVertex] = 20 + self.__data_check[startVertex]%10

    def __breathsearch(self, startVertex = 0):
        """Executes the BFS with the given start vertex."""

        dist = np.array([math.inf for i in range(0,self.__graph.return_num_vertices())]) # Stores distances of each vertex to the root
        parent = np.array([None for i in range(0,self.__graph.return_num_vertices())]) # Stores parent of each vertex
        
        # Set root vertex
        dist[startVertex] = 0 
        parent[startVertex] = startVertex
        
        Q = [startVertex] # current layer of the BFS-tree
        Q_strich = [] # next layer of the BFS-tree
        dist_count = 0
        
        while len(Q) > 0: # Explore layer after layer
            dist_count += 1
            for u in Q: 
                for v in self.__graph.return_adjacencies(u): # Travesere outgoing edges of u
                    if parent[v[0]] == None: # Until non-travesered vertex is found
                        Q_strich.append(v[0])
                        dist[v[0]] = dist_count
                        parent[v[0]] = u # Update BFS-tree
            # Switch to next layer
            Q = Q_strich
            Q_strich = []
        
        # Print warning if not all vertices have been visited by the BFS
        if np.any(dist == math.inf):
            warn(Warning("During the executed width search, not all nodes in the graph could be reached from the selected start node."))
        
        # Set parent of the root vertex to none
        parent[startVertex] = None
        # Store computed values
        self.__bfs_dist[startVertex] = tuple(dist)
        self.__bfs_parent[startVertex] = tuple(parent)
        self.__data_check[startVertex] += 1
        
    def __create_bfs_spanningTree(self, startVertex = 0):
        """Creates BFS-tree with given start vertex."""
        sub_list = []
        orig_mat = self.__graph.return_adjacencyMatrix()
        prev = self.__bfs_parent[startVertex]
        for j in range(0,len(prev)):
            i = prev[j]
            if i!=None:
                sub_list.append((self.__graph.return_vertexName(i),self.__graph.return_vertexName(j),orig_mat[i][j]))
        # Store computed values
        if len(sub_list) > 0:
            name_order = self.__graph.return_names()
            name_order = [x for x in name_order if x in list(zip(*sub_list))[0] or x in list(zip(*sub_list))[1]]
            self.__bfs_tree[startVertex] = Graph(sub_list, dtype=self.__graph.return_weightType(), vertexNames=name_order)
        else: # Special case: No edges
            self.__bfs_tree[startVertex] =  Graph(np.array([[0]], dtype=self.__graph.return_weightType()), vertexNames=[self.__graph.return_vertexName(startVertex)])
        
        self.__data_check[startVertex] += 2
