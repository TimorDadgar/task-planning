from scipy.spatial import voronoi_plot_2d, Voronoi, Delaunay
import matplotlib.pyplot as plt
import networkx as nx
import random

vor = None

def create_graph_edges(n_n):
    edge_l = []     # create local list we will return
    for i in range(len(n_n)):
        n1 = n_n[i][0]  # assign n1 in n_n to local var n1 to get more readable code
        n2 = n_n[i][1]  # assign n2 in n_n to local var n2 to get more readable code
        n3 = n_n[i][2]  # assign n3 in n_n to local var n3 to get more readable code

        if (n1, n2) not in edge_l and (n2, n1) not in edge_l:   # check for duplicates in edge_l
            edge_l.append((n1, n2))     # append edge between (n1, n2) if not already in edge_l
        if (n2, n3) not in edge_l and (n3, n2) not in edge_l:
            edge_l.append((n2, n3))
        if (n3, n1) not in edge_l and (n1, n3) not in edge_l:
            edge_l.append((n3, n1))
    return edge_l   # return local list


def add_nodes(graph, n_l):
    for i in range(len(n_l)):
        graph.add_node(i, pos=n_l[i])   # add node to graph and assign correct cords to that node


def calc_vertex(tri):
    vertex_n_l = []   # create local list we will return
    for i in range(len(tri.vertices)):
        x = vor.vertices[i][0]      # assign vertices x value to local var x to get more readable code
        y = vor.vertices[i][1]      # assign vertices y value to local var y to get more readable code

        # if vertices x,y values is greater/smaller than the max/min value of the given nodes x,y values,
        # we can assume that the vertex is outside the accepted voronoi region. Therefor we will not
        # append that vertex's neighboring nodes to the vertex_n_list (should not be an edge between them)
        if x > x_max_min[0] or x < x_max_min[1] or y > y_max_min[0] or y < y_max_min[1]:
            continue
        else:
            vertex_n_l.append(tri.vertices[i])   # append neighboring nodes to vertex
    return vertex_n_l     # return local list


def calc_xy_max_min(n_l):
    global x_max_min
    global y_max_min
    global offset
    x_list = []     # create local list to hold all x values
    y_list = []     # create local list to hold all y values
    for i in range(len(n_l)):   # go through all x,y values and append them to each list
        x_list.append(n_l[i][0])
        y_list.append(n_l[i][1])

    x_max_min = (max(x_list)+offset, min(x_list)-offset)    # set (max, min) values for x
    y_max_min = (max(y_list)+offset, min(y_list)-offset)    # set (max, min) values for y


def get_edges_for_graph(given_nodes):  # replace n with given_nodes later

    # generates n numbers of random nodes
    global vor
    vor = Voronoi(given_nodes)  # using scipy Voronoi library to create voronoi diagram of given points
    tri = Delaunay(given_nodes)    # using scipy Delaunay library to triangulate given points

    calc_xy_max_min(given_nodes)    # calculate the (max, min) values for x,y of given nodes
    vertex_node_n = calc_vertex(tri)     # check which vertices that is in the accepted voronoi region
    edge_list = create_graph_edges(vertex_node_n)  # create edge list from vertex node neighbor list
    print(edge_list)

    return edge_list


def visualise_voronoi(given_nodes, edge_list):
    # create visual graph with help of networkx library
    G = nx.Graph()  # create networkx graph
    add_nodes(G, given_nodes)  # add nodes to networkx's graph
    G.add_edges_from(edge_list)  # add edges not networkx's graph

    # draw graph with nodes and edges
    nx.draw(G, nx.get_node_attributes(G, 'pos'), font_color='w', edge_color='b', with_labels=True, font_weight='bold')

    # draw voronoi diagram with given nodes
    voronoi_plot_2d(vor)
    plt.figure()
    # draw graph with nodes and edges inside the voronoi diagram
    # nx.draw(G, nx.get_node_attributes(G, 'pos'), font_color='w', edge_color='b', with_labels=True, font_weight='bold')

    # show drawings with the help of matplotlib library
    # plt.show()


x_max_min = ()   # (max, min) x values of given nodes
y_max_min = ()    # (max, min) y values of given nodes
offset = 1  # offset for the accepted voronoi region



# print statements for bug fixing
""""
for i in range(len(given_nodes)):
    print(given_nodes[i])
print("ver", tri.vertices)
print(nodes_n)
print(edge_list)
"""

