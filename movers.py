import pygame
import common
#import canvas
import objects
import checkers
import misc

def moveUnSnap(canvas, mouseLoc, selectedTiles, selectedTile,
        oldselectedTiles, sidesToSnap, tiles):
    for tile in selectedTiles:
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))
    if canvas.isLDown:
        gapCount = 0
        for i in range(-1, len(selectedTile.sides) - 1):
            #print(self.selectedTile.sides[i].isSnapped)
            if (selectedTile.sides[i].isSnapped and not
                    selectedTile.sides[i + 1].isSnapped):
                gapCount += 1
        #print(gapCount)
        #Only runs if the tile being unsapped is holding two groups of
        #tiles together.  If this happens, the tile group needs to be
        #split into two or more new tile groups.
        if gapCount >= 2:
            #print("in")
            for side in selectedTile.sides:
                if side.isSnapped:
                    side.adjSide.tile.tileGroup = []
            for side in selectedTile.sides:
                if side.isSnapped:
                    for sideB in selectedTile.sides:
                        if (sideB.isSnapped and sideB.adjSide.tile not in
                                side.adjSide.tile.tileGroup):
                            side.adjSide.tile.tileGroup = [side.adjSide.tile]
                            misc.addNeighbors(side.adjSide.tile, selectedTile)
        selectedTile.unSnap()
        tiles.remove(selectedTile)
        tiles.append(selectedTile)
    for side in sidesToSnap:
        side.adjSide = None
    sidesToSnap = []
    snapdTile = None
    isSnapped = False
    oldselectedTiles = []
    oldselectedTiles.extend(selectedTile.tileGroup)
    #for tile in self.selectedTile.tileGroup:
        #self.oldselectedTiles.append(tile)
    isUnSelectOld = True
    return (oldselectedTiles, isSnapped, sidesToSnap, snapdTile, isUnSelectOld)
    
#Unsnaps tile if leftclick, moves group if rightclick.
def moveUnSnappable(canvas, mouseLoc, selectedTiles, selectedTile,
        oldselectedTiles, isSnapped, sidesToSnap, snapdTile, isUnSelectOld,
        tiles):
    #print("in")
    for side in snapdTile.sides:
        #print("in2")
        '''
        if side.adjSide is not None:
            print(myAdd(mySub(
                mouseLoc, self.snapdTile.mouseOffset),
                side.corner.getOffset()),
                side.adjSide.corner.getPosition())
        '''
        #print(side.adjSide)
        #print(self.snapdTile)
        if (side.adjSide is not None and common.getDistance(common.myAdd(
                common.mySub(mouseLoc, snapdTile.mouseOffset),
                side.corner.getOffset()), side.adjSide.corner.getPosition()) >
                objects.Canvas.SNAP_DISTANCE * objects.Canvas.scale + 1):
            #print("in2")
            oldselectedTiles, isSnapped, sidesToSnap, snapdTile, \
                    isUnSelectOld = moveUnSnap(canvas, mouseLoc,
                    selectedTiles, selectedTile, oldselectedTiles, sidesToSnap,
                    tiles)
            break
    return (oldselectedTiles, isSnapped, sidesToSnap, snapdTile, isUnSelectOld)

def noSnapMove(mouseLoc, selectedTiles):
    #foo
    #print("in", selectedTiles)
    for tile in selectedTiles:
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))

