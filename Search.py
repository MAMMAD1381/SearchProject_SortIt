import State
from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    Gn = {}
    states_hash = {}

    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None

    @staticmethod
    def ucs(prb: Problem) -> Solution:  # this method get a first state of Problem and do ucs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for i in neighbors:
                Search.gn(i)
                Search.add_hash(i)
            Search.sort_neighbors(neighbors)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None

    @staticmethod
    def gn(state):
        Gn = Search.Gn
        if state.__hash__() in Gn:
            Gn[state.__hash__()] += 1
        else:
            Gn[state.__hash__()] = 1
        Search.Gn = Gn
        return Gn[state.__hash__()]

    @staticmethod
    def minimum_in_dict(dict):
        min_value = min(dict.values())
        for i in dict:
            if dict[i] == min_value:
                return i
            else:
                return False

    @staticmethod
    def add_hash(state):
        states_hash = Search.states_hash
        states_hash[state.__hash__()] = state
        Search.states_hash = states_hash

    @staticmethod
    def sort_neighbors(neighbors):
        gn_neighbors = {}
        print(f'neighbors: {neighbors}')
        for s in neighbors:
            gn_neighbors[s.__hash__()] = Search.Gn[s.__hash__()]
        neighbors = []
        while len(gn_neighbors.values()) > 0:
            print(gn_neighbors, neighbors)
            min_value = min(gn_neighbors.values())
            for s in gn_neighbors:
                if gn_neighbors[s] == min_value:
                    neighbors.append(Search.states_hash[s])
                    del gn_neighbors[s]
                    break

        print(gn_neighbors, neighbors)
        return neighbors
