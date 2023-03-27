from Pipe import Pipe
from State import State


class Heuristic:
    def __init__(self, state: State):
        self.state = state
        self.colors = self.state_colors(self.state)
        print(self.colors)
        # self.goal_state(self.state, self.colors)
        pass

    def goal_state(self, state: State, colors: list):
        print(colors)
        # test_path = 'tests/test4.txt'
        # file = open(test_path, 'r')
        # p = []
        # for i in file.readlines():
        #     a = i.replace('\n', '')
        #     a = a.replace(' ', '')
        #     a = a.split(',')
        #     p.append(Pipe(a[:-1], int(a[-1])))
        # final_state = State(p, None, 0, (0, 0))
        # for pipe in final_state.pipes:
        #     while len(pipe.stack) > 0:
        #         pipe.stack.pop()
        # for pipe in enumerate(state.pipes):
        #     for final_pipe in enumerate(final_state.pipes):
        #         final_state.pipes[final_pipe[0]].stack = state.pipes[pipe[0]].stack
        #         print(final_pipe)

        return state

    def state_colors(self, state: State):
        best_pipe_for_color = {}
        color_pipe = {}
        colors = []
        pipe_limit = state.pipes[0].limit
        for pipe in state.pipes:
            for ball in pipe.stack:
                colors.append(ball)
        print(colors)
        while len(colors) > 0:
            current_color = colors[0]
            counter = 0
            for ball in colors:
                if ball == current_color:
                    counter += 1
            while current_color in colors:
                colors.remove(current_color)
            if counter == pipe_limit:
                color_pipe[current_color] = 1
            elif counter == 2 * pipe_limit:
                color_pipe[current_color] = 2
        for pipe in state.pipes:
            current_ball = pipe.stack[0]
            counter = 0
            for ball in pipe.stack:
                if ball == current_ball:
                    counter += 1
                else:
                    break
            best_pipe_for_color[current_ball] = (state.pipes.index(pipe), counter / pipe.limit)
        print(best_pipe_for_color)
        return color_pipe