def moveSnappable(canvas, mouseLoc, checkedTiles, selectedTiles,
        selectedTile, palletBack, isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide,
        grid, gridRes, isArranging):
    #adjTile = None
    #print("in")
    minDistance = objects.Canvas.SNAP_DISTANCE * objects.Canvas.scale
    isMatch = False
    #print("in")
    #foo
    #print(selectedTile.tileGroup)
    for tileA in selectedTile.tileGroup:
        #'''
        if tileA.isFree():
            areasToCheck = misc.getAreasToCheck(tileA.position, grid, gridRes)
            for sideA in tileA.sides:
                if not sideA.isSnapped:
                    for area in areasToCheck:
                        #print(area.row, area.col)
                        for tileB in area:
                            if tileB.isFree() and tileB not in checkedTiles:
                                sideB = tileB.getSide(sideA.adjType)
                                #print(sideA.sideGroup.adjGroup.sides)
                                #print("sideA ", sideA.corner.getAbsPosition())
                                #print(sideB.isSnapped)
                                minDist, isMatch, snapdSide, adjSide = \
                                        misc.findMatch(sideA, sideB,
                                        minDistance, isMatch, snapdSide, adjSide)
    if isMatch:
        #isDrawClicked = True
        checkedTiles.append(adjSide.tile)
        #foo
        #print("in2")
        isSnapped, snapdTile, snapdSide = misc.snapTiles(selectedTile,       
                snapdSide, adjSide)
        #print(selectedTile.getSmallRect(), self.palletBack)
        if selectedTile.getSmallRect().colliderect(palletBack):
        #print(self.selectedTile.getSmallRect(), self.palletBack)
            #foo
            #print("in")
            isSnapped, sidesToSnap, snapdTile, isConflict = \
                    misc.unSnapAll(sidesToSnap)
        else:
            isSnapped, sidesToSnap, snapdTile, isConflict = \
                    checkers.checkBordersSnap(canvas, mouseLoc,
                    selectedTiles, checkedTiles, grid, gridRes, True, isSnapped, sidesToSnap,
                    snapdTile, isArranging, selectedTiles)
        if isConflict:
            isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide = \
                    moveSnappable(canvas, mouseLoc, checkedTiles,
                    selectedTiles, selectedTile, palletBack, isSnapped, sidesToSnap,
                    snapdTile, snapdSide, adjSide, grid, gridRes, isArranging)
    else:
        noSnapMove(mouseLoc, selectedTiles)
    #'''
    #self.noSnapMove()
    #return isDrawClicked
    return isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide

def tryMoveAll(tiles, grid, gridRes, dirtyRects, isDrawAll):
    #print(tiles)
    #foo
    #print("in3", tiles)
    for tile in tiles:
        misc.toGrid(tile, grid, gridRes)
        #for tile in backTiles:
            #tile.draw()
        pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                tile.getLargeRect())
        dirtyRects.append(tile.getLargeRect())
        #foo
        #print("in2", tile.mouseOffset)
        tile.setPosition(common.mySub(mouseLoc, tile.mouseOffset))
        #print("in2", tile, tile.position)
        #tile.resize(Canvas.scale)
        tile.scalePosition(objects.Canvas.scale)
        isDrawAll = True
    return isDrawAll

