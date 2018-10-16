import numpy as np
import heapq
import unittest

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

# Solution:


def heuristic_sld_providence(state):
    return sld_providence[state]


class Frontier_PQ:
    ''' frontier class for uniform search, ordered by path cost '''
    def __init__(self, start, cost, heuristic):
        self.states = (0, start)
        self.q = [(0, start, [start], 0)]

    def add(self, cost, state, path, sub_cost):
        heapq.heappush(self.q, (cost, state, path, sub_cost))

    def pop(self):
        return heapq.heappop(self.q)

    def replace(self, state, cost):
        self.states[state] = cost
# Solution:


def astar_search(start, goal, state_graph, heuristic, return_cost=False, return_nexp=False):
    '''A* search from `start` to `goal`
    start = initial state
    goal = goal state
    heuristic = function for estimated cost to goal (function name)
    return_cost = logical (True/False) for whether or not to return the total path cost
    return_nexp = logical (True/False) for whether or not to return the number of nodes expanded
    '''
    visited = []
    frontier = Frontier_PQ(start, 0, heuristic(start))
    while goal not in visited:
        cost, current, path, cost2 = frontier.q[0]
        vertex = frontier.pop()
        if current not in visited:
            visited.append(current)
            list2 = list(state_graph[current].items())
            for city in list2:
                cit, dist = city
                if cit not in visited:
                    sub_cost = cost2 + dist
                    total_cost = dist + heuristic(cit)
                    frontier.add(total_cost, cit, path + [cit], sub_cost)
    r1, r2, r3, r4 = vertex
    if return_cost and return_nexp:
        return (r3, r4, len(visited) + 1)
    elif return_cost:
        return (r3, r4)
    elif return_nexp:
        return (r3, len(visited) + 1)
    else:
        return r3
