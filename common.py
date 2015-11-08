from __future__ import division
import pygame
from operator import add, sub
import math

def load(image):
    return pygame.image.load(image).convert_alpha()

def adjToScreen(position, scale, windowWidth, windowHeight):
    return myAdd(myMult(scale, position), (windowWidth / 2, windowHeight / 2))

def x(point):
    return point[0]

def y(point):
    return point[1]

def myAdd(vector1, vector2):
    return tuple(map(add, vector1, vector2))

def mySub(vector1, vector2):
    return tuple(map(sub, vector1, vector2))

def myMult(scalar, vector):
    return tuple([scalar * x for x in vector])

def myDiv(vector, scalar):
    return tuple([x / scalar for x in vector])

def getDistance(point1, point2):
    return math.sqrt((y(point1) - y(point2)) ** 2 +
            (x(point1) - x(point2)) ** 2)

def isInSquare(point, centerPoint, radius):
    return (abs(x(centerPoint) - x(point)) < radius and
            abs(y(centerPoint) - y(point)) < radius)

# Blits an object to the screen with desired opacity
def blitAlpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

def getOrDefault(array, i, default):
        if i < 0 or i >= len(array):
            return default
        return array[i]

def makeGrid(rows, cols, init):
    if init == "empty":
        return [[[] for j in range(cols)] for i in range(rows)]
    else:
        return [[init for j in range(cols)] for i in range(rows)]
