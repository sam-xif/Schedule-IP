

class Vertex:
    def __init__(self, data):
        self.potential = 0
        self.edges = []
        self.data = data

class VertexGroup:
    def __init__(self, data, numClones):
        self.data = data
        self.numClones = numClones
        self.numExposed = 0
        self.vertices = [Vertex(data) for x in range(numClones)]

    def exposeNext(self):
        if numExposed < numClones:
            return False
        self.numExposed += 1
        return True

    def connectToNew(self, other):
        pass

    def changePotential(self, vertex, amount):
        vertex.potential += amount

    def __iter__(self):
        return self.vertices[0:numExposed]