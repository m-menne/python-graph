import numpy as np
import igraph as ig
import random as rd
from graph import Graph

class Visu:    
    def __init__(self, g: Graph, **optional):
        
        if "w" in optional:
            width = optional["w"]
        else:
            width = 500
        if "h" in optional:
            height = optional["h"]
        else:
            height = 500
        if "directed" in optional:
             self.__directed = optional["directed"]
        else:
            self.__directed = True
        if "seed" in optional:
            seed = optional["seed"]
        else:
            seed = 123
            
        if not self.__directed:
           if not np.allclose(g.return_adjacencyMatrix(), g.return_adjacencyMatrix().T, atol=1e-6):
               raise ValueError("The given graph has no symmetrical adjacency matrix! In order to draw the graph in an undirected way, the adjacency matrix must be symmetrical.")
            
        self.__vi_graph = ig.Graph(directed= self.__directed)
        rd.seed(seed)
        self.__graph = g
        # Introduction of some abbreviations for simplification
        self.__size = self.__graph.return_num_vertices
        self.__get_adj = self.__graph.return_adjacencies
        self.__vi_graph.add_vertices(self.__size())
        # Pass the adjacency list to igraph
        for i in range(0,self.__size()):
            if len(self.__get_adj(i))>0: 
                for j in self.__get_adj(i):
                    if self.__directed or i<j[0]:
                        self.__vi_graph.add_edge(i, j[0], weight=j[1])
                    
        # Settings for visualization
        self.__visual_style = {}
        self.__visual_style["bbox"] = (width, height)
        self.__visual_style["edge_width"] = np.ones(self.__size())
        self.__visual_style["margin"] = 60    
        self.__visual_style["vertex_color"] = [(255,255,255) for x in range(0,self.__size())]
        self.__visual_style["edge_color"] = [(0,0,0) for x in range(0,g.return_num_edges())]
        self.__visual_style["edge_width"] = [1 for x in range(0,g.return_num_edges())]
        self.__visual_style["vertex_label"] = g.return_names()
        layout = self.__vi_graph.layout("kk")
        self.__visual_style["layout"] = layout
        
    def remove_marks(self):
        """Removes all marks."""
        self.__visual_style["vertex_color"] = [(255,255,255) for x in range(0,self.__size())]
        self.__visual_style["edge_color"] = [(0,0,0) for x in range(0,self.__graph.return_num_edges())]
        self.__visual_style["edge_width"] = [1 for x in range(0,self.__graph.return_num_edges())]
        
    def mark_subgraph(self, sub: Graph, color=(255,0,0)):
        """Marks the given graph in the original graph. Generates an error if the given graph is not a subgraph."""
        if not type(color) is tuple or len(color)<3 or len(color)>4:
            raise TypeError("\'color\' has to be a 3- or 4-tuple.")
        if not sub.is_subgraph_of(self.__graph):
            raise ValueError("\'sub\' is no subgraph.")
        # Traverses each vertex of the subgraph and marks it in the supergraph
        mark_names = sub.return_names()
        for name in mark_names:
            self.__visual_style["vertex_color"][self.__graph.return_vertexIndex(name)] = color
            
            # Marks all out-going edges of the vertices of the subgraph
            adj_sub = sub.return_adjacencies(sub.return_vertexIndex(name))
            for edge in adj_sub:
                vertexIndex = self.__graph.return_vertexIndex(sub.return_vertexName(edge[0]))
                if  self.__directed:
                    index = self.__vi_graph.get_edgelist().index((self.__graph.return_vertexIndex(name),vertexIndex))
                else:
                    # If the graph is undirected, check both directions
                    if (self.__graph.return_vertexIndex(name),vertexIndex) in self.__vi_graph.get_edgelist():
                        index = self.__vi_graph.get_edgelist().index((self.__graph.return_vertexIndex(name),vertexIndex))
                    else:
                        index = self.__vi_graph.get_edgelist().index((vertexIndex,self.__graph.return_vertexIndex(name)))
                    
                self.__visual_style["edge_color"][index] = color
                self.__visual_style["edge_width"][index] = 2
        
    
    def visualize(self, name=None):
        """Plots and stores the graph, if a filename is specified. Otherwise the plot is sent to the standard image viewer."""
        if name==None:
            ig.plot(self.__vi_graph, **self.__visual_style)
        else:            
            ig.plot(self.__vi_graph, name, **self.__visual_style)
        
