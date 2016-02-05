import pygame
import common
import objects
import checkers
import drawers
import misc

#TODO: change self.grid to grid
def checkArrangeInit(canvas, arrangeIndex, isArranging, activeRow,
        selectedTile, isArrange, groupGrid, tiles):
    if isArrange:
        '''
        self.activeTileRow = []
        for tile in tiles:
            self.activeTileRow.append(tile)
        '''
        #foo
        #print("in", selectedTile.tileGroup)
        groupGrid = objects.GroupGrid(selectedTile.tileGroup)
        for tile in selectedTile.tileGroup:
            tiles.remove(tile)
            tiles.append(tile)
            tile.isToPlay = False
            tile.isInPlayGroup = True
        activeRow = groupGrid.grid[0]
        #print(activeRow)
        #self.activeTileRow = self.groupGrid[len(self.groupGrid) - 1]
        #print("grouopGrid", groupGrid)
        #self.activeBinRow = [0, 0]
        #for tile in activeRow[0].tileGroup:
            #tile.isToPlay = False
            #tile.isInPlayGroup = True
        '''
        for tile in self.activeTileRow:
            #tile.isToPlay = False
            if tile.image == TileSet.w:
                self.activeBinRow.append(0)
            else:
                self.activeBinRow.append(1)
        '''
        isArranging = True
        #self.activeBinRow.append(0)
        canvas.playIcon.setPause()
        #self.playIcon.image = pygame.transform.smoothscale(
                #self.pauseImage, (self.playIcon.image.get_width(),
                #self.playIcon.image.get_height()))
        isArrange = False
        #foo
        #print("in", self.groupGrid)
        arrangeIndex = 1
    return groupGrid, arrangeIndex, isArranging, activeRow, isArrange

def checkPause(canvas, mouseLoc, isClick, tiles, oldPlayPosition, dirtyRects,
        oldSelectedTiles, playCopy, grid, gridRes, isUnSelectOld, isDrawClicked,
        isArrangeStep, isArranging, activeRow):
    if isClick:
        if canvas.playIcon.getRect().collidepoint(mouseLoc):
            #foo
            canvas.playIcon.setPlay()
            pygame.draw.rect(canvas.windowSurface, objects.Canvas.BACK_COLOR,
                canvas.playIcon.getRect())
            dirtyRects.append(canvas.playIcon.getRect())
            drawers.drawNearTiles(canvas, [canvas.playIcon], tiles,
                    oldPlayPosition, dirtyRects, oldSelectedTiles, playCopy,
                    grid,
                    gridRes, isUnSelectOld, canvas.windowSurface)
            if len(activeRow) > 0:
                for tile in activeRow[-1].tileGroup:
                    tile.isInPlayGroup = False
            isDrawClicked = True
            isArrangeStep = isArranging = False
    return isDrawClicked, isArrangeStep, isArranging

    #TODO: delete functions?
def isSideLoop(lOrR, offset, activeRow):
    if lOrR == "left":
        sign = -1
        i = 0
    elif lOrR == "right":
        sign = 1
        i = len(activeRow) - 1
    offsetPosition = canvas.x(activeRow[i].position) + \
            sign * activeRow[i].getSmallRect().width * offset
    if lOrR == "left":
        return offsetPosition < 0
    elif lOrR == "right":
        return offsetPosition > WIDTH

