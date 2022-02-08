from algorithm import *


class State():
    def __init__(self):
        self.pos = {}
        self.carrying = None


# Operators
def goto(state, p):
    state.pos['r'] = p
    return state


def pickup(state,i):
    state.carrying = i
    return state


def drop(state):
    state.carrying = None
    return state


# Methods
def move_robot(state,l1,l2):
    if(state.pos['r'] == l1):
        return [('goto', l2)]
    else:
        return False


def pickup_item(state,loc,i):
    if(state.carrying == None and state.pos['r'] == loc):
        return [('pickup'), i]
    else:
        return False


def drop_item(state,loc,i):
    if(state.carrying == i and state.pos['r'] == loc):
        return [('drop'), i]
    else:
        return False


def take_picture(state,loc,c):
    if(state.pos['r'] == loc):
        return [('capture'), c]
    else:
        return False


def formulate_problem(initial_st, goal_st):
    if(initial_st == goal_st):
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
    print(plan)
    state1 = State()
    state1.pos = {'r': plan[0].state}
    # print(T.nodes[plan[0].state]) # print coordinates instead of node name.
    list = []  # for appending command.
    for i in range(1, len(plan)):
        command = move_robot(state1, plan[i - 1].state, plan[i].state)
        list.append(command)
        state1.pos = {'r': plan[i].state}
    return list


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



# i= index, T.nodes coordinate on each node
pos = {i:T.nodes[i] for i in range(len(T.nodes))}

# drawing in random layout
nx.draw(K, pos= pos, with_labels=True)
plt.savefig("filename3.png")



#declaration of problem and heuristic
#problem = #intial state, goal state, actions
#heuristic = #calculation of the heuristic function
#plan = search(problem,heuristic)
#plan = {........}
