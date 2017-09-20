import pyglet
import math

class square_class:
    def __init__(self, ID, color, position, edge_length):
        """ initialize a square with 3D position """
        self.ID = ID
        self.color = color
        self.position = position
        self.edge_length = edge_length

    def setPosition(self, position):
        """ set the x,y,z coordinates of the triangle """
        self.position = position

    def getColor(self):
        """ set the x,y,z coordinates of the triangle """
        return self.color

    def getPosition(self):
        """ return the position coordinate of the square """
        return self.position

    def calculateSquareVertices(self,dimensions,adjustment):
        """ function which calculates the vertex list required to draw the square """
        # Dimensions e.g. [0,1] for x,y
        vertices = []  # initialize a list of vertices

        for i in range(0, 4):
            angle = i * (0.5) * math.pi  # specify a vertex of the triangle (x,y values)
            x = self.edge_length* math.cos(angle) + self.position[dimensions[0]] + adjustment[0]
            y = self.edge_length * math.sin(angle) + self.position[dimensions[1]] + adjustment[1]
            vertices.append(x)  # append the x value to the vertex list
            vertices.append(y)  # append the y value to the vertex list

        # convert the vertices list to pyGlet vertices format for the first triangle & return this list
        vertexList = pyglet.graphics.vertex_list(4, ('v2f', vertices))
        return vertexList

    def getBackSquare(self):
        vertices = []
        for i in range(0,4):
            angle = (math.pi/4.) + i * (0.5) * math.pi
            x = self.edge_length* math.cos(angle) + self.position[0]
            y = self.edge_length * math.sin(angle) + self.position[1]
            vertices.append(x)  # append the x value to the vertex list
            vertices.append(y)  # append the y value to the vertex list
        vertexList = pyglet.graphics.vertex_list(4, ('v2f', vertices))
        return vertexList