def checkBordersAdd(canvas, tile, checkedTiles, tileGroup, selectedTiles,
        selectedTile, isSnapped, sidesToSnap, snapdTile, toDraws, tiles, grid,
        gridRes, isArranging):
    isSnapped, sidesToSnap, snapdTile, isConflict = checkers.checkBordersSnap(
            canvas, None, [tile], checkedTiles, grid, gridRes, False,
            isSnapped, sidesToSnap, snapdTile, isArranging, selectedTiles)
    if isConflict:
        tile.setImage(objects.TileSet.w)
        tile.scaleImage(objects.Canvas.scale)
    isSnapped, sidesToSnap, snapdTile, isConflict = checkers.checkBordersSnap(
            canvas, None, [tile], checkedTiles, grid, gridRes, False,
            isSnapped, sidesToSnap, snapdTile, isArranging, selectedTiles)
    #foo
    #print(isConflict)
    if isConflict:
        #if tile.gridRow is not None:
            #self.grid[tile.gridRow][tile.gridCol].remove(tile)
        #tiles.pop()
        selectedTile = None
        selectedTiles = []
        #toDraws.pop()
    else:
        #foo
        #if tile.image is TileSet.rYB:
            #print("in")
        tiles.append(tile)
        misc.toGrid(canvas, tile, grid, gridRes)
        toDraws.append(tile)
        #self.addToPlayGroup(tile, tiles)
        #'''
        tile.isInPlayGroup = True
        #print(activeRow)
        #if len(activeRow) > 0
        #foo
        #print(activeRow[len(activeRow) - 1])
        #print(activeRow[len(activeRow) - 1].tileGroup)
        #tileGroup = activeRow[len(activeRow) - 1].tileGroup
        #tileGroup = tileAddingTo.tileGroup
        tileGroup.append(tile)
        tile.tileGroup = tileGroup
        #'''
    return isConflict, isSnapped, sidesToSnap, snapdTile, selectedTile, \
            selectedTiles

def tryConnectNewTile(canvas, side, adjSide, toDraws, selectedTiles,
        selectedTile, isSnapped, sidesToSnap, snapdTile, tiles, grid, gridRes,
        isArranging):
    #print("in", tiles)
    isConflict = False
    if adjSide.isSnapped is False:
        #self.connectNewTile(side.corner, adjSide.corner.getAbsPosition(),
            #toDraws)
        tile = side.corner.tile
        #tiles.append(tile)
        tile.matchCorner(side.corner, adjSide.corner.getAbsPosition())
        tile.scalePosition(objects.Canvas.scale)
        #self.toGrid(tile, self.grid, self.gridRes)
        selectedTile = tile
        selectedTiles = [selectedTile]
        #toDraws.append(tile)
        checkedTiles = []
        isConflict, isSnapped, sidesToSnap, snapdTile, selectedTile, \
                selectedTiles = checkBordersAdd(canvas, tile, checkedTiles,
                adjSide.tile.tileGroup, selectedTiles, selectedTile,
                isSnapped, sidesToSnap, snapdTile, toDraws, tiles, grid,
                gridRes,
                isArranging)
        #foo
        #print(isConflict)
        #foo
        #print(isConflict)
        #print(sidesToSnap)
    #print("in", tiles)
    return (isConflict, selectedTiles, selectedTile, isSnapped, sidesToSnap,
            snapdTile)

'''
def objectToBin(myObject):
    if myObject is None or myObject.image is objects.TileSet.w:
        return 0
    return 1
'''
    
'''
def objectToBin(self, array, i):
    DEFAULT = 0
    myObject = self.getOrDefault(array, i, DEFAULT)
    #foo
    #print(myObject)
    if (myObject == DEFAULT or myObject is None or myObject.image is
            TileSet.w):
        return DEFAULT
    return 1
'''
def objectToBin(myObject):
    if myObject is None or myObject.binary == 0:
        return 0
    elif myObject.binary == 1:
        return 1

def getEnd(array):
    for i in reversed(range(len(array))):
        if array[i] is not None:
            return i

def removeWhiteEnds(activeRow):
    end = getEnd(activeRow)
    for i in range(end + 1):
        if activeRow[i] is not None:
            return(activeRow[i:end + 1])

