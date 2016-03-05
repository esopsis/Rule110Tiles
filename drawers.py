import pygame
import objects
import misc

# Draws the tile pallet, along with any initial tiles specified by the
# variable "tiles"
def initDraw(myCanvas, tiles, palletBack, windowSurface):
    windowSurface.fill(objects.Canvas.BACK_COLOR)
    for tile in tiles:
        tile.scalePosition(objects.Canvas.scale)
        tile.draw()
    drawPalletBack(palletBack, windowSurface)
    for tile in myCanvas.tilePallet:
        tile.draw()
    pygame.display.flip()

def drawPalletBack(palletBack, windowSurface):
    pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR, palletBack)

# This function makes sure tiles are drawn in order from the bottom tile
# to the top one
def drawInOrder(tiles, allTiles, windowSurface):
    for tile in sorted(tiles, key=lambda tile: allTiles.index(tile)):
        tile.draw()

#Objects should all be of the same type
def drawNearTiles(myCanvas, myObjects, allTiles, oldPositions, dirtyRects,
        grid, gridRes, windowSurface):
    areasToCheck = []
    tilesToDraw = []
    if len(myObjects) > 0 and isinstance(myObjects[0], objects.Tile):
        for tile in myObjects:
            misc.addAreas(myCanvas, tile.position, areasToCheck, grid, gridRes)
        for position in oldPositions:
            misc.addAreas(myCanvas, position, areasToCheck, grid, gridRes)
    for area in areasToCheck:
        tilesToDraw.extend(area)
    drawInOrder(tilesToDraw, allTiles, windowSurface)

# Draws the tile pallet
def drawPallet(myCanvas, palletBack, dirtyRects, windowSurface):
    drawPalletBack(palletBack, windowSurface)
    dirtyRects.append(palletBack)
    for tile in myCanvas.tilePallet:
        tile.draw()

# Draws groups of tiles in their new positions, and also draws any tiles
# which were behind those groups
def drawTileGroups(myCanvas, tiles, toDraws, oldPositions, isUnClick,
        dirtyRects, selectedTile, palletBack, isComputerPlay,
        grid, gridRes, windowSurface):
    if not isComputerPlay and selectedTile is not None:
        #TODO: extend or =?
        toDraws.extend(selectedTile.tileGroup)
    if len(toDraws) > 0:
        for tile in toDraws:
            tile.scalePosition(objects.Canvas.scale)
        # Draws any tiles which are behind moved tiles
        drawNearTiles(myCanvas, toDraws, tiles, oldPositions, dirtyRects,
                grid, gridRes, windowSurface)
        # Draws the tile pallet
        drawPallet(myCanvas, palletBack, dirtyRects, windowSurface)
        # Moved tiles are drawn on top of everything else
        for tile in toDraws:
            tile.draw()
            dirtyRects.append(tile.getRect())

# Draws tiles
def draw(myCanvas, tiles, toDraws, oldPositions, isUnClick, dirtyRects,
        isDrawClicked, isDrawAll, selectedTile, palletBack, isComputerPlay,
        grid, gridRes, windowSurface):
    # Draws groups of tiles in their new positions, and also draws any
    # tiles which were behind those groups
    if isDrawClicked:
        drawTileGroups(myCanvas, tiles, toDraws, oldPositions, isUnClick,
                dirtyRects, selectedTile, palletBack, grid, gridRes,
                windowSurface)
        # If the user unclicks, the tile pallet is re-drawn over
        # everythingn else to put it back on top
        if isUnClick:
            drawPallet(myCanvas, palletBack, dirtyRects, windowSurface)
        pygame.display.update(dirtyRects)
    # Re-draws everything, if all the tiles need to be re-drawn
    if isDrawAll:
        for tile in tiles:
            dirtyRects.append(tile.getRect())
            tile.draw()
        drawPalletBack(palletBack, windowSurface)
        dirtyRects.append(palletBack)
        for tile in myCanvas.tilePallet:
            tile.draw()
        pygame.display.update(dirtyRects)
