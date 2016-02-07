#TODO: Tiles should maybe turn red one frame earlier
from __future__ import division
import pygame
import sys
import math
#import copy
#from operator import add, sub
#from pygame.locals import *
pygame.init()
WIDTH = 200
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
#import arrangers
import objects
#import checkers
#import common
import drawers
import misc
#import movers
#import objects
#pygame.init()

#WIDTH = 1100
#HEIGHT = 600

FPS = 60
clock = pygame.time.Clock()

#rYB = pygame.image.load("rYB.png").convert_alpha()

#palletFiles = ["rB.png", "by.png", "rYB.png", "rY.png", "bR.png", "y.png",
        #"w.png"]
#palletFiles = ["rYB.png", "y.png", "bR.png", "bY.png", "rB.png", "rY.png",
        #"w.png"]
        
RESIZE_FACT = .9
'''
canvas = pygame.Surface((2000, 2000))
canvas.fill(WHITE)
'''
#isDrag = False

tiles = []
#tiles = tiles
'''
for i in range(2):
    tile = Tile(rYB, (0, 0))
    tiles.append(tile)
    tile.resize(self.scale)
draw(tiles)
'''

isScrollUp = isScrollDown = isDrag = isMouseDown = isLDown = isRDown = \
        isSnapped = False
#fromPallet = None
isSnapped = isUnSelectOld = False
canvas = objects.Canvas(tiles, windowSurface)
isArrangeStep = isArranging = isArrange = False
oldMouseLoc = oldPlayPosition = arrangeIndex = gridRes = None
activeRow = playCopy = selectedTile = fromPallet = snapdTile = snapdSide = \
        adjSide = groupGrid = None
selectedTiles = []
#TODO: needed?
oldselectedTiles = []
sidesToSnap = []
grid, gridRes = misc.setGrid(canvas, tiles)
palletBack = misc.resizePalletBack(canvas)
drawers.initDraw(canvas, tiles, palletBack, windowSurface)
while(True):
    isClick = isUnClick = isSpace = False
    button = None
    #print("in5")
    for event in pygame.event.get():
        #print("in4")
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print("in3")
            #button = event.button
            #print(event.button)
            #print(event.button)
            if event.button == 1 or event.button == 3:
                button = event.button
                isClick = True
                #print(event.button)
            if event.button == 4:
                isScrollUp = True
                newScale = objects.Canvas.scale / RESIZE_FACT
                if newScale <= 1:
                    objects.Canvas.scale = newScale
            if event.button == 5:
                isScrollDown = True
                newScale = objects.Canvas.scale * RESIZE_FACT
                if newScale >= .005:
                    objects.Canvas.scale = newScale
        elif event.type == pygame.MOUSEBUTTONUP:
            isUnClick = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isSpace = True

    #isScrollUp = isScrollDown = False
    #print(canvas.drawAll)
    #if canvas.drawAll or isScrollUp or isScrollDown:
        #canvas.draw(tiles)
    mouseLoc = pygame.mouse.get_pos()
    #print(isScrollDown, isScrollUp)
    #print(button)
    selectedTiles, isArrangeStep, grid, gridRes, groupGrid, arrangeIndex, \
            isArranging, activeRow, isDrag, selectedTile, fromPallet, \
            palletBack, oldselectedTiles, isSnapped, sidesToSnap, snapdTile, \
            playCopy, isArrange, oldPlayPosition, isUnSelectOld, snapdSide, \
            adjSide, oldMouseLoc = misc.update(canvas, tiles, selectedTiles,
            mouseLoc, button, isUnClick, isClick, isScrollDown, isScrollUp,
            isSpace, isArrangeStep, grid, gridRes, groupGrid, arrangeIndex,
            isArranging, activeRow, isDrag, selectedTile, fromPallet,
            palletBack, oldselectedTiles, isSnapped, sidesToSnap, snapdTile,
            playCopy, isArrange, oldPlayPosition, isUnSelectOld, snapdSide,
            adjSide, clock, FPS, oldMouseLoc, windowSurface)
    isScrollDown = isScrollUp = False