def checkAddLeft(canvas, activeRow, toDraws, selectedTiles, selectedTile,
        isSnapped, sidesToSnap, snapdTile, tiles, grid, gridRes, isArranging):
    #print("in")
    #print("in", activeRow)
    isConflict = False
    end = getEnd(activeRow)
    for i in range(end + 1):
        myObject = activeRow[i]
        #TODO: my object is not none instead for next line?
        if isinstance(myObject, objects.Tile):
            newTile = None
            #TODO: set image instead of tile?
            if myObject.image is objects.TileSet.bY:
                newTile = objects.Tile(canvas, objects.TileSet.rYB)
            elif (myObject.image is objects.TileSet.rB or myObject.image is
                    objects.TileSet.bR):
                newTile = objects.Tile(canvas, objects.TileSet.y)
            start = i
            if newTile is not None:
                #foo
                #print("in")
                #print("activerow", activeRow)
                isConflict, selectedTiles, selectedTile, isSnapped, \
                        sidesToSnap, snapdTile = tryConnectNewTile(canvas, 
                        newTile.upperRight.rightSide,
                        myObject.upperLeft.leftSide, toDraws,
                        selectedTiles, selectedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, grid, gridRes, isArranging)
                #foo
                #print("lefttile", sidesToSnap)
                #toDraws.append(newTile)
                #foo
                #print("isConflict")
                if isConflict:
                    if newTile.image is objects.TileSet.y:
                        image = objects.TileSet.rYB
                    elif newTile.image is objects.TileSet.rYB:
                        image = objects.TileSet.y
                    #print("in", image is TileSet.y)
                    isConflict, selectedTiles, selectedTile, isSnapped, \
                        sidesToSnap, snapdTile = tryConnectNewTile(canvas,
                        objects.Tile(canvas, image).upperRight.rightSide,
                        myObject.upperLeft.leftSide, toDraws,
                        selectedTiles, selectedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, grid, gridRes, isArranging)
                    #foo
                    #print("in", isConflict)
                if not isConflict:
                    #self.addToPlayGroup(newTile, activeRow)
                    if i > 0:
                        #print("in2")
                        activeRow[i - 1] = newTile
                        start = i - 1
                    else:
                        #print("in3")
                        activeRow = [newTile] + activeRow
                        #i = i - 1
                        end = end + 1
                        #start = i
            break
    #foo
    #print("in", self.activeRow)
    #activeRowTemp = activeRow
    #activeRow = []
    #for j in range(i, end + 1):
        #activeRow.append(activeRowTemp[j])
    activeRow = activeRow[start:end + 1]
    return (isConflict, activeRow, selectedTiles, selectedTile, isSnapped,
            sidesToSnap, snapdTile)

def checkAddRight(canvas, myObject, newTile):
    if (myObject.image is objects.TileSet.bY or myObject.image is objects.TileSet.y or
            myObject.image is objects.TileSet.bR or myObject.image is objects.TileSet.rYB):
        newTile = objects.Tile(canvas, objects.TileSet.rB)
    return newTile

def checkMerge(myObject, activeRow, i, toDraws):
    if ((myObject.image is objects.TileSet.rY or myObject.image is
            objects.TileSet.rB) and
            i + 1 < len(activeRow) and activeRow[i + 1] is not None and
            (activeRow[i + 1].image is objects.TileSet.y or
            activeRow[i + 1].image is objects.TileSet.rYB or
            activeRow[i + 1].image is objects.TileSet.rY)):
        tileA = tileB = None
        if myObject.image is objects.TileSet.rY:
            #foo
            #print("in")
            myObject.oldImage = myObject.image
            myObject.oldScaledImage = myObject.scaledImage
            myObject.setImage(objects.TileSet.rYB)
            tileA = myObject
            #toDraws.append(myObject)
        elif myObject.image is objects.TileSet.rB:
            myObject.oldImage = myObject.image
            myObject.oldScaledImage = myObject.scaledImage
            myObject.setImage(objects.TileSet.bR)
            tileA = myObject
            #toDraws.append(myObject)
        if activeRow[i + 1].image is objects.TileSet.y:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(objects.TileSet.bY)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        elif activeRow[i + 1].image is objects.TileSet.rYB:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(objects.TileSet.bR)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        elif activeRow[i + 1].image is objects.TileSet.rY:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(objects.TileSet.rB)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        toDraws = tryFinishSetImages([tileA, tileB], toDraws)
    return toDraws

