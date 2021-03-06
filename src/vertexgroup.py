import random

class Vertex:
    def __init__(self, data, group=None):
        """
        group is a reference to the vertex group that the vertex is a part of, if any.
        """

        self.potential = 0
        self.edges = []
        self.data = data
        self.id = self.generateID(32);
        self.group = group

    def generateID(self, length):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join([random.choice(alphabet) for x in range(length)])

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id.__hash__()

class VertexGroup:
    def __init__(self, vertices, tag=None):
        self.vertices = vertices
        for v in self.vertices:
            v.group = self
        self.numExposed = 1
        #self.vertices = [Vertex(data, group=self) for x in range(numClones)]
        self.tag = tag

    def exposeNext(self):
        if self.numExposed < len(self.vertices):
            return False
        self.numExposed += 1
        return True

    def getExposedVertex(self):
        if self.numExposed <= 0:
            raise Exception("No edges have been exposed yet")
        return self.vertices[self.numExposed - 1]

    def connectToNew(self, other):
        pass

    def changePotential(self, vertex, amount):
        vertex.potential += amount

    def __iter__(self):
        return iter(self.vertices[0:self.numExposed])