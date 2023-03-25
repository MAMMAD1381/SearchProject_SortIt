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
    def ids(prb: Problem) -> Solution:  # this method get a first state of Problem and do ids for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            Search.add_hash(state)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                if not Search.add_hash(c):
                    continue
                queue.insert(0, c)
        return None

    @staticmethod
    def dfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do dfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in Search.states_hash.keys():
                    queue.append(c)
                    Search.add_hash(c)
        return None

    @staticmethod
    def dls(prb: Problem) -> Solution:  # this method get a first state of Problem and do dls for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        Search.Gn[state.__hash__()] = 0
        limited_depth = 199
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            if prb.is_goal(state):
                # printing all states cost to final state and the cost of final state and returning it
                print(Search.Gn, state.__hash__(), Search.Gn[state.__hash__()])
                return Solution(state, prb, start_time)
            neighbors = prb.successor(state)
            for c in neighbors:
                Search.gn(state, c, 1)

                if c.__hash__() not in Search.states_hash.keys() and Search.Gn[c.__hash__()] <= limited_depth:
                    queue.append(c)
                    Search.add_hash(c)

        return None

    # todo adding hash to dfs and dls

    @staticmethod
    def gn(parent, child, child_cost):
        Gn = Search.Gn
        Gn[child.__hash__()] = Gn[parent.__hash__()] + child_cost
        Search.Gn = Gn

    @staticmethod
    def minimum_in_dict(dictionary):  # returns the minimum key of minimum value in dictionary
        min_value = min(dictionary.values())
        for i in dictionary:
            if dictionary[i] == min_value:
                return i
            else:
                return False

    @staticmethod
    def add_hash(state):  # adds a state to a dict base on hash as key & object as value
        states_hash = Search.states_hash
        if state.__hash__() in states_hash.keys():
            return False
        states_hash[state.__hash__()] = state
        Search.states_hash = states_hash
        return True

    @staticmethod
    def sort_neighbors(neighbors):  # sorts the neighbors based on their gn and returns objects of states
        gn_neighbors = {}
        for s in neighbors:
            gn_neighbors[s.__hash__()] = Search.Gn[s.__hash__()]
        neighbors = []
        while len(gn_neighbors.values()) > 0:
            min_value = min(gn_neighbors.values())
            for s in gn_neighbors:
                if gn_neighbors[s] == min_value:
                    neighbors.append(Search.states_hash[s])
                    del gn_neighbors[s]
                    break
        return neighbors

    @staticmethod
    def has_exists(state):
        states_hash = Search.states_hash
