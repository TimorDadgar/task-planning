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

    """"
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
    """
    def to_graph(self, edges):
        G = dict()
        N = self.nodes
        for e in edges:
            if e[0] not in G.keys():
                G[e[0]] = dict()
            if e[1] not in G.keys():
                G[e[1]] = dict()
            G[e[0]][e[1]] = sqrt((N[e[0]][0]-N[e[1]][0])**2 + (N[e[0]][1]-N[e[1]][1])**2)
            G[e[1]][e[0]] = sqrt((N[e[0]][0] - N[e[1]][0]) ** 2 + (N[e[0]][1] - N[e[1]][1]) ** 2)
        return G



""""
for i in range(20):
    for j in range(20):
        N = T.nodes
        if j in G[i] and random() > (8192 / ((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2))**6:
            G[i].pop(j)
            G[j].pop(i)
"""
from voronoi import *

min_xy = 0  # minimum range of x,y
max_xy = 256   # maximum range of x,y

# given_nodes = [(random.uniform(min_xy, max_xy), random.uniform(min_xy, max_xy)) for i in range(10)]
T = top_map()

T.generate_random(20, min_xy, max_xy, 4)   # (number of nodes, min_xy, max_xy, number of sensors)

given_nodes = T.nodes

E = get_edges_for_graph(given_nodes)
print(E)

G = T.to_graph(E)
visualise_voronoi(given_nodes, E)