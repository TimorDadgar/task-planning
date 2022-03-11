from scipy.spatial import voronoi_plot_2d, Voronoi, Delaunay
import matplotlib.pyplot as plt
import networkx as nx
import random
import math


x_max_min = ()   # (max, min) x values of given nodes
y_max_min = ()    # (max, min) y values of given nodes
offset = 1  # offset for the accepted voronoi region
added_nodes = set()


def create_graph_edges(n_n):
    global added_nodes
    edge_l = []     # create local list we will return
    for i in range(len(n_n)):
        n1 = n_n[i][0]  # assign n1 in n_n to local var n1 to get more readable code
        n2 = n_n[i][1]  # assign n2 in n_n to local var n2 to get more readable code
        n3 = n_n[i][2]  # assign n3 in n_n to local var n3 to get more readable code
        added_nodes.add(n1)
        added_nodes.add(n2)
        added_nodes.add(n3)
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


def calc_vertex(tri, vor):
    vertex_n_l = []   # create local list we will return
    print(len(tri.vertices), len(vor.vertices))
    for i in range(len(vor.vertices)):
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


def calc_distance(n1, n_l):
    c_d = math.inf
    c_n = None
    for i in range(len(n_l)):
        n2 = n_l[i]
        if n1 == n2:
            continue
        else:
            d = math.sqrt((pow(n2[0] - n1[0], 2)) + (pow(n2[1] - n1[1], 2)))
            if d < c_d:
                c_d = d
                c_n = i
    return c_n


def check_for_empty_node(n_l, e_l):
    for i in range(len(n_l)):
        if i not in added_nodes:
            c_n = calc_distance(n_l[i], n_l)
            e_l.append((i, c_n))
            added_nodes.add(i)


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
    global vor
    vor = Voronoi(given_nodes)  # using scipy Voronoi library to create voronoi diagram of given points
    tri = Delaunay(given_nodes)    # using scipy Delaunay library to triangulate given points
    calc_xy_max_min(given_nodes)    # calculate the (max, min) values for x,y of given nodes
    vertex_node_n = calc_vertex(tri, vor)     # check which vertices that is in the accepted voronoi region
    edge_list = create_graph_edges(vertex_node_n)  # create edge list from vertex node neighbor list
    check_for_empty_node(given_nodes, edge_list)
    print(edge_list)

    return edge_list


def visualise_voronoi(given_nodes, edge_list):
    global vor
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
    #plt.show()


#n = 15   # number of points to generate

#test_nodes = [(random.uniform(-5, 5),random.uniform(-5, 5)) for i in range(n)]  # generates n numbers of random points
#test_nodes = [(1.2547800514351115, -0.7215606591710655), (3.6337368926452935, -4.995631025070335), (0.918546225362368, 2.5292394478198563), (1.307224728044675, -2.489504820947901)]

#Weird case no edges, gives edges only to two pairs of nodes. Could have added a check that adds an edge to the second closest node
# instead of the closest node. This will not be a problem with n amount of nodes.
#test_nodes = [(2.3709415468095667, 3.768823190049382), (2.3501222781943554, 2.96306969504694), (4.173247078390004, -1.3651226961868677), (2.9444466329461028, -3.447544532073805)]

#Case where our implementation works well, in the case sensor might have been nodes, 13 or 5
#test_nodes = [(3.0634010222286836, -0.8639108250866476), (-1.4966553333303856, -1.0839981993876768), (-1.4942957955659555, 2.6664818820202543), (2.783680472930059, 1.617018931312768), (-2.800201162728663, 3.9424020100825725), (4.379611567834591, -4.068593094471076), (-1.61152034835081, 0.7523775107295432), (3.7873134371897557, -3.4505628326554105), (3.3753974338197175, 0.6038481608856507), (3.9061418964142405, 3.039121218394774), (-3.892100167690856, 1.324433374461754), (3.0062381090314965, 0.36869672002892884), (-2.806047011726167, 3.648443928691796), (4.96465734782644, -4.7635734287225615), (1.387641281252547, 3.8566573478081025)]

#E = get_edges_for_graph(test_nodes)
#visualise_voronoi(test_nodes, E)

# print statements for bug fixing
""""
for i in range(len(given_nodes)):
    print(given_nodes[i])
print("ver", tri.vertices)
print(nodes_n)
print(edge_list)
"""

