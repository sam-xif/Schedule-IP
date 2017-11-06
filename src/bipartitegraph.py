"""
Implementation of bipartite graph
"""

from src.classcode import ClassCode

class Edge:
    def __init__(self, xn, yn, graph, direction=None):
        """
        direction is an optional parameter that is None by default.
        If it is set to 0, the direction is from x -> y
        If it is set to 1, the direction is from y -> x
        """
        if direction != 0 or direction != 1 or direction is not None:
            raise Exception("Invalid value for direction")

        self.xn = xn
        self.yn = yn
        self.directed = direction is not None
        self.direction = direction
        self.graph = graph

    def getTuple(self):
        if directed:
            if direction == 1:
                return (self.graph.x[self.xn], self.graph.y[self.yn])
            else:
                return (self.graph.y[self.yn], self.graph.x[self.xn])
        else:
            return (self.graph.x[self.xn], self.graph.y[self.yn])

    def flip(self):
        if self.directed:
            self.direction = 1 if self.directed == 0 else 0
        #tmp = self.xn
        #self.xn = self.yn
        #self.yn = tmp

    def __eq__(self, other):
        return self.xn == other.xn and self.yn == other.yn and self.direction == other.direction

class BipartiteGraph:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise Exception("Arguments 'x' and 'y' not of the same length")

        self.x = x
        self.y = y
        self.edges = set()
        self.connectedEdges = set()
        self.matching = set()

    def generatePossibleEdges(self, classes):
        """
        Generate all possible edges of the graph based on student course requests
        """
        for i, studentNode in enumerate(self.x):
            req = studentNode.requestObj
            requests = [[req.course1, req.c1alt1, req.c1alt2, req.c1alt3], 
                                  [req.course2, req.c2alt1, req.c2alt2, req.c2alt3], 
                                  [req.course3, req.c3alt1, req.c3alt2, req.c3alt3], 
                                  [req.course4, req.c4alt1, req.c4alt2, req.c4alt3], 
                                  [req.course5, req.c5alt1, req.c5alt2, req.c5alt3]]

            for request in requests:
                for course in request:
                    classCode = ClassCode.getClassCodeFromTitle(course)
                    
                    for j, courseSpot in enumerate(self.y):
                        if ClassCode.getClassCodeFromTitle(courseSpot.classCode) == classCode:
                            self.edges.append(Edge(i, j))