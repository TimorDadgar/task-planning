import select
import traceback

from algorithm import *
import copy

shadDrainRate = 0.3
sunChargeRate = 0


class State:
    def __init__(self):
        self.pos = {}
        self.carrying = set()
        self.battery = 30


class Goal:
    def __init__(self):
        self.goal = ()
        self.goto_objectives = []
        self.sensors_to_be_dropped = []
        self.sensors_to_be_picked_up = []


class Plan:
    def __init__(self):
        self.plan = None
        self.current_objective = None
        self.current_plan_list_pos = 0


state1 = State()
goals = Goal()
final_plan = Plan()


def restore_state(onto, refer):
    onto.pos = copy.copy(refer.pos)
    onto.carrying = copy.copy(refer.carrying)
    onto.battery = refer.battery


def path_length(l1, l2):
    problem = Problem(l1, l2)  # the path is a sub-problem handled in algorithm.py
    heuristic = (lambda n: n.path_cost + sqrt(
        (T.nodes[n.state][0] - T.nodes[l2][0]) ** 2 + (T.nodes[n.state][1] - T.nodes[l2][1]) ** 2))
    # distance from explored node to goal
    path = best_first_graph_search(problem, heuristic, False)
    if path is None:  # impossible to get there
        return None
    path = path.path()  # the path leading up to final node
    length = 0
    for i in range(1, len(path)):
        length += distn(path[i - 1].state, path[i].state)
    return length


def find_sun(pos):
    outdist = float('inf')
    batteryOut = float('inf')
    sunnode = None
    if pos in T.inshadow:
        for N in range(len(T.nodes)):
            if N not in T.inshadow:
                pl = path_length(pos, N)
                if pl is not None and pl < outdist:
                    sunnode = N
                    outdist = pl
        batteryOut = outdist * shadDrainRate
    else:
        batteryOut = 0
    return batteryOut, sunnode


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
    path = best_first_graph_search(problem, heuristic, False)
    if path is None:  # impossible to get there
        raise Exception("Cannot reach node " + str(l2) + " from " + str(l1))
    path = path.path()  # the path leading up to final node
    plan = []  # for appending command.
    olb = state.battery  # olb = old battery
    ols = copy.deepcopy(state)  # ols = old state
    for i in range(1, len(path)):
        plan.append(('goto', path[i].state))
        goto(state, path[i].state)
        if path[i].state in T.inshadow or path[i - 1].state in T.inshadow:
            state.battery -= distn(path[i - 1].state, path[i].state)*shadDrainRate
        else:
            state.battery = min(state.battery + distn(path[i - 1].state, path[i].state) * sunChargeRate, 100)
    # make sure to never let it be impossible to get out of shadow

    su = find_sun(state.pos['r'])
    batteryOut = su[0]
    sunnode = su[1]
    print(state.battery, batteryOut)
    print(path)
    if state.battery < batteryOut:
        if l1 in T.inshadow:
            restore_state(state, ols)
            su = find_sun(l1)
            print(state.battery, su)
            if state.battery < su[0]:
                raise Exception("Impossible to get out of shadow at " + str(l1) + " - insufficient battery, need " + str(su[0]) + " has " + str(state.battery))
            print(state.battery)
            plan = move_robot(state, l1, su[1])
            if abs(state.battery - (ols.battery - su[0])) > 0.001:
                raise Exception("Cost out of " + str(l1) + " was miscalculated: " + str(state.battery) + " vs " + str(ols.battery - su[0]))
            plan.extend(move_robot(state, su[1], l2))
        elif olb - state.battery + batteryOut <= 100:  # is it possible to before charge enough to get in and out?
            plan.insert(0, ('charge', olb - state.battery + batteryOut+1))
            # print("charge to", str(olb - state.battery + batteryOut))
            state.battery = batteryOut + 1
            # print("end up with", str(batteryOut))
        else:
            if batteryOut < 50:  # if the shortest distance from goal to sun is short enough
                restore_state(state, ols)
                plan = move_robot(state, l1, sunnode)
                plan.append(('charge', batteryOut * 2+1))
                state.battery = batteryOut * 2+1
                plan.extend(move_robot(state, sunnode, l2))
            else:
                raise Exception("Going to  " + str(l2) + " from " + str(l1) + " would risk running out of battery")

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
        p = pickup_item(state, state.pos['s' + str(i)], i)  # get it
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
    loc = l[len(l) - 1][0][1]
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


