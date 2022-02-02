from random import *

class top_map:
    def __init__(self):
        self.nodes = [];
        
    def generate_random(self, n_nodes, minxy, maxxy):
        self.nodes = []
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
                    G[i][j] = (N[i][0]-N[j][0])**2 + (N[i][1]-N[j][1])**2
                    #print(G[i][j])
        return G
        

T = top_map()
T.generate_random(20,0,256)
G = T.to_graph()
