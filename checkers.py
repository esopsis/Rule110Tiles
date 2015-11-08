import pygame
import common
import objects
import drawers
import movers
import misc

# Checks the tile pallet to see if a new tile needs to be added,
# if so, sets selectedTile as that tile
def checkPallet(myCanvas, tiles, mouseLoc, isDrag, selectedTile):
    for tile in myCanvas.tilePallet:
        if (not isDrag and common.isInSquare(mouseLoc, tile.position,
                tile.radius) and common.getDistance(mouseLoc, tile.position) <
                tile.radius):
            newTile = objects.Tile(myCanvas, tile.image)
            newTile.setPosition(tile.position)
            tiles.append(newTile)
            newTile.mouseOffset = common.mySub(mouseLoc, tile.position)
            selectedTile = newTile
            isDrag = True
    return isDrag, selectedTile

# Checks for clicked tiles to be moved.
def checkClick(myCanvas, mouseLoc, tiles, selectedTiles, isClick,
        isDrawClicked, isDrag, selectedTile, grid, gridRes):
    if isClick:
        # Checks the tile pallet to see if a new tile needs to be added,
        # if so, sets selectedTile as that tile
        isDrag, selectedTile = checkPallet(myCanvas, tiles, mouseLoc, isDrag,
                selectedTile)
        # Sets selected tile or selected tiles and mouse offsets for
        # tile/tiles which have been selected.  Right clicks select
        # groups of tiles, left clicks select individual tiles.
        selectedTiles, isDrag, selectedTile, = misc.setMouseOffset(myCanvas,
                tiles, selectedTiles, mouseLoc, isDrag, selectedTile, grid,
                gridRes)
        if selectedTile is not None:
            isDrawClicked = True
    return (selectedTiles, isDrawClicked, isDrag, selectedTile)

# Checks if the mouse has unclicked, and if so, sets up tile groups such
# that any snapped tiles are now in the same group.  Also changes which
# part of the tile grid they are now a part of
def checkUnclick(myCanvas, isUnClick, isClick, tiles, selectedTiles,
        isDrawClicked, oldPositions, dirtyRects, selectedTile, isSnapped,
        sidesToSnap, snapdTile, grid, gridRes, snapdSide):
    # This block only evaluates if the user has unclicked, and not also
    # re-clicked during the update
    if isUnClick and not isClick:
        # This block only evaluates if a tile or group of tiles have
        # been positioned to snap together in a previous update
        if isSnapped:
            # This checks each side from the selected tile group which
            # is to be snapped to another tile.  It then checks whether
            # or not the tile it is to be snapped to is already a part
            # of its tile group, and if not, adds each tile in its tile
            # group to the tile group of the tile it is snapping to, and
            # then sets its own tile group to the tile group of the tile
            # it is snapping to.  Basically the two tile groups merge.
            # This is set up to work even if one tile group is
            # connecting simultaniously to two  or more
            # other disconnected tile groups.
            for side in sidesToSnap:
                if side.adjSide.tile not in selectedTile.tileGroup:
                    for tile in selectedTile.tileGroup:
                        side.adjSide.tile.tileGroup.append(tile)
                        tile.tileGroup = side.adjSide.tile.tileGroup
                side.isSnapped = side.adjSide.isSnapped = True
        if selectedTile is not None:
            isDrawClicked = True
            for tile in selectedTiles:
                oldPositions.append(tile.position)
                misc.toGrid(myCanvas, tile, grid, gridRes)
        isSnapped = False
        snapdSide = None
        ajdSide = None
        snapdTile = None
        sidesToSnap = []
    return (isDrawClicked, selectedTile, isSnapped, sidesToSnap, snapdTile,
            snapdSide)

