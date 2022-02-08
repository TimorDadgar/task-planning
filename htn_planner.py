from algorithm import *

class State():
    def __init__(self):
        self.pos = {}
        self.carrying = None

#Operators
def goto(state, p):
    state.pos['r'] = p
    return state

def pickup(state,i):
    state.carrying = i
    return state

def drop(state):
    state.carrying = None
    return state

#Methods
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

def search(problem, heuristic):
    plan = best_first_graph_search(problem, heuristic)
    return plan







#declaration of problem and heuristic
#problem = #intial state, goal state, actions
#heuristic = #calculation of the heuristic function
#plan = search(problem,heuristic)
#plan = {........}