# execute the set of tasks to do
def dotodo(state, todo):
    ols = copy.deepcopy(state)  # for restoring state
    # plan each subtask separately at first, as if each done from initial condition
    plans = []
    for t in todo:
        p = t(state)
        plans.append(p)
        state = copy.deepcopy(ols)
    plan = []
    print(plans)
    # for as long as there are tasks to add to the ultimate single plan
    while len(plans):
        mind = float(inf)  # minimal distance
        mini = 0  # index of minimal distance
        for i in range(len(plans)):  # for each sub-plan
            p = plans[i]
            d = 0  # distance of current plan
            j = 0  # instruction index
            if p[j][0] == 'charge':
                j += 1
            olp = state.pos['r']  # to estimate distance
            while j < len(p) and p[j][0] == 'goto':  # for as long as movement is required
                d += distn(olp, p[j][1])
                olp = p[j][1]
                j += 1
            if d < mind:
                mind = d
                mini = i

        plan.append(plans[mini].pop(0))  # add the instruction(s) that require the least distance to get something done
        if plan[-1][0] == 'charge':
            state.battery = plan[-1][1]
            plan.append(plans[mini].pop(0))
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
            while plans[mini][0][0] != 'goto' and plans[mini][0][0] != 'charge':
                plan.append(plans[mini].pop(0))
                if plan[-1][0] == 'drop':
                    state.pos['s' + str(plan[-1][1])] = state.pos['r']
                if len(plans[mini]) == 0:
                    plans.pop(mini)
                    break
        # after moving to a new location, new paths are needed to each other location
        for i in range(len(plans)):
            ols = copy.deepcopy(state)
            pos = state.pos['r']  # eventually the destination
            if plans[i][0][0] == 'charge':
                state.battery = plans[i][0][1]
                plans[i].pop(0)
            while plans[i][0][0] == 'goto':
                op = plans[i].pop(0)
                pos = op[1]
            mov = move_robot(state, state.pos['r'], pos)
            mov.reverse()  # inserting each movement at index zero, reversing this order makes it easy
            for m in mov:
                plans[i].insert(0, m)
            state = ols
            print(plans)
    return plan


def generate_test_plan():
    state1.pos['r'] = startp = randint(0, len(T.sensors) - 1)

    for i in range(len(T.sensors)):
        state1.pos['s' + str(i)] = T.sensors[i]
    print(state1.pos)
    # each sensor's position to be dropped
    goal1, goal2, goal3, goal4 = -1, -1, -1, -1
    while goal1 not in T.G:
        goal1 = randint(0, len(T.sensors) - 1)
    while goal2 not in T.G:
        goal2 = randint(0, len(T.sensors) - 1)
    while goal3 not in T.G:
        goal3 = randint(0, len(T.sensors) - 1)
    while goal4 not in T.G:
        goal4 = randint(0, len(T.sensors) - 1)
    todo = [lambda state: drop_item(state, goal1, 0), lambda state: drop_item(state, goal2, 1),
            lambda state: drop_item(state, goal3, 2), lambda state: drop_item(state, goal4, 3)]

    # the position in graph to draw nodes
    # i= index, T.nodes coordinate on each node
    pos = {i: T.nodes[i] for i in range(len(T.nodes))}

    try:
        final_plan.plan = dotodo(state1, todo)
        print(final_plan.plan)
    except BaseException as e:
        print(traceback.format_exc())
        print("Error:", e)
        final_plan.plan = None

    # if the nodes not part of the plan are to be drawn
    drawall = True
    if drawall:
        for i in range(len(T.nodes)):
            if i in T.G:
                K.add_edge(i, i)

    col = ['lime' if node in T.sensors else 'yellow' for node in K]  # green for pickup place, yellow for nothing special
    colind = dict()  # color index. This gets a little complicated when not all nodes are drawn
    for i in range(len(T.nodes)):
        j = 0
        for node in K:
            if node == i:
                colind[i] = j
            j += 1

    col[colind[startp]] = 'cyan'  # start position color

    for k in state1.pos.keys():
        if k[0] == 's' and state1.pos[k] in T.G:
            col[colind[state1.pos[k]]] = 'violet'  # drop position color

    if final_plan.plan is not None:
        col[colind[final_plan.plan[-2][1]]] = 'red'  # end position color
    from matplotlib import colors

    for k in T.inshadow:
        if k in colind:
            if colors.is_color_like("dark" + col[colind[k]]):
                col[colind[k]] = "dark" + col[colind[k]]
            else:
                if col[colind[k]] == "lime":
                    col[colind[k]] = "darkgreen"
                else:
                    col[colind[k]] = "darkgoldenrod"
            '''
            c = colors.to_rgb(col[colind[k]])
            c2 = colors.to_rgb('gray')
            c = (c[0]/2 + c2[0]/2,
                 c[1] / 2 + c2[1] / 2,
                 c[2] / 2 + c2[2] / 2)
            col[colind[k]] = c
            '''

    # drawing in random layout
    if final_plan.plan is not None:
        nx.draw(K, pos=pos, with_labels=True, node_color=col, edge_color=nx.get_edge_attributes(K, 'color').values(),
                width=list(nx.get_edge_attributes(K, 'weight').values()))
    else:
        nx.draw(K, pos=pos, with_labels=True, node_color=col)
    plt.show()
    plt.savefig("filename3.png")