def isSideLoop(lOrR, offset, activeRow, canvas):
    if lOrR == "left":
        sign = -1
        i = 0
    elif lOrR == "right":
        sign = 1
        i = len(activeRow) - 1
    offsetPosition = common.x(activeRow[i].position) + sign * \
            activeRow[i].getSmallRect().width * offset
    if lOrR == "left":
        return offsetPosition < 0
    elif lOrR == "right":
        return offsetPosition > canvas.WIDTH

def generateRow(canvas, activeRow, arrangeIndex, isLeftLoop, isLeftPrimeLoop, isRightLoop, isRightPrimeLoop, groupGrid):
    #foo
    #print("arrangein", arrangeIndex)
    #TODO: only do this if there isn't already a tile in the position!!
    isInGroupGrid = arrangeIndex < len(groupGrid.grid)
    leftTiles = []
    rightTiles = []
    #foo
    #print(activeRow)
    #for tile in activeRow:
        #print("activeRow", tile, tile.position)
    #print("in2")
    end = len(activeRow)
    if isLeftLoop:
        start = 0
    else:
        start = -1
        if isLeftPrimeLoop:
            end -= 1
            #print("in")
        elif isRightLoop:
            end -= 1
            #print("in")
        elif isRightPrimeLoop:
            start = 0
            # print("in2")
    #foo
    #print(start, end)
    for i in range(start, end):
        if isLeftPrimeLoop or isRightPrimeLoop:
            leftObject = common.loopGet(activeRow, i - 1)
            centerObject = common.loopGet(activeRow, i)
            rightObject = common.loopGet(activeRow, i + 1)
        else:
            leftObject = common.getOrDefault(activeRow, i - 1, None)
            centerObject = common.getOrDefault(activeRow, i, None)
            rightObject = common.getOrDefault(activeRow, i + 1, None)
        leftBin = objectToBin(leftObject)
        centerBin = objectToBin(centerObject)
        rightBin = objectToBin(rightObject)
        #foo
        #print(leftBin, centerBin, rightBin)
        newBin = (canvas.rules["".join(map(str, [leftBin, centerBin,
                rightBin]))])
        #print(newBin)
        newTile = None  
        if not (leftObject is None and centerObject is None and
                rightObject is None):
            if i == -1:
                newTile = objects.Tile(canvas)
                newTile.binary = newBin
                if isLeftLoop:
                    newTile.matchCorner(newTile.upperLeft, centerObject.lower.getAbsPosition())
                else:
                    newTile.matchCorner(newTile.upperRight, rightObject.lower.getAbsPosition())
            elif centerObject is None:
                if rightObject is not None:
                    newTile = objects.Tile(canvas)
                    #TODO: move the two newBin setters down
                    newTile.binary = newBin
                    newTile.matchCorner(newTile.upperRight,
                            rightObject.lower.getAbsPosition())
            else:
                newTile = objects.Tile(canvas)
                newTile.binary = newBin
                newTile.matchCorner(newTile.upperLeft,
                        centerObject.lower.getAbsPosition())
                newTile.upperLeft.rightSide.adjSide = \
                        centerObject.lower.rightSide
            if newTile is not None:
                newTile.isAddedRowNewTile = True
                #foo
                #print("")
                #print(newTile, newTile.position)
                if isInGroupGrid:
                    xIndex = groupGrid.getTileIndex("x",
                            common.x(newTile.absPosition))
                    #print("xIndex", xIndex)
                    #print("groupGrid", groupGrid.grid[arrangeIndex])
                    if xIndex < 0:
                        leftTiles.append(newTile)
                    elif xIndex >= len(groupGrid.grid[arrangeIndex]):
                        rightTiles.append(newTile)
                    else:
                        newSpace = groupGrid.grid[arrangeIndex][xIndex]
                        if newSpace is None:
                            #pass
                            groupGrid.grid[arrangeIndex][xIndex] = newTile
                else:
                    #TODO: change this to newrow maybe
                    leftTiles.append(newTile)
    #foo
    #for row in groupGrid.grid:
        #print(row)
    #print("next")
    if isInGroupGrid:
        #foo
        #print("in")
        #print(leftTiles, groupGrid.grid[arrangeIndex], rightTiles)
        #for tile in groupGrid.grid[arrangeIndex] + rightTiles:
            #print("newTiles", tile, tile.position)
        newRow = leftTiles + groupGrid.grid[arrangeIndex] + rightTiles
        arrangeIndex += 1
        end = getEnd(newRow)
        for i in range(end + 1):
            if newRow[i] is not None:
                newRow = newRow[i:end + 1]
                break
    else:
        #print("in2")
        newRow = leftTiles
    #foo
    #print("newrow", newRow)
    return newRow, arrangeIndex

