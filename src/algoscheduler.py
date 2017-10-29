"""
File containing implementations of scheduling algorithms.
"""

from src.scheduler import *

class BipartiteScheduler(BasicScheduler):
    """
    Implementation of scheduling using a bipartite graph algorithm
    """
    def __init__(self, graph):
        self.graph = graph