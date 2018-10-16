from collections import deque
import heapq
from scipy import stats
import numpy as np

map_distances = dict(
    chi=dict(det=283, cle=345, ind=182),
    cle=dict(chi=345, det=169, col=144, pit=134, buf=189),
    ind=dict(chi=182, col=176),
    col=dict(ind=176, cle=144, pit=185),
    det=dict(chi=283, cle=169, buf=256),
    buf=dict(det=256, cle=189, pit=215, syr=150),
    pit=dict(col=185, cle=134, buf=215, phi=305, bal=247),
    syr=dict(buf=150, phi=253, new=254, bos=312),
    bal=dict(phi=101, pit=247),
    phi=dict(pit=305, bal=101, syr=253, new=97),
    new=dict(syr=254, phi=97, bos=215, pro=181),
    pro=dict(bos=50, new=181),
    bos=dict(pro=50, new=215, syr=312, por=107),
    por=dict(bos=107))


map_times = dict(
    chi=dict(det=280, cle=345, ind=200),
    cle=dict(chi=345, det=170, col=155, pit=145, buf=185),
    ind=dict(chi=200, col=175),
    col=dict(ind=175, cle=155, pit=185),
    det=dict(chi=280, cle=170, buf=270),
    buf=dict(det=270, cle=185, pit=215, syr=145),
    pit=dict(col=185, cle=145, buf=215, phi=305, bal=255),
    syr=dict(buf=145, phi=245, new=260, bos=290),
    bal=dict(phi=145, pit=255),
    phi=dict(pit=305, bal=145, syr=245, new=150),
    new=dict(syr=260, phi=150, bos=270, pro=260),
    pro=dict(bos=90, new=260),
    bos=dict(pro=90, new=270, syr=290, por=120),
    por=dict(bos=120))

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

class Frontier_PQ:
    ''' frontier class for uniform search, ordered by path cost '''
    # add your code here
    def __init__(self, start, cost):
        self.states = (0, start)
        self.q = [(0, start, [start])]

    def add(self, cost, state, path):
        heapq.heappush(self.q, (cost, state, path))

    def pop(self):
        return heapq.heappop(self.q)

    def replace(self, state, cost):
        self.states[state] = cost
    # add your code here

# Solution:

def uniform_cost(start, goal, state_graph, return_cost=False):
    # add your code here
    visited = []
    frontier = Frontier_PQ(start, 0)
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
    if return_cost:
        return (r3, r1)
    else:
        return r3
# add your code here

# first, grab the time-optimal route from New York to Chicago, using the uniform cost search
start = 'chi'
goal = 'new'
graph = map_times
route, time = uniform_cost(start, goal, graph, True)


sigma = np.log(1.1)


# set parameters
# m = map_times[route[i]][route[i+1]]
sigma = np.log(1.1)
save = np.zeros(10000)
for i in range(len(route)-1):
    map_times[route[i]]
    mu = np.log(map_times[route[i]][route[i+1]])
    s = np.random.lognormal(mu, sigma, 10000)
    save = np.add(save, s)
path_costs = save

# print('probability that Neal making it to Chicago in time for that turkey: {:0.1f}'.format(np.sum(path_costs <= 940)/len(path_costs)))
