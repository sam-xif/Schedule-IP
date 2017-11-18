"""
File containing implementations of scheduling algorithms.
"""

import sys
import os
import itertools

if __name__=='__main__':
    sys.path.append(os.path.realpath('../')) # Assuming the script is run from within the src directory

from tqdm import tqdm

from src.scheduler import *
from src.bipartitegraph import BipartiteGraph, Edge
from src.vertexgroup import VertexGroup, Vertex

class HungarianScheduler(BasicScheduler):
    """
    Implementation of scheduling using a bipartite graph algorithm
    """

    def generateCostMatrix(self, n, m, groupDict):
        self.costMatrix = []
        boundPairs = [(groupDict[x][0], groupDict[x][-1]) for x in groupDict]
        for x in tqdm(range(n), ascii=True):
            self.costMatrix.append({})
            #pair = (groupDict[x][0], groupDict[x][-1])
            for p in boundPairs:
                #ynode = self.graph.y[y]
                cost = self.edgeCost(x, p[0])
                self.costMatrix[x][p] = cost



        #self.costMatrix = [[self.edgeCost(x, y) for y in range(m)] for x in tqdm(range(n), ascii=True)]
        # Generate cost matrix

    def edgeCost(self, x, y):
        # Assume x and y are Vertex objects

        # Define preference cost function
        prefCostFunc = lambda x : x**2

        # Get some info from the requests object
        req = x.data[0]
        if req is None: # i.e. Dummy student required to even out the two sides of the graph. Cost is 0
            return 0

        requests = [[req.course1, req.c1alt1, req.c1alt2, req.c1alt3], 
                                [req.course2, req.c2alt1, req.c2alt2, req.c2alt3], 
                                [req.course3, req.c3alt1, req.c3alt2, req.c3alt3], 
                                [req.course4, req.c4alt1, req.c4alt2, req.c4alt3], 
                                [req.course5, req.c5alt1, req.c5alt2, req.c5alt3]]
        student = req.student

        for course in requests:
            for i, alternate in enumerate(course):
                if alternate != '':
                    if ClassCode.getClassCodeFromTitle(alternate) == ClassCode.getClassCodeFromTitle(y.data.classCode):
                        return prefCostFunc(i)

        # TODO: Change this: Instead of returning absurdly high cost, make it so edges that connect students to course they didn't ask for are disallowed.
        return 100000

    def createCourseDict(self, courses):
        ret = {}
        for c in courses:
            code = ClassCode.getClassCodeFromTitle(c.classCode)
            if code in ret:
                ret[code].append(c)
            else:
                ret[code] = [c]

        return ret

    def getCostOfEdge(self, x, y):
        dict = self.costMatrix[x]
        for key in dict:
            if y >= key[0] and y <= key[1]:
                return dict[key]

    def setCostOfEdge(self, x, y, value):
        dict = self.costMatrix[x]
        for key in dict:
            if y >= key[0] and y <= key[1]:
                dict[key] = value

    # Only needs to implement generateSchedule
    def generateSchedule(self):
        ### TODO: Fill out the code for generating the left and right columns
        ### TODO: Generate a set that is the union of all classes the students request

        requestedCourses = set()

        for req in self.requests:
            courses = set([req.course1, req.c1alt1, req.c1alt2, req.c1alt3, 
                                req.course2, req.c2alt1, req.c2alt2, req.c2alt3, 
                                req.course3, req.c3alt1, req.c3alt2, req.c3alt3, 
                                req.course4, req.c4alt1, req.c4alt2, req.c4alt3, 
                                req.course5, req.c5alt1, req.c5alt2, req.c5alt3])
            requestedCourses = requestedCourses | courses

        courseDict = self.createCourseDict(self.classes)
        

        # Generate nodes for (student, period) pairs* 
        left = []
        # We use self.requests instead of self.student because the Request object contains a reference to the student as well as the course request data
        # This is useful for calculating the weights of the edges
        for r in self.requests:
            left.extend([Vertex((r, p)) for p in range(1, 8)])

        courseGroups = {}

        # Generate nodes for spots in classes
        right = []
        for courseName in requestedCourses:
            if courseName != '':
                code = ClassCode.getClassCodeFromTitle(courseName)
                if code in courseDict:
                    courseGroups[code] = []
                    index = len(right)
                    for c in courseDict[code]:
                        right.append(VertexGroup(c, c.targetCapacity))
                        for s in range(c.targetCapacity):
                            courseGroups[code].append(index)
                            index += 1
                            #right.append(c)

        # Even out the graph
        #while len(left) < len(right):
        #    left.append((None, 0))

        self.graph = BipartiteGraph(left, right)

        # Generate initial collection of edges
        for i, x in enumerate(tqdm(self.graph.x, ascii=True, desc="populating graph")):
            for group in self.graph.y:
                for y in group:
                    e = Edge(x, y, self.graph, direction=0)
                    e.setCost(self.edgeCost(x, y))
                    self.graph.edges.append(e)


        #print("\nGenerating cost matrix...\n")
        #self.generateCostMatrix(len(self.graph.x), len(self.graph.y), courseGroups)

        self.tightEdges = []

        # Initialize potential
        #self.potentialX = [0 for x in range(len(self.graph.x))]
        #self.potentialY = [0 for x in range(len(self.graph.y))]

        """
        in the BipartiteGraph that is used in this function,
         the matching variable stores the set of edges directed from y -> x.
        Initially, edges are created that are directed from x -> y.

        The algorithm also maintains that all edges in the matching are tight.
        """

        # while we have not reached a perfect matching
        while len(self.graph.matching) < len(self.graph.x):
            # Gets a list of tight edges in graph
            self.tightEdges = [edge 
                          for edge in tqdm(self.graph.edges, ascii=True, desc="getting tight edges")
                          if edge.isTight()]

            self.graph.matching = set([x for x in self.tightEdges if x.direction == 1])

            print("generating subsets...")
            X = set([(0, x) for x in self.graph.x])
            Y = set(itertools.chain.from_iterable([[(1, y) for y in x] for x in self.graph.y]))
            r_x = X - set([(0, x.x) for x in self.graph.matching])
            r_y = Y - set([(1, x.y) for x in self.graph.matching])

            tightEdgesXs = [edge.x for edge in self.tightEdges]

            # Gets a list of the edges that start in r_x
            tightEdgesFrom_r_x = [edge
                                  for edge in self.tightEdges
                                  if edge.direction == 0
                                  and edge.x in tightEdgesXs]

            # Perform a breadth-first search through the collection of tight edges from r_x
            Z = set()
            paths = []
            queue = []
            print("Executing breadth-first search...")
            for i, edge in enumerate(tightEdgesFrom_r_x):
                # Two extra tags are added to the end of each tuple here
                # The 3rd value is the number of the path
                # The 4th value indicates the position of the node in the path
                queue.append((0, edge.x, i, 0))

            while len(queue) > 0:
                vertex = queue.pop(0)
                Z.add((vertex[0], vertex[1]))
                paths.append(vertex)
                for edge in vertex[1].edges:
                    if edge.isTight():
                        queue.append((1 - edge.direction, edge.y, vertex[2], vertex[3] + 1))

            intersection = r_y & Z
            if len(intersection):
                # reverse the orientation of paths[0]
                print("sorting path")
                paths.sort(key=lambda x: x[2])
                
                index = 0
                while paths[index][2] == 0: index += 1
                path = paths[0:index]
                path.sort(key=lambda x: x[3])
                
                fullpath = []
                counter = 0
                while path[counter][3] == counter: 
                    fullpath.append(path[counter])
                    counter += 1

                if len(fullpath) % 2 == 1: fullpath = fullpath[0:len(fullpath) - 1]

                pathEdges = []
                for u, v in zip(fullpath, fullpath[1:]):
                    for edge in u[1].edges:
                        if edge.y == v[1]:
                            pathEdges.append(edge)

                for edge in pathEdges:
                    print("Edge flipped")
                    edge.flip()
                    if edge.direction == 1:
                        self.graph.matching.add(edge)
                    else:
                        self.graph.matching.remove(edge)
            else:


                i = Z & X
                j = Y - Z
                
                values = []
                for m, x in i:
                    for n, y in j:
                        values.append(self.getCostOfEdge(x, y) - self.potentialX[x] - self.potentialY[y])

                delta = min(values)
                for m, vert in i:
                    self.potentialX[vert] += delta
                for m, vert in (Z & Y):
                    self.potentialY[vert] -= delta

if __name__=="__main__":
    """Main procedure for generating schedules"""
    # Add students

    cap = 18

    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    students = session1.query(models.Student).all()

    # Load class, student, and request data from database
    students = [pymodels.Student.__import__(x) for x in session1.query(models.Student).all()]
    requests = [pymodels.SimpleRequest.__import__(x) for x in session1.query(models.SimpleRequest).all()]
    classes = [pymodels.Class.__import__(x) for x in session1.query(models.Class).all()]

    for c in classes:
        c.slotsRemaining = cap


    scheduler = HungarianScheduler(students, requests, classes, session1)

    # Perform scheduling
    scheduler.generateSchedule()
    scheduler.commit()
    # TODO: Update objects modified in generateSchedule(), then commit
    # Note: Updates are processed automatically when changes to the pymodels are made

    costInfo = (scheduler.cost(), scheduler.cost()[0] / len(scheduler.schedule))

    # Commit
    session1.commit()
    session1.close()