def generate_plan():
    # implement how to create plan from mqtt
    for i in range(len(T.sensors)):
        state1.pos['s' + str(i)] = T.sensors[i]
    print(state1.pos)

    # ????


def set_info_from_simulation(data):
    # insert intitial state of robot
    # insert sensors???
    # insert battery info
    # insert shadow vector
    state1.pos['r'] = (data['position']['x'], data['position']['y'])
    print(state1.pos)


def set_info_from_perception(data):
    # insert obstacle map
    T.obstacle_map = data


def set_info_from_mission_control(data):
    # insert goal state
    # insert goto objectives
    # insert sensors (drop/pickup)
    for i in data:
        print(data[i])
        if data[i][0]['command'] == 'goal-state':
            print("adding goal state....")
            goals.goal = (data[i][0]['x'], data[i][0]['y'])
            print(goals.goal)
        elif data[i][0]['command'] == 'goto':
            print("adding goto objectives....")
            goals.goto_objectives = (data[i][0]['x'], data[i][0]['y'])
            print(goals.goto_objectives)
        elif data[i][0]['command'] == 'sensor-drop':
            print("adding sensors to be dropped....")
            goals.sensors_to_be_dropped.append({data[i][0]['id']: (data[i][0]['x'], data[i][0]['y'])})
            print(goals.sensors_to_be_dropped)
        elif data[i][0]['command'] == 'sensor-pickup':
            print("adding sensors to be picked up....")
            goals.sensors_to_be_picked_up.append({data[i][0]['id']: (data[i][0]['x'], data[i][0]['y'])})
            print(goals.sensors_to_be_picked_up)
        else:
            print("we cant handle this command at the moment")


# if mock_data is True we send mock data to motion planning
# if mock_data is False we send real data to motion planning
def send_final_plan_1_by_1(mock_data):
    if mock_data is True:
        plan_out = {"id": 0, "command": "goto", "x": 40, "y": 25}   # create message format
        data_out = json.dumps(plan_out)     # create json message
        return data_out
    else:
        current_plan_id = final_plan.current_plan_list_pos  # get plan's current id (pos in plan list)
        print("current plan id in list:", current_plan_id)
        if final_plan.current_plan_list_pos < len(final_plan.plan):
            command = final_plan.plan[current_plan_id][0]   # get command to execute
            arg = T.nodes[final_plan.plan[current_plan_id][1]]  # get coordinates from node n
            plan_out = {"id": current_plan_id, "command": command, "x": arg[0], "y": arg[1]}     # create message format
            data_out = json.dumps(plan_out)     # create json message
            print(data_out)
            return data_out
        else:
            print("plan is done, which means the plan should have succeeded")


#generate_test_top_map()
#generate_test_plan()
# declaration of problem and heuristic
# problem = #intial state, goal state, actions
# heuristic = #calculation of the heuristic function
# plan = search(problem,heuristic)
# plan = {........}
