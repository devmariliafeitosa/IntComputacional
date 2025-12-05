from .estado import State

class VacuumProblem:
    def __init__(self, initial_state):
        self.initial = initial_state
        self.actions = ["LEFT", "RIGHT", "SUCK"]

    def transition(self, state, action):
        loc = state.location
        dirt = state.dirty.copy()

        if action == "LEFT":
            if loc == "B":
                loc = "A"

        elif action == "RIGHT":
            if loc == "A":
                loc = "B"

        elif action == "SUCK":
            dirt[loc] = False

        return State(loc, dirt)

    def is_goal(self, state):
        return state.is_goal()
