import State
from Heuristic import Heuristic
from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    Gn = {}
    states_hash = {}
    Fn = {}
    ids_limit = 1

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
        Search.Gn[state.__hash__()] = 0
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for i in neighbors:
                Search.gn(state, i, 1)
                Search.add_hash(i)
            neighbors = Search.sort_neighbors(neighbors)

            for c in neighbors:
                print(c.__hash__(), Search.Gn[c.__hash__()])
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
        Search.Gn[state.__hash__()] = 0
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            neighbors = prb.successor(state)
            for c in neighbors:
                Search.gn(state, c, 1)
                print(Search.Gn[c.__hash__()], Search.ids_limit)
                if c.__hash__() not in Search.states_hash.keys() and Search.Gn[c.__hash__()] <= Search.ids_limit:
                    queue.append(c)
                    Search.add_hash(c)
        Search.ids_limit += 1
        Search.Gn = {}
        Search.states_hash = {}
        return Search.ids(prb)

    @staticmethod
    def dfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do dfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            # print(prb.heuristic(state))
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in Search.states_hash.keys():
                    print(prb.heuristic(c))
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

    @staticmethod
    def astar(prb: Problem) -> Solution:  # this method get a first state of Problem and do astar for find solution if
        # no solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        Search.Gn[state.__hash__()] = 0
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for i in neighbors:
                Search.gn(state, i, 1)
                Search.fn(i)
                Search.add_hash(i)
            neighbors = Search.sort_neighbors_fn(neighbors)

            for c in neighbors:
                print(c.__hash__(), Search.Fn[c.__hash__()])
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
                queue = Search.sort_neighbors_fn(queue)
        return None

    @staticmethod
    def ida(prb: Problem) -> Solution:  # this method get a first state of Problem and do ida for find solution if
        # no solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        unexpanded = {}
        visited_hash = {}
        state = prb.initState
        print(prb.initState.__hash__())
        Search.Gn[state.__hash__()] = 0
        Search.fn(state)
        cut_off = Search.Fn[state.__hash__()]
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for i in neighbors:
                Search.gn(state, i, 1)
                Search.fn(i)
                Search.add_hash(i)
            neighbors = Search.sort_neighbors_fn(neighbors)

            for c in neighbors:
                if Search.Fn[c.__hash__()] <= cut_off:
                    print(c.__hash__(), cut_off)
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    visited_hash[c.__hash__()] = c
                    queue.append(c)
                    queue = Search.sort_neighbors_fn(queue)
                elif not c.__hash__() in visited_hash.keys():
                    unexpanded[c.__hash__()] = Search.Fn[c.__hash__()]
            if len(queue) == 0:
                print(prb.initState.__hash__())
                queue.append(prb.initState)
                cut_off = min(unexpanded.values())
                Search.Fn = {}
                Search.Gn = {}
                unexpanded = {}
                Search.Gn[prb.initState.__hash__()] = 0
                print(cut_off)
        return None

    @staticmethod
    # receives the parent and child node and increments the child value based on the parent, and it's value
    # note that for the first node you should set the value yourself
    def gn(parent, child, child_cost):
        Gn = Search.Gn
        Gn[child.__hash__()] = Gn[parent.__hash__()] + child_cost
        Search.Gn = Gn
        return Gn[child.__hash__()]

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
    def sort_neighbors_fn(neighbors):
        fn_neighbors = {}
        for s in neighbors:
            fn_neighbors[s.__hash__()] = Search.Fn[s.__hash__()]
        neighbors = []
        while len(fn_neighbors.values()) > 0:
            min_value = min(fn_neighbors.values())
            for s in fn_neighbors:
                if fn_neighbors[s] == min_value:
                    neighbors.append(Search.states_hash[s])
                    del fn_neighbors[s]
                    break
        return neighbors

    @staticmethod
    def fn(state):
        gn = Search.Gn[state.__hash__()]
        hn = Heuristic.heuristic(state)
        Search.Fn[state.__hash__()] = gn + hn
        pass
