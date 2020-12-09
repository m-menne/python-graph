import numpy as np
import random
from warnings import warn

def random_graph(numVertices: int, edgeWeight = True, edgeDensity=0.1):
    """Produces a random graph with given edge density"""
    if numVertices < 1:
        raise ValueError("The number of vertices have to be at least 1.")
    if edgeDensity > 1.0 or edgeDensity < 0:
        raise ValueError("The edge density should be within the range of [0,1].")
    # Calculating the number of edges from the given edge density
    numEdges = int((numVertices**2-numVertices) * edgeDensity)
    
    # Generate edges
    edges = [(i,j) for i in range(0,numVertices) for j in range(0,numVertices) if i != j]
    edges = random.sample(edges,numEdges)
    
    # Create adjacency matrix
    if edgeWeight:
        mat = np.zeros((numVertices, numVertices), dtype= np.float64)
    else: 
        mat = np.zeros((numVertices, numVertices), dtype= np.int32)
    for edge in edges:
        if edgeWeight:
            mat[edge[0]][edge[1]] = random.random()
        else: mat[edge[0]][edge[1]] = 1.0
    
    # Generate and return graph
    return Graph(mat, dtype = np.float64)
    

class Graph:
    def __init__(self, graph, **optional):
        """Constructor chooses either the adjacency list constructor or adjacency matrix constructor"""
        if type(graph)==np.ndarray: 
            self.__init_matrix(graph, **optional)
        elif type(graph)==list:
            self.__init_list(graph, **optional)
        else:
            raise TypeError("\'graph\' must be either a numpy array or a adjacency list [(i,j,w), ...].")
        # To keep the attributes immutable, they are stored as tuples
        self.__adj = tuple([tuple(x) for x in self.__adj])
        self.__name_list = tuple(self.__name_list)
        # __mat Access restriction to read-only
        self.__mat = np.copy(self.__mat)
        self.__mat.flags.writeable = False
        
    def __init_list(self, adjlist, **optional): 
        """Adjacency list constructor, which creates a graph from the given adjacency list"""
		# Error handling
        if any([len(x)!=3 for x in adjlist]):
            raise TypeError("The adjacency list may only have entries of the form (i,j,weight).")
        elif any(x[2]<=0 for x in adjlist):
            raise ValueError("Weights must be > 0.")
        elif any(x[0]==x[1] for x in adjlist):
            raise ValueError("The graph must not contain circles of length 1.")
        
        if "vertexNames" in optional:
            node_order = optional["vertexNames"]
        else:
            node_order = None
            warn(Warning("If the parameter \'vertexNames\' is not set in the adjacency list representation of the graph, the indexing is not deterministic."))
        if not "dtype" in optional:
            warn(Warning("If the parameter \'dtype\' has not been set in the adjacency list representation, then the values will automatically be casted to float32."))
            self.__type = np.float32
        else:
            self.__type = optional["dtype"]
                
        
        # List of names
        if node_order == None:
            self.__name_list = list(set([y for x in [(x[0],x[1]) for x in adjlist] for y in x]))
        else:
            self.__name_list = node_order
            if not set([y for x in [(x[0],x[1]) for x in adjlist] for y in x]).issubset(set(node_order)):
                raise ValueError("The passed list of names does not contain the same node names as the node names from the adjacency list.")
            
        # Number of edges
        self.__size = len(self.__name_list)
        # Hashmap name->index
        self.__names = {self.__name_list[i]: i for i in range(0,self.__size)}
        # adjacency matrix
        self.__mat = np.zeros((self.__size, self.__size), dtype=self.__type)
        # adjacency list
        self.__adj = [[] for i in range(0,self.__size)]
        # Used to cast the values to the given datatype
        cast_to = np.array([0,0], dtype=self.__type)[0]
        for edge in adjlist:
            i = self.__names[edge[0]]
            j = self.__names[edge[1]]
            # Cast weights to given datatype
            self.__adj[i].append((j, type(cast_to)(edge[2])))            
            self.__mat[i][j] = type(cast_to)(edge[2])
            
        # List of known supergraphs
        self.__supergraph = []
        
    def __init_matrix(self, adjacencyMatrix, **optional):
        """Adjacency matrix constructor, which creates a graph from the given adjacency matrix"""
		# Error handling
        if adjacencyMatrix.ndim!=2 or adjacencyMatrix.shape[0]!=adjacencyMatrix.shape[1]:
            raise TypeError("\'adjacencyMatrix\' has to be a square matrix.")
        elif np.any(adjacencyMatrix<0):
            raise ValueError("The weights have to be positive.")
        elif not (str(adjacencyMatrix.dtype).startswith("float") or str(adjacencyMatrix.dtype).startswith("int")):
            raise TypeError("Weights have to be of the type \'float*\' or \'int*\'.")
        elif np.any(np.diagonal(adjacencyMatrix)):
            raise ValueError("The graph is not allowed to contain circles of length 1.")
		# Save shape and type
        self.__size = adjacencyMatrix.shape[0]
        self.__type = adjacencyMatrix.dtype
        if "vertexNames" in optional:
            # List of names
            self.__name_list = optional["vertexNames"]
            if len(self.__name_list)!=self.__size:
                raise ValueError("There have not been specified as many names in \'vertexNames\' as there are nodes.")
            else:
                if len(set(self.__name_list)) != len(self.__name_list):
                    raise ValueError("Vertex names are not unique.")
                else:
                    # Hashmap name->index
                    self.__names = {self.__name_list[i]:i for i in range(0,self.__size)}
        else:
            warn(Warning("If node names in adjacency matrix representation are not explicitly set with the parameter \'vertexNames\', partial and supergraphs cannot be recognized reliably."))
            self.__name_list = [i for i in range(0,self.__size)]
            self.__names = {self.__name_list[i]:i for i in range(0,self.__size)}
            
        # Adjacency matrix
        self.__mat = adjacencyMatrix
        # Adjacency matrix
        self.__adj = [[(i,self.__mat[vertices][i]) for i in np.arange(self.__size) if self.__mat[vertices][i]>0] for vertices in np.arange(0,self.__size)]
        
        # List of known supergraphs
        self.__supergraph = []
        
        
    # Getter-methods
    def is_adjacent(self, startVertex: np.int_ , endVertex: np.int_):
        """Returns whether the start node is adjacent to the end node"""
        return self.__mat[startVertex][endVertex]>0
		
    def return_weight(self, startVertex: np.int, endVertex:np.int):
        """Returns the weight of an edge (startVertex, endVertex)"""
        return self.__mat[startVertex][endVertex]
		
    def return_num_vertices(self):
        """Returns the number of nodes of the graph"""
        return self.__size
		
    def return_num_edges(self):
        """Returns the number of edges of the graph"""
        return sum(map(lambda x: len(x),self.__adj))
        
    def return_outdeg(self, vertex: np.int_):
        """Returns the output degree of the selected node"""
        return len(self.__adj[vertex])
        
    def return_indeg(self, vertex: np.int_):
        """Returns the output degree of the selected node"""
        return sum(map(lambda x: x>0,self.__mat[:,vertex]))
        
    def return_adjacencies(self, vertex: np.int_):
        """Returns all nodes that are adjacent to the selected node with the corresponding edge weight"""
        return self.__adj[vertex]
        
    def return_adjacencyMatrix(self):
        """Returns the adjacency matrix of the graph"""
        return self.__mat
        
    def return_adjacencyList(self):
        """Returns the adjacency list of the graph"""
        return self.__adj
        
    def return_weightType(self):
        """Returns the data type of the edge weights"""
        return self.__type

    def return_names(self):
        """Returns the names of the nodes of the graph"""
        return self.__name_list
        
    def return_vertexIndex(self, name):
        """Returns the index of a node, given a name"""
        return self.__names[name]
        
    def return_vertexName(self, index):
        """Returns the name of a node, given an index"""
        return self.__name_list[index]
    
    def is_subgraph_of(self, other):
        """Returns 'True' if the considered graph is a subgraph of the given graph, otherwise 'False'"""
        # If it is already recognized that it is a subgraph this procedure can be skipped.
        if other in self.__supergraph :
            return True
        
        if type(self)!=type(other):
            raise TypeError("Only works between graphs.")
        elif other.return_num_vertices() == 0:
            return False
        elif self.return_num_vertices() == 0:
            return True
        names_to_check = self.return_names()
        # Checks if the vertices are a subset
        if not set(names_to_check).issubset(set(other.return_names())):
            return False
        
        # Traverses each node and checks if the adjacencies build a subset.
        # To do so, the node indices must be replaced by node names.
        # This is laborious, but only needs to be done once.
        for name in names_to_check:
            selflist  = set(map(lambda x: (self.return_vertexName(x[0]),x[1]), self.return_adjacencies(self.return_vertexIndex(name))))
            otherlist = set(map(lambda x: (other.return_vertexName(x[0]),x[1]), other.return_adjacencies(other.return_vertexIndex(name))))
            if not selflist.issubset(otherlist):
                return False
        self.__supergraph.append(other)
        
        return True