# Checks if tiles are currently over the tile pallet, and sets them to
# turn red if and only if they are over it.  If there has been an
# unclick and the tiles are over the pallet, they are deleted
def checkTrash(myCanvas, tiles, selectedTiles, oldPositions, isUnClick,
            dirtyRects, selectedTile, grid, gridRes, palletBack, isDeleted,
            windowSurface):
    # This block only runs if a tile has been selected with the mouse,
    # and the right mouse button is down or the selected tile is not
    # snapped to anything.  The reason for these checks is that,
    # if the right mouse button is not down, and the tile is currently
    # snapped to something, then the user is selecting an individual
    # tile which is snapped to some other tiles.  An individually
    # selected tile, as opposed to a selected group of tiles, should not
    # be deleted unless it is currently unsnapped from all other tiles.
    if selectedTile is not None and (myCanvas.isRDown or not
            selectedTile.isSnapped()):
        # This block only runs if the selected tile is overlapping with
        # the tile pallet
        if selectedTile.getRect().colliderect(palletBack):
            # Each tile in the tile group of the selected tile has
            # isToDel set to true, so that they are set to be deleted if
            # they unclick
            for tile in selectedTiles:
                tile.isToDel = True
            # Only runs if the user unclicks while the selected tile is
            # overlapping with the tile pallet
            if isUnClick:
                # Each tile is deleted, and a white patch is drawn where
                # it was
                for tile in selectedTiles:
                    if tile.gridRow is not None:
                        grid[tile.gridRow][tile.gridCol].remove(tile)
                    tiles.pop()
                    pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                            tile.getRect())
                    dirtyRects.append(tile.getRect())
                # Tiles which are in adjacent parts of the grid to tiles
                # which were deleted, are re-drawn over any white
                # patches where the tile was deleted
                drawers.drawNearTiles(myCanvas, selectedTiles, tiles,
                        oldPositions, dirtyRects, grid, gridRes, windowSurface)
                isDeleted = True
        # If the tile was set to be deleted, but is no longer over the
        # tile pallet, isToDel is set to false on it
        else:
            if selectedTile.isToDel:
                for tile in selectedTile.tileGroup:
                    tile.isToDel = False
        return isDeleted

# Checks whether the borders of two snapping tiles in two groups of
# tiles are compatible to snap
def checkBorderSnap(mouseLoc, sideA, sideB, checkedTiles, isDragging,
        isSnapped, sidesToSnap, snapdTile, isConflict, selectedTiles):
    if common.isInSquare(sideA.corner.getAbsPosition(),
            sideB.corner.getAbsPosition(), 1):
        if not isConflict:
            if (sideA.color == sideB.color and not
                    sideA.isSnapped and not sideB.isSnapped):
                sideA.adjSide = sideB
                sideB.adjSide = sideA
                # If colors match and both sides aren't snapped, they
                # are added to a list of sides to snap if there is an
                # unclick
                sidesToSnap.append(sideA)
            else:
                if isDragging:
                    movers.noSnapMove(mouseLoc, selectedTiles)
                    isSnapped, sidesToSnap, snapdTile, isConflict = \
                            misc.unSnapAll(sidesToSnap)
                isConflict = True
        # If there has been a conflict with another tile in the group of
        # the tile who's side is being checked, then the tile is just
        # added to a list of tiles which have already been checked
        checkedTiles.append(sideB.tile)
    return isSnapped, sidesToSnap, snapdTile, isConflict

# Checks whether all the borders of two snapping tile groups are
# compatible.  If so, it sets them to snap when there is an unclick, if
# not, it moves them back to where they were before an attempt was made
# to snap them together.
def checkBordersSnap(myCanvas, mouseLoc, tilesToSnap, checkedTiles, grid,
        gridRes, isDragging, isSnapped, sidesToSnap, snapdTile, selectedTiles):
    isConflict = False
    for tileA in tilesToSnap:
        if tileA.isFree():
            areasToCheck = misc.getAreasToCheck(tileA.position, grid, gridRes)
            for sideA in tileA.sides:
                if not sideA.isSnapped:
                    for area in areasToCheck:
                        for tileB in area:
                            if tileA is not tileB:
                                sideB = tileB.getSide(sideA.adjType)
                                isSnapped, sidesToSnap, snapdTile, \
                                        isConflict = checkBorderSnap(mouseLoc,
                                        sideA, sideB, checkedTiles, isDragging,
                                        isSnapped, sidesToSnap, snapdTile,
                                        isConflict, selectedTiles)
    return isSnapped, sidesToSnap, snapdTile, isConflict
