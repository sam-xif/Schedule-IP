"""
Implementation of bipartite graph
"""

class BipartiteGraph:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise Exception("Arguments 'x' and 'y' not of the same length")

        self.x = x
        self.y = y