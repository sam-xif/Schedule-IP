"""
File containing implementations of scheduling algorithms.
"""

import sys
import os
if __name__=='__main__':
    sys.path.append(os.path.realpath('../')) # Assuming the script is run from within the src directory


from src.scheduler import *
from src.bipartitegraph import BipartiteGraph, Edge

class HungarianScheduler(BasicScheduler):
    """
    Implementation of scheduling using a bipartite graph algorithm
    """

    def generateCostMatrix(self, n):
        self.costMatrix = [[0 for x in range(n)] for y in range(n)]
        # Generate cost matrix

    def edgeCost(self, x, y):
        # Define preference cost function
        prefCostFunc = lambda x : x**2

        # Get some info from the requests object
        req = x[0]
        requests = [[req.course1, req.c1alt1, req.c1alt2, req.c1alt3], 
                                [req.course2, req.c2alt1, req.c2alt2, req.c2alt3], 
                                [req.course3, req.c3alt1, req.c3alt2, req.c3alt3], 
                                [req.course4, req.c4alt1, req.c4alt2, req.c4alt3], 
                                [req.course5, req.c5alt1, req.c5alt2, req.c5alt3]]
        student = req.student

        for course in requests:
            for i, alternate in enumerate(course):
                if ClassCode.getClassCodeFromTitle(alternate) == ClassCode.getClassCodeFromTitle(y.classCode):
                    return prefCostFunc(i)

        # TODO: Change this: Instead of returning absurdly high cost, make it so edges that connect students to course they didn't ask for are disallowed.
        return 100000

    # Only needs to implement generateSchedule
    def generateSchedule(self):
        ### TODO: Fill out the code for generating the left and right columns

        # Generate nodes for (student, period) pairs* 
        left = []
        # We use self.requests instead of self.student because the Request object contains a reference to the student as well as the course request data
        # This is useful for calculating the weights of the edges
        for r in self.requests:
            left.extend([(r, p) for p in range(1, 8)])

        # Generate nodes for spots in classes
        right = []
        for c in self.classes:
            right.extend([c for c in range(len(c.targetCapacity))])

        self.graph = BipartiteGraph(left, right)

        # Generate initial collection of edges
        for i, x in enumerate(self.graph.x):
            for j, y in enumerate(self.graph.y):
                self.graph.edges.add(Edge(i, j, self.graph, direction=0))

        self.generateCostMatrix(len(self.graph.x))

        self.tightEdges = []

        # Initialize potential
        self.potentialX = [0 for x in range(len(self.graph.x))]
        self.potentialY = [0 for x in range(len(self.graph.y))]

        """
        in the BipartiteGraph that is used in this function,
         the matching variable stores the set of edges directed from x -> y.
        Initially, edges are created that are directed from y -> x.

        The algorithm also maintains that all edges in the matching are tight.
        """

        # while we have not reached a perfect matching
        while len(self.graph.matching) < len(self.graph.x):
            # Gets a list of tight edges in graph
            self.tightEdges = [edge 
                          for edge in self.graph.edges 
                          if self.costMatrix[edge.xn][edge.yn] == self.potentialX[edge.xn] + self.potentialY[edge.xn]]

            self.graph.matching = set([x for x in self.tightEdges if x.direction == 1])

            X = set([(0, x) for x in range(len(self.graph.x))])
            Y = set([(1, x) for x in range(len(self.graph.y))])
            r_x = X - set([(0, x.xn) for x in self.graph.matching])
            r_y = Y - set([(1, x.yn) for x in self.graph.matching])

            tightEdgesXs = [edge.xn for edge in tightEdges]

            # Gets a list of the edges that start in r_x
            tightEdgesFrom_r_x = [edge
                                  for edge in tightEdges
                                  if edge.direction == 0
                                  and edge.xn in tightEdgesXs]

            # Perform a breadth-first search through the collection of tight edges from r_x
            Z = set()
            paths = []
            queue = []

            for i, edge in enumerate(tightEdgesFrom_r_x):
                # Two extra tags are added to the end of each tuple here
                # The 3rd value is the number of the path
                # The 4th value indicates the position of the node in the path
                queue.append((0, edge.xn, i, 0))

            while len(queue) > 0:
                vertex = queue.pop(0)
                Z.add((vertex[0], vertex[1]))
                paths.append(vertex)
                for edge in tightEdges:
                    if vertex[0] == 0 and edge.xn == vertex[1] and edge.direction == 0:
                        queue.append((1, edge.yn, vertex[2], vertex[3] + 1))
                    elif vertex[0] == 1 and edge.yn == vertex[1] and edge.direction == 1:
                        queue.append((0, edge.xn, vertex[2], vertex[3] + 1))

            intersection = r_y & Z
            if len(intersection):
                # reverse the orientation of paths[0]
                path = []
                for i in range(max([x[2] for x in paths]) + 1):
                    path = [x for x in paths if x[2] == i]
                    if len(path) % 2 == 0:
                        break

                path.sort(key=lambda x: x[3])

                for i in range(len(path) - 1):
                    for edge in self.graph.edges:
                        if path[i][0] == 0 and edge.direction == 0:
                            if edge.xn == path[i][1] and edge.yn == path[i+1][1]:
                                edge.flip()
                        if path[i][0] == 1 and edge.direction == 1:
                            if edge.yn == path[i][1] and edge.xn == path[i+1][1]:
                                edge.flip()
            else:
                i = Z & X
                j = Y - Z
                
                values = []
                for m, x in i:
                    for n, y in j:
                        values.append(costMatrix[x][y] - potentialX[x] - potentialY[y])

                delta = min(values)
                for m, vert in i:
                    potentialX[vert] += delta
                for m, vert in (Z & Y):
                    potentialY[vert] -= delta

if __name__=="__main__":
    sched = HungarianScheduler()


