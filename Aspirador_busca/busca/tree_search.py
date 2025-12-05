from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def solution(self):
        actions = []
        node = self
        while node.parent:
            actions.append(node.action)
            node = node.parent
        return list(reversed(actions))


def tree_search(problem, strategy="bfs"):
    frontier = deque([Node(problem.initial)])

    while frontier:
        if strategy == "bfs":
            node = frontier.popleft()     # FIFO
        else:
            node = frontier.pop()         # LIFO (DFS)

        if problem.is_goal(node.state):
            return node.solution(), node

        for action in problem.actions:
            new_state = problem.transition(node.state, action)
            frontier.append(Node(new_state, node, action))

    return None
