from random import *

from math import *

# ____for drawing the graph.____
import networkx as nx
import matplotlib.pyplot as plt

class top_map:
    def __init__(self):
        self.nodes = []
        self.sensors = []
        
    def generate_random(self, n_nodes, minxy, maxxy, n_sensors):
        self.nodes = []
        self.sensors = []
        for i in range(n_sensors):
            self.sensors.append(randint(0, n_nodes))
        for i in range(n_nodes):
            self.nodes.append( (uniform(minxy, maxxy), uniform(minxy,maxxy) ))
            #print(self.nodes[i])

    def to_graph(self):
        G = dict()
        N = self.nodes
        for i in range(len(N)):
            G[i] = dict()
            for j in range(len(N)):
                if i != j:
                    G[i][j] = sqrt((N[i][0]-N[j][0])**2 + (N[i][1]-N[j][1])**2)
                    #print(G[i][j])
        return G


T = top_map()
T.generate_random(20, 0, 256, 4)   # (number of nodes, min_xy, max_xy, number of sensors)
G = T.to_graph()

K = nx.Graph()
