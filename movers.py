import pygame
import common
import objects
import checkers
import misc

# Unsnaps a tile or group of tiles
def moveUnSnap(myCanvas, mouseLoc, selectedTiles, selectedTile, sidesToSnap,
        tiles):
    # Moves the tiles back to the position they would be if not snapped
    for tile in selectedTiles:
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))
    # The next block only runs if the left mouse button is down, meaning
    # only one tile is being selected
    if myCanvas.isLDown:
        gapCount = 0
        for i in range(-1, len(selectedTile.sides) - 1):
            if (selectedTile.sides[i].isSnapped and not
                    selectedTile.sides[i + 1].isSnapped):
                gapCount += 1
        # This block only runs if the tile being unsapped is holding two
        # groups of tiles together.  If this happens, the tile group
        # needs to be and is split into two or more new tile groups.
        if gapCount >= 2:
            # Ungroups all tiles
            for side in selectedTile.sides:
                if side.isSnapped:
                    side.adjSide.tile.tileGroup = []
            # Regroups tiles into new seperate groups.  For each side of
            # the single tile that is being unsnapped, this checks
            # whether there is another tile snapped to the unsnapping
            # tile which should be part of a seperate group from that
            # other tile.  If so, that seperate tile is recursively
            # grouped with other tiles extensionally connected to it
            for side in selectedTile.sides:
                if side.isSnapped:
                    for sideB in selectedTile.sides:
                        if (sideB.isSnapped and sideB.adjSide.tile not in
                                side.adjSide.tile.tileGroup):
                            side.adjSide.tile.tileGroup = [side.adjSide.tile]
                            misc.addNeighbors(side.adjSide.tile, selectedTile)
        selectedTile.unSnap()
    for side in sidesToSnap:
        side.adjSide = None
    sidesToSnap = []
    snapdTile = None
    isSnapped = False
    return (isSnapped, sidesToSnap, snapdTile)

# Checks whether tiles which have snapped can unsnap, and if so, unsnaps
# them.  If a group of tiles is being dragged, and has snapped to
# another group of tiles, they can still unsnap as long as the user has
# not already unclicked, causing the snapped tile groups to merge
def moveUnSnappable(myCanvas, mouseLoc, selectedTiles, selectedTile, isSnapped,
        sidesToSnap, snapdTile, tiles):
    # Checks each side of one of the tiles which is snapped but can
    # potentially still be unsnapped.  If the distance between this
    # tile and another tile is enough, the tiles unsnap
    for side in snapdTile.sides:
        if (side.adjSide is not None and common.getDistance(common.myAdd(
                common.mySub(mouseLoc, snapdTile.mouseOffset),
                side.corner.getOffset()), side.adjSide.corner.getPosition()) >
                objects.Canvas.SNAP_DISTANCE * objects.Canvas.scale + 1):
            isSnapped, sidesToSnap, snapdTile = moveUnSnap(myCanvas, mouseLoc,
                    selectedTiles, selectedTile, sidesToSnap, tiles)
            break
    return (isSnapped, sidesToSnap, snapdTile)

# Moves tiles to wherever the mouse drags them to (they don't snap to
# other tiles)
def noSnapMove(mouseLoc, selectedTiles):
    for tile in selectedTiles:
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))

