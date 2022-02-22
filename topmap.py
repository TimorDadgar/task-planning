from random import *

from math import *

# ____for drawing the graph.____
import networkx as nx
import matplotlib.pyplot as plt
K = nx.Graph()
class top_map:
    def __init__(self):
        self.nodes = []
        self.sensors = []
        
    def generate_random(self, n_nodes, minxy, maxxy, n_sensors):
        self.nodes = []
        self.sensors = []
        for i in range(n_sensors):
            self.sensors.append(randint(0, n_nodes-1))
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
                        #K.add_edge(i, j, color='gray', weight=0.1)
                    G[i][j] = sqrt((N[i][0]-N[j][0])**2 + (N[i][1]-N[j][1])**2)

                    # print(G[i][j])
        return G


T = top_map()
T.generate_random(20, 0, 256, 4)   # (number of nodes, min_xy, max_xy, number of sensors)
G = T.to_graph()


for i in range(20):
    for j in range(20):
        N = T.nodes
        if j in G[i] and random() > (8192 / ((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2))**6:
            G[i].pop(j)
            G[j].pop(i)