def setColor(canvas, newRow, tileIndex, activeRow, selectedTiles, selectedTile,
        isSnapped, sidesToSnap, snapdTile, toDraws, tiles, isLeftLoop, isLeftPrimeLoop,
        isLeftDoublePrimeLoop, isRightLoop, isRightDoublePrimeLoop, grid,
        gridRes, isArranging):
    #foo
    #print("in", newRow, tileIndex)
    centerObject = newRow[tileIndex]
    #isStart = tileIndex == 0
    #isEnd = tileIndex == len(newRow) - 1
    '''
    isLeft = isRight = False
    if (centerObject.image is TileSet.bY or centerObject.image
            is TileSet.rB or centerObject.image is TileSet.bR):
        isLeft = True
    if (centerObject.image is TileSet.bY or centerObject.image is
            TileSet.y or centerObject.image is TileSet.rYB or
            centerObject.image is TileSet.bR):
        isRight = True
    '''
    centerBin = objectToBin(centerObject)
    if isLeftDoublePrimeLoop or isRightDoublePrimeLoop:
        leftBin = objectToBin(common.loopGet(newRow, tileIndex - 1))
        rightBin = objectToBin(common.loopGet(newRow, tileIndex + 1))
    else:
        leftBin = objectToBin(common.getOrDefault(newRow, tileIndex - 1, None))
        rightBin = objectToBin(common.getOrDefault(newRow, tileIndex + 1,
                None))
    #isRightLoop = False
    if tileIndex == 0 and (isLeftPrimeLoop and not isLeftLoop or isRightLoop):
        topBin = objectToBin(activeRow[-1])
    else:
        topSide = centerObject.upperLeft.rightSide.adjSide
        if topSide is None:
            topBin = 0
        else:
            topBin = objectToBin(topSide.tile)
    #print(leftBin, centerBin, rightBin)
    #TODO: change equals's to is's
    image = None
    if centerBin:
        if leftBin:
            if rightBin:
                if topBin:
                    #if tileIndex >= 1:
                        #print(newRow[tileIndex + 1])
                    image = objects.TileSet.bR
                else:
                    image = objects.TileSet.bY
            else:
                #if i == len(newRow) - 1:
                #foo
                #print(isEnd, isRight)
                image = objects.TileSet.rB
        else:
            if rightBin:
                if topBin:
                    image = objects.TileSet.rYB
                else:
                    image = objects.TileSet.y
            else:
                image = objects.TileSet.rY
    else:
        image = objects.TileSet.w
    #print(sidesToSnap)
    #TODO: Next few lines necessary?
    if image is not None:
        #if centerObject.isSnapped:
        isConflict = False
        #'''
        if centerObject.image is not objects.Tile.delTile:
            #foo
            #print("in")
            #TODO: if image is not centerObject.image:
            oldImage = centerObject.image
            if not (oldImage is objects.TileSet.bR and image is
                    objects.TileSet.bY):
                oldScaledImage = centerObject.scaledImage
                centerObject.setImage(image)
                #isConflict = False
                isConflict = checkers.checkBorders([centerObject])
                if isConflict:
                    centerObject.setImage(oldImage)
                    centerObject.scaledImage = oldScaledImage
                else:
                    centerObject.scaleImage(objects.Canvas.scale)
                    toDraws.append(centerObject)
        #'''
        if centerObject.image is objects.Tile.delTile:
            centerObject.setImage(image)
            centerObject.scaleImage(objects.Canvas.scale)
            isConflict, isSnapped, sidesToSnap, snapdTile, selectedTile, \
                    selectedTiles = checkBordersAdd(canvas, centerObject, [],
                    activeRow[-1].tileGroup, selectedTiles, selectedTile,
                    isSnapped, sidesToSnap, snapdTile, toDraws, tiles, grid,
                    gridRes, isArranging)
        #print(sidesToSnap)
        #'''
        #isConflict = False
        if isConflict:
            #print(newRow)
            newRow[newRow.index(centerObject)] = None
            #print(newRow)
        #else:
            #self.addToPlayGroup(centerObject, activeRow)
        #foo
        #print("in2", newRow)
    return isConflict, selectedTile, selectedTiles