# Moves tiles which can snap to other tiles, and makes sure to only snap
# a tile or tile group to the nearest tile/tile group
def moveSnappable(myCanvas, mouseLoc, checkedTiles, selectedTiles,
        selectedTile, palletBack, isSnapped, sidesToSnap, snapdTile, snapdSide,
        adjSide, grid, gridRes):
    # minDistance will end up storing the distance to the nearest tile/
    # tile group
    minDistance = objects.Canvas.SNAP_DISTANCE * objects.Canvas.scale
    # isMatch keeps track of whether or not there are two tiles who's
    # facing sides match, and which are close enough together to
    # potentially snap
    isMatch = False
    # This next block basically looks at all the moving tiles, and
    # determines whether or not any of them are close enough, and the
    # right kind of side, to potentially snap together, and if so,
    # sets those to sides to snapdSide and adjSide
    for tileA in selectedTile.tileGroup:
        # This block only runs if there are sides to the tile which are
        # not already snapped to other tiles
        if tileA.isFree():
            # This gets areas near each tile to reduce the number of
            # tiles which need to be checked for potential snapping
            areasToCheck = misc.getAreasToCheck(tileA.position, grid, gridRes)
            for sideA in tileA.sides:
                if not sideA.isSnapped:
                    for area in areasToCheck:
                        for tileB in area:
                            # If a side of a moving tile is not snapped,
                            # and a nearby tile has unsnapped sides,
                            # and the nearby tile has not already been
                            # found to be unsnappable (not in
                            # checkedTiles) then this block evaluates
                            if tileB.isFree() and tileB not in checkedTiles:
                                # This sets sideB to the side of the
                                # nearby tile adjacent to the moving
                                # tile
                                sideB = tileB.getSide(sideA.adjType)
                                # This determines if the two sides
                                # could potentially snap, and if so
                                # sets snapdSide and adjSide to these
                                # two sides, and sets isMatch to True.
                                # In the end it only applies to a
                                # nearest snappable tile.
                                minDist, isMatch, snapdSide, adjSide = \
                                        misc.findMatch(sideA, sideB,
                                        minDistance, isMatch, snapdSide,
                                        adjSide)
    if isMatch:
        checkedTiles.append(adjSide.tile)
        # If two matching sides were found above in this function, then
        # the below function shifts the moving tiles into a snapped
        # position with the nearby tiles
        isSnapped, snapdTile, snapdSide = misc.snapTiles(selectedTile,
                snapdSide, adjSide)
        # If, by shifting towards other tiles to snap, a tile group
        # would overlap with the tile pallet, the tile group is then
        # moved back to where it would have been before shifting, and
        # isConflict is set to true.  This is to prevent tiles from
        # snapping to other tiles when they would also be moving into
        # a position over the tile pallet which usually means the tiles
        # would be set to be deleted
        if selectedTile.getRect().colliderect(palletBack):
            isSnapped, sidesToSnap, snapdTile, isConflict = \
                    misc.unSnapAll(sidesToSnap)
        # All that is known at this point is that two tiles match and
        # could potentially snap.  Below, the code checks whether or not
        # shifting tiles to a snapped position would cause OTHER tiles
        # to not match with each other, in which case these tiles are
        # moved back to where they were before they were snapped.  Any
        # tiles which were found to not be able to snap are added to
        # checkedTiles.  This moveSnappable function is then called
        # recursively to check for possible matches which are not the
        # NEAREST potential matches, until all nearby tiles have been
        # checked for possible snapping.  If all the sides match, the
        # sides are set up to be snapped whenever the user unclicks.
        else:
            isSnapped, sidesToSnap, snapdTile, isConflict = \
                    checkers.checkBordersSnap(myCanvas, mouseLoc,
                    selectedTiles, checkedTiles, grid, gridRes, True,
                    isSnapped, sidesToSnap, snapdTile, selectedTiles)
        if isConflict:
            isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide = \
                    moveSnappable(myCanvas, mouseLoc, checkedTiles,
                    selectedTiles, selectedTile, palletBack, isSnapped,
                    sidesToSnap, snapdTile, snapdSide, adjSide, grid, gridRes)
    # If there were no sets of tiles nearby in which all sides matched,
    # the dragged tiles simply move to where they are dragged
    else:
        noSnapMove(mouseLoc, selectedTiles)
    return isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide

# Moves all of the tiles on the canvas.  Also finds their new positions
# in the tile grid.
def moveAll(myCanvas, mouseLoc, tiles, grid, gridRes, dirtyRects, isDrawAll,
        windowSurface):
    for tile in tiles:
        misc.toGrid(myCanvas, tile, grid, gridRes)
        pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                tile.getRect())
        dirtyRects.append(tile.getRect())
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))
        tile.scalePosition(objects.Canvas.scale)
        isDrawAll = True
    return isDrawAll

# If a tile or tiles is being dragged, this determines where they should
# be moved and also snaps or unsnaps them from other tiles
def moveSome(myCanvas, mouseLoc, tiles, selectedTiles, oldPositions, isUnClick,
        dirtyRects, selectedTile, isSnapped, sidesToSnap, snapdTile,
        palletBack, snapdSide, adjSide, grid, gridRes, windowSurface):
    isDrawClicked = True
    # Draws a white area over where the tile was, and adds its old
    # position to a list
    for tile in selectedTiles:
        oldPositions.append(tile.position)
        pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                tile.getRect())
        dirtyRects.append(tile.getRect())
    # Checks whether the clicked tile is snapped to another tile
    if selectedTile.isSnapped() and myCanvas.isLDown:
        snapdTile = selectedTile
    # This block only runs if the left mouse button is being held down
    # over a tile which is snapped to another tile, or if a group of
    # tiles is being moved, has just snapped to another tile or tile
    # group, but has not merged with them due to an unclick yet.
    # Basically it runs if there are tiles which are to be unsnapped
    # from other tiles, and unsnaps them.
    if snapdTile is not None and (myCanvas.isLDown or snapdTile.adjTile not in
            snapdTile.tileGroup):
        # Figures out how to move tiles which can potentially unsnap
        # from other tiles
        isSnapped, sidesToSnap, snapdTile, = moveUnSnappable(myCanvas,
                mouseLoc, selectedTiles, selectedTile, isSnapped, sidesToSnap,
                snapdTile, tiles)
    # If a tile is set to be deleted, it should not snap to anything.
    elif selectedTile.isToDel:
        noSnapMove(mouseLoc, selectedTiles)
    # Moves tiles which can snap to other tiles, and does any necessary
    # snapping
    else:
        isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide = moveSnappable(
                myCanvas, mouseLoc, [], selectedTiles, selectedTile,
                palletBack, isSnapped, sidesToSnap, snapdTile, snapdSide,
                adjSide, grid, gridRes)
    return (isDrawClicked, isSnapped, sidesToSnap, snapdTile, snapdSide,
            adjSide)
