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
                    if ClassCode.getClassCodeFromTitle(alternate) == y.tag: #ClassCode.getClassCodeFromTitle(y..classCode):
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
        for r in tqdm(self.requests, ascii=True, desc="initializing left"):
            left.extend([Vertex((r, p)) for p in range(1, 8)])

        courseGroups = {}

        # Generate nodes for spots in classes
        right = []
        for courseName in tqdm(requestedCourses, ascii=True, desc="initializing right"):
            if courseName != '':
                code = ClassCode.getClassCodeFromTitle(courseName)
                if code in courseDict:
                    courseGroups[code] = []
                    index = len(right)
                    vertices = []
                    for c in courseDict[code]:
                        for s in range(c.targetCapacity):
                            courseGroups[code].append(index)
                            index += 1
                            #right.append(c)
                        vertices.extend([Vertex(c) for x in range(c.targetCapacity)])

                    right.append(VertexGroup(vertices, tag=code))

        # Even out the graph
        #while len(left) < len(right):
        #    left.append((None, 0))

        self.graph = BipartiteGraph(left, right)

        # Generate initial collection of edges
        for i, x in enumerate(tqdm(self.graph.x, ascii=True, desc="populating graph")):
            for group in self.graph.y:
                for y in group:
                    e = Edge(x, y, self.graph, direction=0)
                    e.setCost(self.edgeCost(x, group))
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

        print("generating subsets...")
        #X = set([(0, x) for x in self.graph.x])
        #Y = set(itertools.chain.from_iterable([[(1, y) for y in x] for x in self.graph.y]))
        #r_x = X - set([(0, x.x) for x in self.graph.matching]) # Initially this set is all of X
        #r_y = Y - set([(1, x.y) for x in self.graph.matching]) # Initially this set is all of Y

        # Flag set to true if a potential change occured, which indicates the need to refresh the tight edge list
        potentialChange = True

        # Flag set when a potential change should be forced
        forcePotentialChange = False
        attemptManualMatch = False

        # while we have not reached a perfect matching...
        while len(self.graph.matching) < len(self.graph.x):
            print("Current length of matching:", len(self.graph.matching))

            if attemptManualMatch:
                print("MANUAL FALLBACK INVOKED")
                # This is executed when the algorithm has needs manual intervention to continue (i.e. forcing the connection of two nodes).
                # It is unclear exactly why the algorithm halts, but it may have to do with the fact that we dynamically expand the graph.

                # Attempt to match one element of r_x with the lowest cost element of r_y
                elem = list(r_x)[0]
                edges = [e for e in elem[1].edges if (1, e.y) in r_y]
                minCostEdge = sorted(edges, key=lambda x: x.cost)[0]
                delta = minCostEdge.cost - minCostEdge.x.potential - minCostEdge.y.potential
                minCostEdge.x.potential += delta
                minCostEdge.flip()

                attemptManualMatch = False

            if potentialChange:
                potentialChange = False

            X = set([(0, x) for x in self.graph.x])
            Y = set(itertools.chain.from_iterable([[(1, y) for y in x] for x in self.graph.y]))

            # Gets a list of tight edges in graph
            self.tightEdges = [edge 
                            for edge in tqdm(self.graph.edges, ascii=True, desc="getting tight edges")
                            if edge.isTight()]

            self.graph.matching = set([x for x in self.tightEdges if x.direction == 1])

            r_x = X - set([(0, x.y) for x in self.graph.matching]) # Initially this set is all of X
            r_y = Y - set([(1, x.x) for x in self.graph.matching]) # Initially this set is all of Y

            self.tightEdgesXs = set([edge.x for edge in tqdm(self.tightEdges, ascii=True, desc="getting x-vertices of tight edges") if (0, edge.x) in r_x])

            # Gets a list of the edges that start in r_x
            self.tightEdgesFrom_r_x = set([edge
                                    for edge in tqdm(self.tightEdges, ascii=True, desc="getting tight edges that start in r_x")
                                    if edge.direction == 0
                                    and edge.x in self.tightEdgesXs])

            # Perform a breadth-first search through the collection of tight edges from r_x
            Z = set()
            paths = []
            queue = []
            print("Executing breadth-first search...")
            for i, edge in enumerate(self.tightEdgesFrom_r_x):
                queue.append((0, edge.x))

            while len(queue) > 0:
                vertex = queue.pop(0)
                
                if vertex not in Z: #and vertex not in queue:
                    for edge in vertex[1].edges:
                        if edge.isTight():
                            queue.append((1 - edge.direction, edge.y))

                    Z.add(vertex)

            intersection = r_y & Z
            if len(intersection) and not forcePotentialChange:
                pathEdges = []
                pathStartIndex = 0
                pathFindingFailed = False

                while len(pathEdges) == 0:
                    #print("trying path", pathStartIndex)
                    #print(len(pathEdges))
                    path = []
                    if pathStartIndex >= len(self.tightEdgesXs):
                        pathFindingFailed = True
                        break
                    pathStart = list(self.tightEdgesXs)[pathStartIndex]
                    path.append(pathStart)
                    continuePath = True
                    while continuePath:
                        continuePath = False
                        for edge in path[len(path) - 1].edges:
                            if edge.isTight() and ((0, edge.y) in X or (1, edge.y) in r_y):
                                continuePath = True
                                path.append(edge.y)
                                pathEdges.append(edge)
                                break
                    pathStartIndex += 1

                if pathFindingFailed:
                    # If a path can't be found from r_x to r_y following tight edges, attempt to force a potential change
                    print("FORCING POTENTIAL CHANGE")
                    forcePotentialChange = True
                    continue

                if len(pathEdges) % 2 == 0: pathEdges = pathEdges[0:len(pathEdges) - 1]

                for edge in pathEdges:
                    try:
                        if edge.direction == 0:
                            self.tightEdgesFrom_r_x.remove(edge)
                            self.tightEdgesXs.remove(edge.x)
                        else:
                            self.tightEdgesFrom_r_x.append(edge)
                            self.tightEdgesXs.add(edge.y)
                    except ValueError:
                        pass

                    if edge.direction == 0:
                        edge.flip()
                        self.graph.matching.add(edge)

                        # Expose the next edge in the group
                        edge.x.group.exposeNext()
                        vert = edge.x.group.getExposedVertex()
                        r_y.add((1, vert))

                        # Connect to new edge
                        for x in tqdm(self.graph.x, ascii=True, desc="appending new edges"):
                            if x != edge.y:
                                e = Edge(x, vert, self.graph, 0)
                                e.setCost(self.edgeCost(x, vert.group))
                                self.graph.edges.append(e)
                            else:
                                pass

                        # Modify r_x and r_y

                        # Remove edge from r_x and r_y because these are subsets where the vertices are not contained in the matching
                        try:
                            r_x.remove((0, edge.y))
                            r_y.remove((1, edge.x))
                        except KeyError as e:
                            print("keyerror generated, likely because a path connected to an edge outside of r_x or r_y")
                    else:
                        self.graph.matching.remove(edge)
                        edge.flip()
                        # Modify r_x and r_y
                        #r_x.add((0, edge.x))
                        #r_y.add((1, edge.y))
            else:

                print("POTENTIAL CHANGE")
                i = Z & X
                j = Y - Z
                
                values = []
                for m, x in i:
                    for n, y in j:
                        edge = None
                        for e in x.edges:
                            if e.y == y:
                                edge = e
                                break
                        if edge is not None:
                            values.append(edge.cost - x.potential - y.potential)
                
                if len(values) == 0:
                    forcePotentialChange = False
                    attemptManualMatch = True
                    continue

                delta = min(values)
                for m, vert in i:
                    vert.potential += delta
                for m, vert in (Z & Y):
                    vert.potential -= delta

                potentialChange = True
                forcePotentialChange = False


if __name__=="__main__":
    """Main procedure for generating schedules"""
    # Add students

    cap = 10

    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    students = session1.query(models.Student).all()

    # Load class, student, and request data from database
    students = [pymodels.Student.__import__(x) for x in session1.query(models.Student).all()]
    requests = [pymodels.SimpleRequest.__import__(x) for x in session1.query(models.SimpleRequest).all()]
    classes = [pymodels.Class.__import__(x) for x in session1.query(models.Class).all()]

    for c in classes:
        c.targetCapacity = cap


    scheduler = HungarianScheduler(students, requests, classes, session1)

    # Perform scheduling
    scheduler.generateSchedule()

    tuples = [(match.y.data[0].student.name, match.x.data.classCode) for match in scheduler.graph.matching]
    tuples.sort(key=lambda x: x[0])
    
    for name, course in tuples:
        print('{} -> {}'.format(name, course))

    scheduler.commit()
    # TODO: Update objects modified in generateSchedule(), then commit
    # Note: Updates are processed automatically when changes to the pymodels are made

    costInfo = (scheduler.cost(), scheduler.cost()[0] / len(scheduler.schedule))

    # Commit
    session1.commit()
    session1.close()

