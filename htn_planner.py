from algorithm import *
import copy

class State():
    def __init__(self):
        self.pos = {}
        self.carrying = set()


# Operators
def goto(state, p):
    state.pos['r'] = p
    return state


def pickup(state, i):
    state.carrying = state.carrying | {i}
    return state


def drop(state, i):
    state.carrying -= {i}
    return state


# Methods
# Returns a set of goto statements required to go from l1 to l2, uses best-first
def move_robot(state, l1, l2):
    if l1 == l2:  # already there
        return []
    if state.pos['r'] != l1:  # wrong start
        return False
    problem = Problem(l1, l2)  # the path is a sub-problem handled in algorithm.py
    heuristic = (lambda n: n.path_cost + sqrt(
        (T.nodes[n.state][0] - T.nodes[l2][0]) ** 2 + (T.nodes[n.state][1] - T.nodes[l2][1]) ** 2))
    # distance from explored node to goal
    path = best_first_graph_search(problem, heuristic)
    if path is None:  # impossible to get there
        return None
    path = path.path()  # the path leading up to final node
    plan = []  # for appending command.
    for i in range(1, len(path)):
        plan.append(('goto', path[i].state))
        goto(state, path[i].state)
    return plan


def pickup_item(state, loc, i):
    s = []  # set of instructions to achieve goal
    if state.pos['r'] != loc:  # if not at the sensor, go there
        s = move_robot(state, state.pos['r'], loc)
    pickup(state, i)
    s.append(('pickup', i))
    return s


def drop_item(state, loc, i):
    if i in state.carrying:
        s = []
        if state.pos['r'] != loc:
            s = move_robot(state, state.pos['r'], loc)
        drop(state, i)
        s.append(('drop', i))
        return s
    else:  # if not having the item
        p = pickup_item(state, state.pos['s'+str(i)], i)  # get it
        p.extend(drop_item(state, loc, i))  # proceed with having it
        return p


# currently unused
def take_picture(state, loc, c):
    if state.pos['r'] == loc:
        return [('capture', c)]
    else:
        return False


# not in practical use
def test_of_applying_sensors(l):
    loc = l[len(l)-1][0][1]
    sensor = 'camera1'
    if loc in T.sensors:
        command = pickup_item(state1, loc, sensor)
        l.append(command)
        pickup(state1, sensor)
        command2 = take_picture(state1, loc, sensor)
        l.append(command2)
        command3 = drop_item(state1, loc, sensor)
        l.append(command3)
        drop(state1)


# a function for conveniently calculating distance between nodes (lines would otherwise be very long)
def distn(i, j):
    N = T.nodes
    return sqrt((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2)


# execute the set of tasks to do
def dotodo(state, todo):
    pos = copy.copy(state.pos) # for restoring state
    # plan each subtask separately at first, as if each done from initial condition
    plans = []
    for t in todo:
        p = t(state)
        plans.append(p)
        state.pos = copy.copy(pos)
    plan = []
    # for as long as there are tasks to add to the ultimate single plan
    while len(plans):
        mind = float(inf)  # minimal distance
        mini = 0  # index of minimal distance
        for i in range(len(plans)):  # for each sub-plan
            p = plans[i]
            d = 0  # distance of current plan
            j = 0  # instruction index
            olp = state.pos['r']  # to restore the position after exploration
            while j < len(p) and p[j][0] == 'goto':  # for as long as movement is required
                d += distn(olp, p[j][1])
                olp = p[j][1]
                j += 1
            if d < mind:
                mind = d
                mini = i

        plan.append(plans[mini].pop(0))  # add the instruction(s) that require the least distance to get something done
        while plan[-1][0] == 'goto':  # all the movement up until accomplishing something
            K.add_edge(state.pos['r'], plan[-1][1], color='black', weight=3)
            state.pos['r'] = plan[-1][1]
            plan.append(plans[mini].pop(0))
        # do whatever need to be done at destination
        if plan[-1][0] == 'drop':
            state.pos['s' + str(plan[-1][1])] = state.pos['r']
        if len(plans[mini]) == 0:  # if the subplan is completed, remove it
            plans.pop(mini)
        else:  # the location may contain several things to do at
            while plans[mini][0][0] != 'goto':
                plan.append(plans[mini].pop(0))
                if plan[-1][0] == 'drop':
                    state.pos['s'+str(plan[-1][1])] = state.pos['r']
                if len(plans[mini]) == 0:
                    plans.pop(mini)
                    break
        # after moving to a new location, new paths are needed to each other location
        for i in range(len(plans)):
            pos = state.pos['r']  # eventually the destination
            while plans[i][0][0] == 'goto':
                op = plans[i].pop(0)
                pos = op[1]
            olp = state.pos['r']
            mov = move_robot(state, state.pos['r'], pos)
            mov.reverse()  # inserting each movement at index zero, reversing this order makes it easy
            for m in mov:
                plans[i].insert(0, m)
            state.pos['r'] = olp
    return plan


state1 = State()

state1.pos['r'] = startp = randint(0, 19)

for i in range(len(T.sensors)):
    state1.pos['s' + str(i)] = T.sensors[i]
print(state1.pos)
# each sensor's position to be dropped
goal1 = randint(0, 19)
goal2 = randint(0, 19)
goal3 = randint(0, 19)
goal4 = randint(0, 19)
todo = [lambda state: drop_item(state, goal1, 0), lambda state: drop_item(state, goal2, 1),
        lambda state: drop_item(state, goal3, 2), lambda state: drop_item(state, goal4, 3)]


# the position in graph to draw nodes
# i= index, T.nodes coordinate on each node
pos = {i: T.nodes[i] for i in range(len(T.nodes))}


plan = dotodo(state1, todo)
print(plan)


# if the nodes not part of the plan are to be drawn
drawall = True
if drawall:
    for i in range(len(T.nodes)):
        K.add_edge(i, i)


col = ['green' if node in T.sensors else 'yellow' for node in K]  # green for pickup place, yellow for nothing special
colind = dict()  # color index. This gets a little complicated when not all nodes are drawn
for i in range(len(T.nodes)):
    j = 0
    for node in K:
        if node == i:
            colind[i] = j
        j += 1

col[colind[startp]] = 'cyan'  # start position color

for k in state1.pos.keys():
    if k[0] == 's':
        col[colind[state1.pos[k]]] = 'violet'  # drop position color

col[colind[plan[-2][1]]] = 'red'  # end position color

# drawing in random layout
nx.draw(K, pos=pos, with_labels=True, node_color=col, edge_color=nx.get_edge_attributes(K, 'color').values(),
        width=list(nx.get_edge_attributes(K, 'weight').values()))
plt.show()
plt.savefig("filename3.png")


#declaration of problem and heuristic
#problem = #intial state, goal state, actions
#heuristic = #calculation of the heuristic function
#plan = search(problem,heuristic)
#plan = {........}
