from collections import OrderedDict

canada = OrderedDict(
    [("AB", ["BC", "NT", "SK"]),
    ("BC", ["AB", "NT", "YT"]),
    ("LB", ["NF", "NS", "PE", "QC"]),
    ("MB", ["ON", "NV", "SK"]),
    ("NB", ["NS", "QC"]),
    ("NF", ["LB", "QC"]),
    ("NS", ["LB", "NB", "PE"]),
    ("NT", ["AB", "BC", "NV", "SK", "YT"]),
    ("NV", ["MB", "NT"]),
    ("ON", ["MB", "QC"]),
    ("PE", ["LB", "NS", "QC"]),
    ("QC", ["LB", "NB", "NF", "ON", "PE"]),
    ("SK", ["AB", "MB", "NT"]),
    ("YT", ["BC", "NT"])])

states = ["AB", "BC", "LB", "MB", "NB", "NF", "NS", "NT", "NV", "ON", "PE", "QC", "SK", "YT"]
colors = ["blue", "green", "red"]


class CSP:
    def __init__(self, states, neighbors, colors):
        self.states = states
        self.neighbors = neighbors
        self.colors = colors
        self.current = 0
        self.backs = 0
        self.previous = ""


nbacks = 0


def backtracking_search(csp, lcv, mcv):
    return recursive_backtracking_mcv(OrderedDict(), csp)
    #else:
    #    return recursive_backtracking(OrderedDict(), csp)


def recursive_backtracking(assignment, csp):
    if len(assignment) == len(csp.states):
        if constraint(assignment, canada):
            return (assignment, csp.backs)
        else:
            return {}
    state = csp.states[csp.current]
    for color in csp.colors:
        if valid(assignment, state, color):
            assignment[state] = color
            csp.current += 1
            result = recursive_backtracking(assignment, csp)
            if result != {}:
                return result
            csp.current -= 1
            assignment.popitem()
    csp.backs += 1
    return {}


def selectvariable(assignment, csp):
    all = []
    for state in csp.states:
        potential = 3
        used = []
        if state not in assignment:
            for neighbor in csp.neighbors[state]:
                if neighbor in assignment:
                    if assignment[neighbor] not in used:
                        used.append(assignment[neighbor])
            if (state, potential) not in all:
                all.append((state, potential - len(used)))
    currentMin = 100
    save = ""
    for pair in all:
        val1, val2 = pair
        if val2 < currentMin:
            currentMin = val2
            save = val1

    return save



def recursive_backtracking_mcv(assignment, csp):
    if len(assignment) == len(csp.states):
        if constraint(assignment, canada):
            return (assignment, csp.backs)
        else:
            return {}
    if csp.current == 0:
        state = csp.states[csp.current]
        csp.current += 1
    else:
        state = selectvariable(assignment, csp)
    for color in csp.colors:
        if valid(assignment, state, color):
            assignment[state] = color
            result = recursive_backtracking_mcv(assignment, csp)
            if result != {}:
                return result
            assignment.popitem()
    csp.backs += 1
    return {}


def constraint(assignment, neighbors):
    for state in assignment:
        for neighbor in neighbors[state]:
            if neighbor not in assignment:
                continue
            if assignment[state] == assignment[neighbor]:
                return False
    return True


def valid(assignment, state, color):
        assignment[state] = color
        return constraint(assignment, canada)

# cs = CSP(states, canada, colors)
# a = backtracking_search(cs, lcv)
# print(a)
