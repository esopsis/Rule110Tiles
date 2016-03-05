from __future__ import division
import pygame
import sys
import math
pygame.init()
WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
import objects
import drawers
import misc

""" baseInfinity.py
by Eric J.Parfitt (ejparfitt@gmail.com)

This program lets one arrange certain tiles together which emulate a
rule 110 cellular automaton.

Version: 1.0 alpha
"""

FPS = 60
clock = pygame.time.Clock()

# The speed with which the display resizes
RESIZE_FACT = .9
# Factors for determining maximum and minimum scale when zooming in or
# out
MAX_SCALE = 1
MIN_SCALE = .005

# isSnapped refers to whether or not two groups of tiles currently
# appear snaped together
isScrollUp = isScrollDown = isDrag = isMouseDown = isLDown = isRDown = \
        isSnapped = False
# gridRes refers to the resolution of a grid on which tiles are placed,
# which increases when zoomed in and decreases when zoomed out
oldMouseLoc = gridRes = None
# selectedTile is the tile which is currently being clicked on.
# snadTile is the first tile from one moving group to attempt to snap to
# a tile in another group.  snadSide and adjSide are the sides which are
# going to snap together, snapd being the moving one, and adj being the
# stationary one.  snapdTile keeps track of one of the tiles which could
# snap to another one if the user unclicks
selectedTile = snapdTile = snapdSide = adjSide = None
selectedTiles = []
# sidesToSnap keeps track of tiles which can potentially be merged
# into one snapped together group if the mouse is unclicked
sidesToSnap = []
myCanvas = objects.Canvas(windowSurface)
# Tiles keeps track of tiles, with tiles at the top layer at the end of
# the list, and tiles at the bottom at the beginning of the list
startTile = objects.Tile(myCanvas, objects.TileSet.rYB)
startTile.setPosition((WIDTH / 2, HEIGHT / 2))
tiles = [startTile]
#print(tiles)
# Sets up a grid which is used to only update tiles near the tiles
# currently being modified.
grid, gridRes = misc.setGrid(myCanvas, tiles)
# palletBack is just a white rectangle which is drawn behind the
# tile pallet, which has all the tiles which can be chosen from
palletBack = misc.resizePalletBack(myCanvas)
# Draws the tile pallet, along with any tiles specified by the variable
# "tiles"
drawers.initDraw(myCanvas, tiles, palletBack, windowSurface)
isComputerTurn = True
inPlay = tiles
# Run loop
while(True):               
    isClick = isUnClick = False
    button = None
    # Check for mouse clicks and unclicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                button = event.button
                isClick = True
            if event.button == 4:
                isScrollUp = True
                # Changes Canvas.scale to decrease the size of the scene
                newScale = objects.Canvas.scale / RESIZE_FACT
                # Limits maximum size
                if newScale <= MAX_SCALE:
                    objects.Canvas.scale = newScale
            if event.button == 5:
                isScrollDown = True
                newScale = objects.Canvas.scale * RESIZE_FACT
                # Limits minimum size
                if newScale >= MIN_SCALE:
                    objects.Canvas.scale = newScale
        elif event.type == pygame.MOUSEBUTTONUP:
            isUnClick = True
    # Get mouse location
    mouseLoc = pygame.mouse.get_pos()
    # Updates the scene
    inPlay, selectedTiles, grid, gridRes, isDrag, selectedTile, palletBack, \
            isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide, \
            oldMouseLoc, isComputerTurn = misc.update(myCanvas, inPlay, tiles,
            selectedTiles, mouseLoc, button, isUnClick, isClick, isScrollDown, isScrollUp,
            grid, gridRes, isDrag, selectedTile, palletBack, isSnapped,
            sidesToSnap, snapdTile, snapdSide, adjSide, isComputerTurn, clock, FPS,
            oldMouseLoc, windowSurface)
    isScrollDown = isScrollUp = False
