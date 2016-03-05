from __future__ import division
import os
import pygame
import objects
import common
import checkers
import drawers
import movers
import game

def load(image):
    return common.load(os.path.join("images", image))

#Returns half the height of a tile, adjusted to the scale
def getAdjTileRad():
    return objects.TileSet.w.get_height() * objects.Canvas.scale / 2

# Adds a tile to a specific region of the grid
def toGrid(myCanvas, myObject, grid, resolution):
    row = int(common.y(myObject.getPosition()) // resolution) + 1
    col = int(common.x(myObject.getPosition()) // resolution) + 1
    if not (row == myObject.gridRow and col == myObject.gridCol):
        if myObject.gridRow is not None:
            grid[myObject.gridRow][myObject.gridCol].remove(myObject)
        if myObject.getRect().colliderect(0, 0, myCanvas.WIDTH,
                myCanvas.HEIGHT):
            myObject.gridRow = row
            myObject.gridCol = col
            grid[row][col].append(myObject)
        else:
            myObject.gridRow = myObject.gridCol = None

# Puts tiles on to a grid
def setGrid(myCanvas, tiles):
    gridRes = 2.2 * getAdjTileRad()
    rowNum = int(myCanvas.HEIGHT // gridRes + 3)
    colNum = int(myCanvas.WIDTH // gridRes + 3)
    grid = common.makeGrid(rowNum, colNum, "empty")
    for tile in tiles:
        tile.gridRow = tile.gridCol = None
        toGrid(myCanvas, tile, grid, gridRes)
    return grid, gridRes

# Sets the size of the back of the tile pallet
def resizePalletBack(myCanvas):
    lastTile = myCanvas.tilePallet[-1]
    palletBack = pygame.Rect(0, 0, common.x(lastTile.position) +
            lastTile.scaledImage.get_width() / 2,
            lastTile.scaledImage.get_height())
    return palletBack

# Resizes the display if the user is scrolling
def scrollSize(myCanvas, tiles, grid, gridRes, palletBack, isScrollDown,
        isScrollUp, dirtyRects, isDrawAll, windowSurface):
    if isScrollDown or isScrollUp:
        for tile in tiles:
            pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                    tile.getRect())
            dirtyRects.append(tile.getRect())
            tile.resize(objects.Canvas.scale)
            tile.scalePosition(objects.Canvas.scale)
        grid, gridRes = setGrid(myCanvas, tiles)
        for tile in myCanvas.tilePallet:
            pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                    tile.getRect())
            dirtyRects.append(tile.getRect())
            tile.resize(objects.Canvas.scale)
            tile.scalePosition(objects.Canvas.scale)
            dirtyRects.append(tile.getRect())
        palletBack = resizePalletBack(myCanvas)
        isDrawAll = True
    return grid, gridRes, palletBack, isDrawAll

# Returns areas on a grid that are surrounding an area on a grid which
# a location is in
def getAreasToCheck(location, grid, gridRes):
    row = int(common.y(location) // gridRes) + 1
    col = int(common.x(location) // gridRes) + 1
    areasToCheck = []
    for i in range(-1, 1 + 1):
        for j in range(-1, 1 + 1):
            if (row + i >= 0 and col + j >= 0 and row + i < len(grid) and
                    col + j < len(grid[0])):
                areasToCheck.append(grid[row + i][col + j])
    return areasToCheck

# Sets selected tile or selected tiles and mouse offsets for tile/tiles
# which have been selected.
def setMouseOffset(myCanvas, tiles, selectedTiles, mouseLoc, isDrag,
        selectedTile, grid, gridRes):
    # Only areas near the clicked tile are checked to see if they were
    # clicked on
    areasToCheck = getAreasToCheck(mouseLoc, grid, gridRes)
    for area in areasToCheck:
        for tile in area:
            # Part of this next block insures that only the tile on top
            # of other tiles is selected
            if (not isDrag and common.isInSquare(mouseLoc, tile.position,
                    tile.radius) and
                    common.getDistance(mouseLoc, tile.position) <
                    tile.radius and (selectedTile is None or
                    tiles.index(tile) > tiles.index(selectedTile))):
                selectedTile = tile
    # If there has been a left click, a single tile is selected.  If
    # there has been a right click, a group of snapped tiles is
    # selected.
    if selectedTile is not None:
        if myCanvas.isLDown:
            selectedTiles = [selectedTile]
        else:
            selectedTiles = []
            for tile in selectedTile.tileGroup:
                selectedTiles.append(tile)
        isDrag = True
        for tile in selectedTile.tileGroup:
            tile.mouseOffset = common.mySub(mouseLoc, tile.position)
            # The next two lines move all the tiles in a seleted group
            # of tiles to the top layer of the tiles
            tiles.remove(tile)
            tiles.append(tile)
    return selectedTiles, isDrag, selectedTile

# Recursively groups tiles which are extensionally connected with each
# other.  Basically the code runs, grouping individual tiles to each
# other, until there are no more tiles which are next to one of the
# tiles which is not already a part of the group.
def addNeighbors(tile, selectedTile):
    for side in tile.sides:
        if (side.isSnapped and side.adjSide.tile is not selectedTile and
                side.adjSide.tile not in tile.tileGroup):
            tile.tileGroup.append(side.adjSide.tile)
            side.adjSide.tile.tileGroup = tile.tileGroup
            addNeighbors(side.adjSide.tile, selectedTile)

# If two matching sides were found above in this function, this shifts
# the moving tiles into a snapped position with the nearby tiles
def snapTiles(selectedTile, snapdSide, adjSide):
    snapdTile = snapdSide.tile
    for tile in selectedTile.tileGroup:
        tile.groupOffset = common.mySub(tile.absPosition,
                snapdTile.absPosition)
    for tile in selectedTile.tileGroup:
        tile.matchCorner(snapdSide.corner,
                common.myAdd(adjSide.corner.getAbsPosition(),
                tile.groupOffset))
    snapdTile.adjTile = adjSide.tile
    snapdTile.adjTile.adjTile = snapdTile
    isSnapped = True
    return isSnapped, snapdTile, snapdSide

def unSnapAll(sidesToSnap):
    for side in sidesToSnap:
        side.adjSide.adjSide = None
        side.adjSide = None
    sidesToSnap = []
    snapdTile = None
    isSnapped = False
    isConflict = True
    return isSnapped, sidesToSnap, snapdTile, isConflict

# This determines if the two sides could potentially snap, and if so
# sets snapdSide and adjSide to these two sides, and sets isMatch to
# True
def findMatch(sideA, sideB, minDistance, isMatch, snapdSide, adjSide):
    # This block only runs if the two sides are of the same color, and
    # also neither side is already snapped to another tile.
    if (sideA.color == sideB.color and
            common.isInSquare(sideA.corner.getPosition(),
            sideB.corner.getPosition(), minDistance) and not sideB.isSnapped):
        # When this code is run on different combinations of sides, this
        # code makes sure to only set the closest two compatible sides
        # as the sides to be used for snapping.
        distance = common.getDistance(sideA.corner.getPosition(),
                sideB.corner.getPosition())
        if distance < minDistance:
            minDistance = distance
            snapdSide = sideA
            adjSide = sideB
            isMatch = True
    return minDistance, isMatch, snapdSide, adjSide

def addAreas(myCanvas, position, areasToCheck, grid, gridRes):
    for area in getAreasToCheck(position, grid, gridRes):
        if not area in areasToCheck:
            areasToCheck.append(area)

# For updating the scene
def update(myCanvas, inPlay, tiles, selectedTiles, mouseLoc, button, isUnClick,
        isClick, isScrollDown, isScrollUp, grid, gridRes,
        isDrag, selectedTile, palletBack, isSnapped, sidesToSnap,
        snapdTile, snapdSide, adjSide, isComputerTurn,
        clock, FPS, oldMouseLoc, windowSurface):
    # oldPositions keeps track of where tiles were before they were moved
    oldPositions = []
    # dirtyRects keeps track of parts of the screen that need to be
    # updated after drawing to the screen
    dirtyRects = []
    # determines whether either tiles which have been moved should be
    # re-drawn, or if all of the tiles should be re-drawn
    isDrawClicked = isDrawAll = False
    # isDrag keeps track of whether or not a tile is being dragged
    # around by the mouse
    if isUnClick:
        myCanvas.isMouseDown = myCanvas.isLDown = myCanvas.isRDown = \
                isClick = isDrag = False
    else:
        if button == myCanvas.RIGHT:
            myCanvas.isRDown = True
            myCanvas.isMouseDown = True
        elif button == myCanvas.LEFT:
            myCanvas.isLDown = True
            myCanvas.isMouseDown = True
    # isDeleted is set to true when one or more tiles has been deleted
    # on the current step
    isDeleted = False
    toDraws = []
    if isComputerTurn:
        inPlay, selectedTiles, selectedTile, isSnapped, sidesToSnap, \
                snapdTile = game.computerPlay(myCanvas, inPlay,
                selectedTiles, selectedTile, isSnapped, sidesToSnap, snapdTile,
                tiles, toDraws, grid, gridRes)
        clock.tick(1)
    else:
        clock.tick(FPS)
        # This function resizes the display if the user is scrolling
        grid, gridRes, palletBack, isDrawAll = scrollSize(myCanvas, tiles, grid,
                gridRes, palletBack, isScrollDown, isScrollUp, dirtyRects,
                isDrawAll, windowSurface)
        # This function checks if the user has clicked on the tile pallet.
        # If so, a tile is chosen from the pallet.  It also checks if the
        # user has clicked on a tile already on the canvas.  Either way it
        # sets the mouseOffset attribute for all of the selected tiles, which
        # hold the distance between the center of the tile and the mouse
        # location.  Right mouse clicks chose tile groups, left clicks
        # choose individual tiles.  Generally this gets the tiles ready to be
        # moved.
        selectedTiles, isDrawClicked, isDrag, selectedTile, = \
                checkers.checkClick(myCanvas, mouseLoc, tiles, selectedTiles,
                isClick, isDrawClicked, isDrag, selectedTile, grid,
                gridRes)
        # Checks if the mouse has unclicked, and if so, sets up tile groups
        # such that any snapped tiles are now in the same group.
        # Also changes which part of the tile grid they are now a part of.
        isDrawClicked, selectedTile, isSnapped, sidesToSnap, \
                snapdTile, snapdSide = checkers.checkUnclick(myCanvas, isUnClick,
                isClick, tiles, selectedTiles, isDrawClicked, oldPositions,
                dirtyRects, selectedTile, isSnapped, sidesToSnap,
                snapdTile, grid, gridRes, snapdSide)
        # Checks if tiles are currently over the tile pallet, and sets them
        # to turn red if and only if they are over it.  If there has been an
        # unclick and the tiles are over the pallet, they are deleted
        isDeleted = checkers.checkTrash(myCanvas, tiles, selectedTiles,
                oldPositions, isUnClick, dirtyRects, selectedTile, grid, gridRes,
                palletBack, isDeleted, windowSurface)
        #Sets the mouse offset on all the tiles if the background is dragged
        if not isDrag and isClick:
            for tile in tiles:
                tile.mouseOffset = common.mySub(mouseLoc, tile.position)
        # Things in this block only evaluate if there is both a mouse click,
        # and mouse movement since the last update
        if myCanvas.isMouseDown and mouseLoc != oldMouseLoc:
            # If a tile or tiles is being dragged, this determines where
            # they should be moved and also snaps or unsnaps them from other
            # tiles
            if isDrag:
                isDrawClicked, isSnapped, sidesToSnap, snapdTile, snapdSide, \
                        adjSide = movers.moveSome(myCanvas, mouseLoc, tiles,
                        selectedTiles, oldPositions, isUnClick, dirtyRects,
                        selectedTile, isSnapped, sidesToSnap, snapdTile,
                        palletBack, snapdSide, adjSide, grid, gridRes,
                        windowSurface)
            # This only evaluates if the background is being dragged and there
            # are one or more tiles.  It moves all of the movable tiles.
            elif len(tiles) > 0:
                isDrawAll = movers.moveAll(myCanvas, mouseLoc, tiles, grid,
                        gridRes, dirtyRects, isDrawAll, windowSurface)
    if isDeleted:
        selectedTile = None
    # Draws tiles which need to be drawn
    if isDrawClicked or isDrawAll:
        drawers.draw(myCanvas, tiles, toDraws, oldPositions, isUnClick,
                dirtyRects, isDrawClicked, isDrawAll, selectedTile, palletBack,
                isComputerPlay, grid, gridRes, windowSurface)
    if isUnClick:
        selectedTile = None
    oldMouseLoc = mouseLoc
    return (inPlay, selectedTiles, grid, gridRes, isDrag, selectedTile,
            palletBack, isSnapped, sidesToSnap, snapdTile,
            snapdSide, adjSide, oldMouseLoc, isComputerTurn)
