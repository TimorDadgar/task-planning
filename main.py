from topmap import *
from voronoi import *
import random



T = top_map()

T.generate_random(20, 0, 256, 4)   # (number of nodes, min_xy, max_xy, number of sensors)

given_nodes = [(random.uniform(min_xy, max_xy), random.uniform(min_xy, max_xy)) for i in range(10)]
# given_nodes = T.nodes

vor = Voronoi(given_nodes)  # using scipy Voronoi library to create voronoi diagram of given points
E = get_edges_for_graph(given_nodes)
G = T.to_graph(E)
visualise_voronoi(given_nodes, E)


