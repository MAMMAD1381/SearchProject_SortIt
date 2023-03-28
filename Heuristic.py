from Pipe import Pipe
from State import State


class Heuristic:
    def __init__(self, state: State):
        self.state = state
        self.colors = self.get_color(state)
        self.color_status = self.pipe_balls(self.state)
        self.goal_state(state, self.colors, self.color_status)
        pass


    def get_color(self, state: State):
        colors = []
        pipe_limit = state.pipes[0].limit
        for pipe in state.pipes:
            for ball in pipe.stack:
                if not ball in colors:
                    colors.append(ball)
        return colors

    def goal_state(self, state: State, colors: list, color_status):
        best_pipe_for_color = {}

        for color in colors:
            pipe_color_index = []
            color_preference = []
            for pipe in state.pipes:
                counter = 0
                for ball in pipe.stack:
                    if ball == color:
                        counter += 1
                    else:
                        break
                pipe_color_index.append(state.pipes.index(pipe))
                color_preference.append(counter / pipe.limit)
                best_pipe_for_color[color] = [pipe_color_index, color_preference]
        print(best_pipe_for_color)
        print('*'*10)

        pipe_limit = state.pipes[0].limit
        number_of_pipes = len(state.pipes)
        pipes = []
        for key in range(number_of_pipes):
            pipe = Pipe([], pipe_limit)
            pipes.append(pipe)

        for key in color_status.keys():
            for num_colors in range(color_status[key]):
                best_pipe_to_fill_value = max(best_pipe_for_color[key][1])
                best_pipe_to_fill_index = best_pipe_for_color[key][1].index(best_pipe_to_fill_value)
                # best_pipe_for_color[key][0].remove(best_pipe_to_fill_index)
                # best_pipe_for_color[key][1].remove(best_pipe_to_fill_value)
                best_pipe_for_color[key][1][best_pipe_to_fill_index] = -1
                print(best_pipe_to_fill_index)
                for counter in range(pipes[best_pipe_to_fill_index].limit):
                    pipes[best_pipe_to_fill_index].stack.append(key)
                for pipe in pipes:
                    print(pipe.stack)
        return state

    def pipe_balls(self, state: State):
        color_pipe = {}
        colors = []
        pipe_limit = state.pipes[0].limit
        for pipe in state.pipes:
            for ball in pipe.stack:
                colors.append(ball)
        # print(colors)
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


        return color_pipe

    def heuristic(state: State) -> int:  # this method returns a value based on how far a state is from goal
        n = 0
        o = 0
        x = 0
        for i in state.pipes:
            if not (i.is_full() or i.is_empty()):
                o += min(len(i.stack), (i.limit - len(i.stack)))  # moves to either empty a pipe or fill it
            for j in range(0, len(i.stack)):
                if i.stack[0] != i.stack[j]:
                    n += len(i.stack) - j  # upper balls that we need to remove
                    break
            filled_pipes = 0
            for pipe in state.pipes:
                if len(pipe.stack) > 0:
                    filled_pipes += 1
                    is_all_one_color = False
                    current_ball = pipe.stack[0]
                    for ball in pipe.stack:
                        if ball == current_ball:
                            is_all_one_color = True
                        else:
                            is_all_one_color = False
                            break
                    if is_all_one_color:
                        x += 1

        return int(n + o / 2 + x / len(state.pipes))