'''
def trySetColor(self):
    centerObject = newRow[tileIndex]
    assert centerObject is not None
    centerObject.oldImage = centerObject.image
    cetnerObject.oldScaledImage = centerObject.scaledImage
    isConflict = setColor(newRow, i)
    if isConflict:
'''

def setColors(canvas, newRow, selectedTiles, selectedTile, isSnapped,
        sidesToSnap, snapdTile, toDraws, tiles, isArranging, isLeftLoop,
        isLeftPrimeLoop, isLeftDoublePrimeLoop, isRightLoop, isRightDoublePrimeLoop, grid, gridRes, activeRow):
    indecesToCheck = []
    #foo
    #for tile in activeRow:
        #print("activeRow", tile, tile.position)
    #for tile in newRow:
        #print("newRow", tile, tile.position)
    #print("")
    #print("in3", newRow)
    for i in range(len(newRow)):
        #TODO: move next line down into line after that
        centerObject = newRow[i]
        #TODO: Change to .isNewTile
        if centerObject is not None and centerObject.isAddedRowNewTile:
            #foo
            #print("in2")
            isConflict, selectedTile, selectedTiles = setColor(canvas, newRow,
                    i, activeRow, selectedTiles, selectedTile, isSnapped,
                    sidesToSnap, snapdTile, toDraws, tiles, isLeftLoop,
                    isLeftPrimeLoop, isLeftDoublePrimeLoop, isRightLoop, isRightDoublePrimeLoop, grid, gridRes, isArranging)
            if newRow[i] is None:
                indecesToCheck.append(i)
    #print("in4", newRow)
    #'''
    #TODO: Do I still need this neighbor checking stuff?
    neighborIndeces = []
    for i in indecesToCheck:
        if i - 1 > 0:
            neighborIndeces.append(i - 1)
        if i + 1 < len(newRow) - 1:
            neighborIndeces.append(i + 1)
        #foo
    #print(neighborIndeces)
    for i in set(neighborIndeces):
        if newRow[i] is not None and newRow[i].isAddedRowNewTile:
            isConflict, selectedTile, selectedTiles = setColor(canvas, newRow,
                    i, activeRow, selectedTiles, selectedTile, isSnapped,
                    sidesToSnap, snapdTile, toDraws, tiles, isLeftLoop,
                    isLeftPrimeLoop, isLeftDoublePrimeLoop, isRightLoop, isRightDoublePrimeLoop, grid, gridRes, isArranging)
        #assert not isConflict
    #foo
    #print(indecesToCheck)
    #print("in2", newRow)
    for i in indecesToCheck:
        myObject = newRow[i]
        leftTile = common.getOrDefault(newRow, i - 1, None)
        newTile = objects.Tile(canvas, objects.TileSet.w)
        if leftTile is not None:
            isConflict, selectedTiles, selectedTile, isSnapped, \
                    sidesToSnap, snapdTile = tryConnectNewTile(canvas, 
                    newTile.upperLeft.leftSide,
                    leftTile.upperRight.rightSide, toDraws, selectedTiles,
                    selectedTile, isSnapped, sidesToSnap, snapdTile, tiles,
                    grid, gridRes, isArranging)
        else:
            rightTile = newRow[i + 1]
            isConflict, selectedTiles, selectedTile, isSnapped, \
                    sidesToSnap, snapdTile = tryConnectNewTile(canvas, 
                    newTile.upperRight.rightSide,
                    rightTile.upperLeft.leftSide, toDraws, selectedTiles,
                    selectedTile, isSnapped, sidesToSnap, snapdTile, tiles,
                    grid, gridRes, isArranging)
        if not isConflict:
            newRow[i] = newTile
    #'''
    return isSnapped, sidesToSnap, snapdTile, selectedTile, selectedTiles
