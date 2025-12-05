class State:
    """
    Representa um estado do mundo do aspirador.
    location: 'A' ou 'B'
    dirty: dict com {'A': True/False, 'B': True/False}
    """

    def __init__(self, location, dirty):
        self.location = location
        self.dirty = dirty

    def is_goal(self):
        return not self.dirty["A"] and not self.dirty["B"]

    def __repr__(self):
        return f"State(loc={self.location}, dirt={self.dirty})"

    def __eq__(self, other):
        return (
            self.location == other.location and
            self.dirty == other.dirty
        )

    def __hash__(self):
        return hash((self.location, tuple(self.dirty.items())))
