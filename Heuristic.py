from Pipe import Pipe
from State import State


class Heuristic:
    goal_pipes: list
    def __init__(self, state: State):
        self.state = state
        self.colors = self.get_color(state)
        self.color_status = self.pipe_balls(self.state)
        Heuristic.goal_pipes = self.goal_state(state, self.colors, self.color_status)

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
        print('*' * 10)

        pipe_limit = state.pipes[0].limit
        number_of_pipes = len(state.pipes)
        pipes = []
        for key in range(number_of_pipes):
            pipe = Pipe([], pipe_limit)
            pipes.append(pipe)

        yatim = []
        for key in color_status.keys():
            for num_colors in range(color_status[key]):
                best_pipe_to_fill_value = 0
                best_pipe_to_fill_index = 0
                best_pipe_to_fill_value = max(best_pipe_for_color[key][1])
                if best_pipe_to_fill_value == 0:
                    yatim.append(key)
                    break
                else:
                    best_pipe_to_fill_index = best_pipe_for_color[key][1].index(best_pipe_to_fill_value)
                best_pipe_for_color[key][1][best_pipe_to_fill_index] = -1
                for counter in range(pipes[best_pipe_to_fill_index].limit):
                    pipes[best_pipe_to_fill_index].stack.append(key)
        for baby in yatim:
            for pipe in pipes:
                if pipe.is_empty():
                    for counter in range(pipe.limit):
                        pipe.stack.append(baby)
                    break
        if self.is_goal(pipes):
            print('goal:')
            for pipe in pipes:
                print(pipe.stack)
            print(';')
            return pipes
        else:
            print('fuck')
            return None

    def is_goal(self, pipes) -> bool:  # this method check this state is goal or not
        for i in pipes:
            if not i.is_one_color() or (not (i.is_full() or i.is_empty())):
                return False
        return True

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

    @staticmethod
    def heuristic(state: State) -> int:  # this method returns a value based on how far a state is from goal
        n = 0
        o = 0
        x = 0
        h = 0
        for pipe in state.pipes:
            if not (pipe.is_full() or pipe.is_empty()):
                o += min(len(pipe.stack), (pipe.limit - len(pipe.stack)))  # moves to either empty a pipe or fill it
            for j in range(0, len(pipe.stack)):
                if pipe.stack[0] != pipe.stack[j]:
                    n += len(pipe.stack) - j  # upper balls that we need to remove
                    break

        goal_pipes = Heuristic.goal_pipes
        for pipe in enumerate(state.pipes):
            for ball in range(min(len(state.pipes[pipe[0]].stack), len(goal_pipes[pipe[0]].stack))):
                if not goal_pipes[pipe[0]].stack[ball] == state.pipes[pipe[0]].stack[ball]:
                    h += goal_pipes[pipe[0]].limit - ball
                    break
            # if len(goal_pipes[pipe[0]].stack) == 0:
            #     h += len(state.pipes[pipe[0]].stack)
                # print(ball, goal_pipes[pipe[0]].stack[ball], state.pipes[pipe[0]].stack[ball])

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
        x = x/state.pipes[0].limit

        return int(n + o / 2 + h)
