from algorithm import *


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
def move_robot(state, l1, l2):
    if l1 == l2:
        return []
    if state.pos['r'] != l1:
        return False
    problem = Problem(l1, l2)
    heuristic = (lambda n: n.path_cost + sqrt(
        (T.nodes[n.state][0] - T.nodes[l2][0]) ** 2 + (T.nodes[n.state][1] - T.nodes[l2][1]) ** 2))
    path = best_first_graph_search(problem, heuristic)
    if path is None:
        return None
    path = path.path()
    # print(T.nodes[plan[0].state]) # print coordinates instead of node name.
    plan = []  # for appending command.
    for i in range(1, len(path)):
        plan.append(('goto', path[i].state))
        goto(state, path[i].state)
    return plan


def pickup_item(state, loc, i):
    s = []
    if state.pos['r'] != loc:
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
    else:
        p = pickup_item(state, state.pos['s'+str(i)], i)
        p.extend(drop_item(state, loc, i))
        return p


def take_picture(state, loc, c):
    if state.pos['r'] == loc:
        return [('capture', c)]
    else:
        return False


def formulate_problem(initial_st, goal_st):
    if initial_st == goal_st:
        return False
    else:
        p = Problem(initial_st, goal_st)
        return p


def define_heuristic(goal_state):
    heuristic = (lambda n: n.path_cost + sqrt((T.nodes[n.state][0] - T.nodes[goal_state][0]) ** 2 + (T.nodes[n.state][1] - T.nodes[goal_state][1]) ** 2))
    return heuristic


def search(problem, heuristic):
    plan = best_first_graph_search(problem, heuristic)
    return plan


# converts graph path to strips.
def convert(plan):
    state1.pos = {'r': plan[0].state}
    print(plan)
    # print(T.nodes[plan[0].state]) # print coordinates instead of node name.
    li = []  # for appending command.
    for i in range(1, len(plan)):
        command = move_robot(state1, plan[i - 1].state, plan[i].state)
        li.append(command)
        goto(state1, plan[i].state)
    return li


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

'''
state1 = State()

initial_state = randint(0, 19)
goal_state = randint(0, 19)
f_p = formulate_problem(initial_state, goal_state)
if(f_p == False):
    print("Can,t create a problem!")
    exit(1)
else:
    print(f_p)


# pops the strait node between initial node and goal node.
G[initial_state].pop(goal_state)

d_h = define_heuristic(goal_state)
print(d_h)

plan = search(f_p, d_h)
print(plan)

l = convert(plan.path())
print(l)

print("nodes with sensors: ", T.sensors)

test_of_applying_sensors(l)
print(l)
'''


def distn(i, j):
    N = T.nodes
    return sqrt((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2)

import copy

def dotodo(state, todo):
    pos = copy.copy(state.pos)
    plans = []
    for t in todo:
        p = t(state)
        plans.append(p)
        state.pos = copy.copy(pos)
    plan = []
    while len(plans):
        mind = float(inf)
        mini = 0
        for i in range(len(plans)):
            p = plans[i]
            d = 0
            j = 0
            olp = state.pos['r']
            while j < len(p) and p[j][0] == 'goto':
                d += distn(olp, p[j][1])
                olp = p[j][1]
                j += 1
            if d < mind:
                mind = d
                mini = i

        print(plans)
        plan.append(plans[mini].pop(0))
        while plan[-1][0] == 'goto':
            K.add_edge(state.pos['r'], plan[-1][1], color='black', weight=3)
            state.pos['r'] = plan[-1][1]
            plan.append(plans[mini].pop(0))
        if plan[-1][0] == 'drop':
            state.pos['s' + str(plan[-1][1])] = state.pos['r']
        if len(plans[mini]) == 0:
            plans.pop(mini)
        else:
            while plans[mini][0][0] != 'goto':
                plan.append(plans[mini].pop(0))
                if plan[-1][0] == 'drop':
                    state.pos['s'+str(plan[-1][1])] = state.pos['r']
                if len(plans[mini]) == 0:
                    plans.pop(mini)
                    break
        print(plans)
        for i in range(len(plans)):
            pos = state.pos['r']
            while plans[i][0][0] == 'goto':
                op = plans[i].pop(0)
                pos = op[1]
            olp = state.pos['r']
            mov = move_robot(state, state.pos['r'], pos)
            mov.reverse()
            for m in mov:
                plans[i].insert(0, m)
            state.pos['r'] = olp
        print(plans)
    return plan


state1 = State()

state1.pos['r'] = startp = randint(0, 19)

for i in range(len(T.sensors)):
    state1.pos['s' + str(i)] = T.sensors[i]
print(state1.pos)
goal1 = randint(0, 19)
goal2 = randint(0, 19)
goal3 = randint(0, 19)
goal4 = randint(0, 19)
todo = [lambda state: drop_item(state, goal1, 0), lambda state: drop_item(state, goal2, 1),
        lambda state: drop_item(state, goal3, 2), lambda state: drop_item(state, goal4, 3)]


for i in range(len(T.nodes)):
    K.add_edge(i, i)

# i= index, T.nodes coordinate on each node
pos = {i: T.nodes[i] for i in range(len(T.nodes))}

col = ['green' if node in T.sensors else 'yellow' for node in K]
col[startp] = 'cyan'
plan = dotodo(state1, todo)
print(plan)


for k in state1.pos.keys():
    if k[0] == 's':
        col[state1.pos[k]] = 'violet'

col[plan[-2][1]] = 'red'

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
