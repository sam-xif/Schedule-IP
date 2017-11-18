"""
Implementation of bipartite graph
"""

from src.classcode import ClassCode

class Edge:
    def __init__(self, x, y, graph, direction):
        """
        x should be the vertex where the edge starts
        y should be the vertex where the edge ends
        edges are assumed to be directed unless direction is None
        """
        if direction != 0 and direction != 1 and direction is not None:
            raise Exception("Invalid value for direction")

        self.x = x
        self.y = y
        self.directed = direction is not None
        self.direction = direction
        self.graph = graph
        self.cost = 0

        if direction == 0:
            self.x.edges.append(self)
        else:
            self.y.edges.append(self)

    def getTuple(self):
        if self.directed:
            if self.direction == 1:
                return (x, y)
            else:
                return (y, x)
        else:
            return (x, y)

    def flip(self):
        if self.directed:
            if self.direction == 1:
                self.direction = 0
                self.y.edges.remove(self)
                self.x.edges.append(self)
            else:
                self.direction = 1
                self.x.edges.remove(self)
                self.y.edges.append(self)

            tmp = self.x
            self.x = self.y
            self.y = tmp

    def setCost(self, cost):
        self.cost = cost

    def isTight(self):
        return self.cost == self.x.potential + self.y.potential
                
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__() + (0 if self.direction is None else self.direction)

class BipartiteGraph:
    def __init__(self, x, y):
        #if len(x) != len(y):
        #    raise Exception("Arguments 'x' and 'y' not of the same length")

        self.x = x
        self.y = y
        self.edges = []
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