def moveSome(canvas, mouseLoc, tiles, selectedTiles, oldPositions, isUnClick,
        dirtyRects, selectedTile, oldselectedTiles, isSnapped, sidesToSnap,
        snapdTile, palletBack, isUnSelectOld, snapdSide, adjSide, grid, gridRes, isArranging,
        windowSurface):
    #oldPos = self.selectedTile.position
    #print("in")
    #foo
    #print("in", selectedTiles)
    isDrawClicked = True
    for tile in selectedTiles:
        oldPositions.append(tile.position)
        #print(tile.getLargeRect())
        pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                tile.getLargeRect())
        dirtyRects.append(tile.getLargeRect())
    '''
    selectedTile.isSnapped = False
    for side in selectedTile.sides:
        if side.isSnapped:
            selectedTile.isSnapped = True
            break
    '''
    if selectedTile.isSnapped() and canvas.isLDown:
        #print("in")
        snapdTile = selectedTile
    #foo
    #print("movesnap ", self.selectedTile.isToDel)
    if snapdTile is not None and (canvas.isLDown or snapdTile.adjTile not in
            snapdTile.tileGroup):
        #foo
        #print("in2")
        oldselectedTiles, isSnapped, sidesToSnap, snapdTile, isUnSelectOld = \
                moveUnSnappable(canvas, mouseLoc, selectedTiles,
                selectedTile, oldselectedTiles, isSnapped, sidesToSnap,
                snapdTile, isUnSelectOld, tiles)
    elif selectedTile.isToDel:
        #foo
        #print("in3")
        noSnapMove(mouseLoc, selectedTiles)
    else:
        #foo
        #print("in")
        isSnapped, sidesToSnap, snapdTile, snapdSide, adjSide = moveSnappable(
                canvas, mouseLoc, [], selectedTiles, selectedTile, palletBack, isSnapped,
                sidesToSnap, snapdTile, snapdSide, adjSide, grid, gridRes, isArranging)
    #print(self.isSnapped, isUnClick)
    #print(type(tile.mouseOffset))
    #print(self.selectedTile.absPosition)
    #self.selectedTile.resize(Canvas.scale)
    #print("in2")
    return (isDrawClicked, oldselectedTiles, isSnapped, sidesToSnap, snapdTile,
            isUnSelectOld, snapdSide, adjSide)

def movePlayIcon(canvas, dirtyRects, tiles, activeRow, selectedTile,
        oldselectedTiles, playCopy, isUnSelectOld, mouseLoc):
    pygame.draw.rect(canvas.windowSurface, objects.Canvas.BACK_COLOR,
            playCopy.getRect())
    dirtyRects.append(playCopy.getRect())
    oldPlayPosition = [playCopy.position]
    playCopy.position = common.mySub(mouseLoc, playCopy.mouseOffset)
    playPoint = common.myAdd(mouseLoc, (canvas.playIcon.getRect().width / 2,
            0))
    minDist = canvas.tilePallet[0].getSmallRect().height / 2
    toPlay = None
    for tile in reversed(tiles):
        #if tile.getSmallRect().collidepoint(myAdd(mouseLoc,
                #(self.playIcon.image.get_width() / 2, 0))):
        if common.isInSquare(playPoint, tile.position, minDist):
            distance = common.getDistance(playPoint, tile.position)
            if distance < minDist:
                minDist = distance
                toPlay = tile
    '''
    if toPlay is not None and len(self.activeTileRow) > 0:
        print(toPlay.tileGroup is self.activeTileRow[0].tileGroup)
    else:
        print("no active tile row")
    '''
    #foo
    #print("toPlay", toPlay)
    #print("len", len(self.activeTileRow) > 0, toPlay)
    if activeRow is not None and (toPlay is None or
            toPlay.tileGroup is not activeRow[0].tileGroup):
        #foo
        #print("in5")
        #isDrawClicked = True
        isUnSelectOld = True
        oldselectedTiles = []
        #foo
        #print("in", len(self.activeTileRow[0].tileGroup))
        for tile in activeRow[0].tileGroup:
            tile.isToPlay = False
            oldselectedTiles.append(tile)
        #foo
        #print("isdraws")
        #for tile in tiles: 
            #print(tile.isToPlay)
        #print("in2")
        #for tile in self.activeTileRow[0].tileGroup:
            #print tile.isToPlay
        activeRow = None
        selectedTile = None
        #print(self.oldselectedTiles)
    if toPlay is not None and (activeRow is None or
            toPlay.tileGroup is not activeRow[0].tileGroup):
        #foo
        #print("in4", toPlay)
        for tile in toPlay.tileGroup:
            tile.isToPlay = True
            tiles.remove(tile)
            tiles.append(tile)
        selectedTile = toPlay
        #isDrawClicked = True
        activeRow = toPlay.tileGroup
    #foo
    #print("in", isDrawClicked)
    isDrawClicked = True
    return (isDrawClicked, activeRow, selectedTile, oldselectedTiles,
            oldPlayPosition, isUnSelectOld)
