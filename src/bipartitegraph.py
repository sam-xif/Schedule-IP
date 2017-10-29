"""
Implementation of bipartite graph
"""

from src.classcode import ClassCode

class BipartiteGraph:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise Exception("Arguments 'x' and 'y' not of the same length")

        self.x = x
        self.y = y
        self.edges = []
        self.matching = []

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
                            self.edges.append((i, j))