#'''
def halfSetImage(tile, image):
    tile.oldImage = tile.image
    tile.oldScaledImage = tile.scaledImage
    tile.setImage(image)
#'''
def tryFinishSetImages(tiles, toDraws):
    isConflict = checkers.checkBorders(tiles)
    if isConflict:
        for tile in tiles:
            tile.setImage(tile.oldImage)
            tile.scaledImage = tile.oldScaledImage
    else:
        for tile in tiles:
            tile.scaleImage(objects.Canvas.scale)
            toDraws.append(tile)
    return toDraws

def isRightCloser(self):
    return x(self.activeTileRow[0].position) > WIDTH - \
            x(self.activeTileRow[len(self.activeTileRow) - 1].position)

def doArranging(canvas, grid, gridRes, groupGrid, arrangeIndex, mouseLoc,
        isClick, toDraws, dirtyRects, isDrawClicked, isArrangeStep,
        isArranging, activeRow, selectedTiles, selectedTile, oldSelectedTiles,
        isSnapped, sidesToSnap, snapdTile, playCopy, oldPlayPosition,
        isUnSelectOld, tiles):
    isDrawClicked, isArrangeStep, isArranging = checkPause(canvas, mouseLoc,
            isClick, tiles, oldPlayPosition, dirtyRects, oldSelectedTiles,
            playCopy, grid, gridRes, isUnSelectOld, isDrawClicked,
            isArrangeStep, isArranging, activeRow)
    now = pygame.time.get_ticks()
    if isArranging and now - canvas.lastTick >= objects.Canvas.ARRANGE_TIME:
        #foo
        canvas.lastTick = now
        isArrangeStep = True
        #newRow = []
        #activeRowPrime = []
        #foo
        #print(self.activeRow)
        #TODO: This is supposed to return something?
        activeRow = removeWhiteEnds(activeRow)
        '''
        isLeftConflict, activeRow, selectedTiles, selectedTile, isSnapped, \
                sidesToSnap, snapdTile = checkAddLeft(canvas, activeRow,
                toDraws, selectedTiles, selectedTile, isSnapped, sidesToSnap,
                snapdTile, tiles, grid, gridRes, isArranging)
        '''
        #print("in2")
        #print(sidesToSnap)
        #isRightConflict = False
        for i in range(len(activeRow)):
            myObject = activeRow[i]
            isLast = i == len(activeRow) - 1
            #newTile = None
            #if isLast:
                #newTile = checkAddRight(canvas, myObject, newTile)
            if not isLast and isinstance(myObject, objects.Tile):
                toDraws = checkMerge(myObject, activeRow, i, toDraws)
                #self.connectNewTile(newTileA
                #activeRow.append(myObject)
            #TODO: try moving this stuff into previous if block
            #print(sidesToSnap)
            '''
            if newTile is not None:
                isRightConflict, selectedTiles, selectedTile, isSnapped, \
                        sidesToSnap, snapdTile = tryConnectNewTile(canvas,
                        newTile.upperLeft.leftSide,
                        myObject.upperRight.rightSide, toDraws,
                        selectedTiles, selectedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, grid, isArranging)
                if not isRightConflict:
                    #self.addToPlayGroup(newTile, activeRow)
                    #toDraws.append(newTile)
                    activeRow.append(newTile)
            #print(sidesToSnap)
            '''
        '''
        tile = None
        if isLeftConflict:
            tile = activeRow[0]
            if isRightConflict:
                self.halfSetImage(tile, TileSet.rY)
            else:
                if tile.image is TileSet.bR:
                    self.halfSetImage(tile,TileSet.rYB)
                elif tile.image is TileSet.bY:
                    self.halfSetImage(tile,TileSet.y)
                elif tile.image is TileSet.rB:
                    self.halfSetImage(tile, TileSet.rY)
        elif isRightConflict:
            tile = activeRow[-1]
            if tile.image is bR or tile.image is bY:
                self.halfSetImage(tile, TileSet.rB)
            else:
                self.halfSetImage(tile, TileSet.rY)
        if tile is not None:
            toDraws = self.tryFinishSetImages([tile], toDraws)
        '''
        #foo
        #print("in", sidesToSnap)
        #print("acriverow", activeRow)
        #for row in groupGrid.grid:
            #print("groupGrid", row)
        isLeftLoop = isSideLoop("left", 1, activeRow, canvas)
        isRightLoop = isSideLoop("right", 1, activeRow, canvas)
        isLeftPrimeLoop = isSideLoop("left", 1.5, activeRow, canvas)
        isRightPrimeLoop = isSideLoop("right", 1.5, activeRow, canvas)
        isLeftDoublePrimeLoop = isSideLoop("left", 2, activeRow, canvas)
        isRightDoublePrimeLoop = isSideLoop("right", 2, activeRow, canvas)
        #print(isRightLoop, isRightPrimeLoop)
        newRow, arrangeIndex = generateRow(canvas, activeRow, arrangeIndex,
                isLeftLoop, isLeftPrimeLoop, isRightLoop, isRightPrimeLoop, groupGrid)
        #print("newrow", newRow)
        #nextRow = groupGrid.grid[arrangeIndex]
        #for i in range(len(activeRow) + 1):
        #print(sidesToSnap)
        isSnapped, sidesToSnap, snapdTile, selectedTile, selectedTiles = \
                setColors(canvas, newRow, selectedTiles, selectedTile,
                isSnapped, sidesToSnap, snapdTile, toDraws, tiles,
                isArranging, isLeftLoop, isLeftPrimeLoop, isLeftDoublePrimeLoop, isRightLoop, isRightDoublePrimeLoop, grid, gridRes, activeRow)
        #side.tile.neighbors.append(side.adjSide.tile)
        #self.snapSides()
        #foo
        #print(sidesToSnap)
        #print("left", sidesToSnap)
        for side in sidesToSnap:
            side.isSnapped = side.adjSide.isSnapped = True
        '''
        print("in")
        for side in sidesToSnap:
            print(side.isSnapped, side)
        for tile in tiles:
            if tile.image is TileSet.bY:
                for side in tile.sides:
                    print(side.isSnapped)
        '''
        sidesToSnap = []
        #print("in", newRow)
        activeRow = newRow
        #foo
        #print("in", self.activeRow)
        #self.activeBinRow = newBinRow
        for myObject in activeRow:
            if myObject is not None:
                myObject.isAddedRowNewTile = False
        isDrawClicked = True
    else:
        isArrangeStep = False
    #self.arrangeTicks += 1
    return (arrangeIndex, isDrawClicked, isArrangeStep, isArranging,
            activeRow, selectedTiles, selectedTile, isSnapped, sidesToSnap,
            snapdTile)

