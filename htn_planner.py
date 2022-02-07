from algorithm import *

class State():
    def __init__(self, name):
        self.__name__ = name
        self.pos = {}
        self.carrying = None

#Operators
class goto(state, p):
    state.pos['r'] = p
    return state

class pickup(state,i):
    state.carrying = i
    return state

class drop(state):
    state.carrying = None
    return state

#Methods
class move_robot(state,l1,l2):
    if(state.pos['r'] == l1):
        return [('goto', l2)]
    else:
        return False

class pickup_item(state,loc,i):
    if(state.carrying == None and state.pos['r'] == loc):
        return [('pickup'), i]
    else:
        return False

class drop_item(state,loc,i):
    if(state.carrying == i and state.pos['r'] == loc):
        return [('drop'), i]
    else:
        return False

class take_picture(state,loc,c):
    if(state.pos['r'] == loc):
        return [('capture'), c]
    else:
        return False

class search(problem, heuristic):
    plan = best_first_graph_search(problem, heuristic)
    return plan







#declaration of problem and heuristic
problem = #intial state, goal state, actions
heuristic = #calculation of the heuristic function
plan = search(problem,heuristic)