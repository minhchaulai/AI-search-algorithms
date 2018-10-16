from collections import deque
import heapq
from operator import itemgetter
from collections import deque
from collections import OrderedDict
map_distances = dict(
    chi=OrderedDict([("det", 283), ("cle", 345), ("ind", 182)]),
    cle=OrderedDict([("chi", 345), ("det", 169), ("col", 144), ("pit", 134), ("buf", 189)]),
    ind=OrderedDict([("chi", 182), ("col", 176)]),
    col=OrderedDict([("ind", 176), ("cle", 144), ("pit", 185)]),
    det=OrderedDict([("chi", 283), ("cle", 169), ("buf", 256)]),
    buf=OrderedDict([("det", 256), ("cle", 189), ("pit", 215), ("syr", 150)]),
    pit=OrderedDict([("col", 185), ("cle", 134), ("buf", 215), ("phi", 305), ("bal", 247)]),
    syr=OrderedDict([("buf", 150), ("phi", 253), ("new", 254), ("bos", 312)]),
    bal=OrderedDict([("phi", 101), ("pit", 247)]),
    phi=OrderedDict([("pit", 305), ("bal", 101), ("syr", 253), ("new", 97)]),
    new=OrderedDict([("syr", 254), ("phi", 97), ("bos", 215), ("pro", 181)]),
    pro=OrderedDict([("bos", 50), ("new", 181)]),
    bos=OrderedDict([("pro", 50), ("new", 215), ("syr", 312), ("por", 107)]),
    por=OrderedDict([("bos", 107)]))

map_times = dict(
    chi=OrderedDict([("det", 280), ("cle", 345), ("ind", 200)]),
    cle=OrderedDict([("chi", 345), ("det", 170), ("col", 155), ("pit", 145), ("buf", 185)]),
    ind=OrderedDict([("chi", 200), ("col", 175)]),
    col=OrderedDict([("ind", 175), ("cle", 155), ("pit", 185)]),
    det=OrderedDict([("chi", 280), ("cle", 170), ("buf", 270)]),
    buf=OrderedDict([("det", 270), ("cle", 185), ("pit", 215), ("syr", 145)]),
    pit=OrderedDict([("col", 185), ("cle", 145), ("buf", 215), ("phi", 305), ("bal", 255)]),
    syr=OrderedDict([("buf", 145), ("phi", 245), ("new", 260), ("bos", 290)]),
    bal=OrderedDict([("phi", 145), ("pit", 255)]),
    phi=OrderedDict([("pit", 305), ("bal", 145), ("syr", 245), ("new", 150)]),
    new=OrderedDict([("syr", 260), ("phi", 150), ("bos", 270), ("pro", 260)]),
    pro=OrderedDict([("bos", 90), ("new", 260)]),
    bos=OrderedDict([("pro", 90), ("new", 270), ("syr", 290), ("por", 120)]),
    por=OrderedDict([("bos", 120)]))

sld_providence = dict(
    chi=833,
    cle=531,
    ind=782,
    col=618,
    det=596,
    buf=385,
    pit=458,
    syr=253,
    bal=325,
    phi=236,
    new=157,
    pro=0,
    bos=38,
    por=136)

def path(previous, s):
    '''
    `previous` is a dictionary chaining together the predecessor state that led to each state
    `s` will be None for the initial state
    otherwise, start from the last state `s` and recursively trace `previous` back to the initial state,
    constructing a list of states visited as we go
    '''
    if s is None:
        return []
    else:
        return path(previous, previous[s])+[s]

def pathcost(path, step_costs):
    '''
    add up the step costs along a path, which is assumed to be a list output from the `path` function above
    '''
    cost = 0
    for s in range(len(path)-1):
        cost += step_costs[path[s]][path[s+1]]
    return cost

# Solution:

class Frontier_PQ2:
    ''' frontier class for uniform search, ordered by path cost '''
    def __init__(self, start, cost):
        self.states = (0, start)
        self.q = [(0, start, [start])]

    def add(self, cost, state, path):
        heapq.heappush(self.q, (cost, state, path))

    def pop(self):
        return heapq.heappop(self.q)

    def replace(self, state, cost):
        self.states[state] = cost

# Solution:


def uniform_cost(start, goal, state_graph, return_cost=False, return_nexp = True):
    visited = []
    frontier = Frontier_PQ2(start, 0)
    while goal not in visited:
        cost, current, path = frontier.q[0]
        vertex = frontier.pop()
        if current not in visited:
            visited.append(current)
            list2 = list(state_graph[current].items())
            for city in list2:
                cit, dist = city
                if cit not in visited:
                    total_cost = cost + dist
                    frontier.add(total_cost, cit, path + [cit])
    r1, r2, r3 = vertex
    if return_cost and return_nexp:
        return (r3, r1, len(visited))
    elif return_cost:
        return (r3, r1)
    elif return_nexp:
        return (r3, len(visited))
    else:
        return r3


# add your code here
# path, cost = uniform_cost('chi','pit',map_distances,True)
# print(path)
# print(cost)
