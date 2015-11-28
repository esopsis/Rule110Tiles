#TODO: change self.grid to grid
def checkArrangeInit(self, arrangeIndex, isArranging, activeRow,
        clickedTile, isArrange, groupGrid, tiles):
    if isArrange:
        '''
        self.activeTileRow = []
        for tile in tiles:
            self.activeTileRow.append(tile)
        '''
        #foo
        #print("in", clickedTile.tileGroup)
        groupGrid = GroupGrid(clickedTile.tileGroup)
        for tile in clickedTile.tileGroup:
            tiles.remove(tile)
            tiles.append(tile)
            tile.isToPlay = False
            tile.isInPlayGroup = True
        activeRow = groupGrid.grid[0]
        #print(activeRow)
        #self.activeTileRow = self.groupGrid[len(self.groupGrid) - 1]
        #print(groupGrid)
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
        self.playIcon.setPause()
        #self.playIcon.image = pygame.transform.smoothscale(
                #self.pauseImage, (self.playIcon.image.get_width(),
                #self.playIcon.image.get_height()))
        isArrange = False
        #foo
        #print("in", self.groupGrid)
        arrangeIndex = 1
    return groupGrid, arrangeIndex, isArranging, activeRow, isArrange

    #TODO: delete functions?
def isSideLoop(self, lOrR, offset, activeRow):
    if lOrR == "left":
        sign = -1
        i = 0
    elif lOrR == "right":
        sign = 1
        i = len(activeRow) - 1
    offsetPosition = x(activeRow[i].position) + \
            sign * activeRow[i].getSmallRect().width * offset
    if lOrR == "left":
        return offsetPosition < 0
    elif lOrR == "right":
        return offsetPosition > WIDTH

def checkBordersAdd(self, tile, checkedTiles, tileGroup, clickedTiles,
        clickedTile, isSnapped, sidesToSnap, snapdTile, toDraws, tiles,
        isArranging):
    isSnapped, sidesToSnap, snapdTile, isConflict = self.checkBordersSnap(
            [tile], checkedTiles, False, isSnapped, sidesToSnap, snapdTile,
            isArranging)
    if isConflict:
        tile.setImage(TileSet.w)
        tile.scaleImage(Canvas.scale)
    isSnapped, sidesToSnap, snapdTile, isConflict = self.checkBordersSnap(
            [tile], checkedTiles, False, isSnapped, sidesToSnap, snapdTile,
            isArranging)
    #foo
    #print(isConflict)
    if isConflict:
        #if tile.gridRow is not None:
            #self.grid[tile.gridRow][tile.gridCol].remove(tile)
        #tiles.pop()
        clickedTile = None
        clickedTiles = []
        #toDraws.pop()
    else:
        #foo
        #if tile.image is TileSet.rYB:
            #print("in")
        tiles.append(tile)
        self.toGrid(tile, self.grid, self.gridRes)
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
    return isConflict, isSnapped, sidesToSnap, snapdTile, clickedTile, \
            clickedTiles

def tryConnectNewTile(self, side, adjSide, toDraws, clickedTiles,
        clickedTile, isSnapped, sidesToSnap, snapdTile, tiles,
        isArranging):
    #print("in", tiles)
    isConflict = False
    if adjSide.isSnapped is False:
        #self.connectNewTile(side.corner, adjSide.corner.getAbsPosition(),
            #toDraws)
        tile = side.corner.tile
        #tiles.append(tile)
        tile.matchCorner(side.corner, adjSide.corner.getAbsPosition())
        tile.scalePosition(Canvas.scale)
        #self.toGrid(tile, self.grid, self.gridRes)
        clickedTile = tile
        clickedTiles = [clickedTile]
        #toDraws.append(tile)
        checkedTiles = []
        isConflict, isSnapped, sidesToSnap, snapdTile, clickedTile, \
                clickedTiles = self.checkBordersAdd(tile, checkedTiles,
                adjSide.tile.tileGroup, clickedTiles, clickedTile,
                isSnapped, sidesToSnap, snapdTile, toDraws, tiles,
                isArranging)
        #foo
        #print(isConflict)
        #foo
        #print(isConflict)
        #print(sidesToSnap)
    #print("in", tiles)
    return (isConflict, clickedTiles, clickedTile, isSnapped, sidesToSnap,
            snapdTile)

def objectToBin(self, myObject):
    if myObject is None or myObject.image is TileSet.w:
        return 0
    return 1
    
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
def objectToBin(self, myObject):
    if myObject is None or myObject.binary == 0:
        return 0
    elif myObject.binary == 1:
        return 1

def getEnd(self, array):
    for i in reversed(range(len(array))):
        if array[i] is not None:
            return i

def removeWhiteEnds(self, activeRow):
    end = self.getEnd(activeRow)
    for i in range(end + 1):
        if activeRow[i] is not None:
            return(activeRow[i:end + 1])

def checkAddLeft(self, activeRow, toDraws, clickedTiles, clickedTile,
        isSnapped, sidesToSnap, snapdTile, tiles, isArranging):
    #print("in")
    #print("in", activeRow)
    isConflict = False
    end = self.getEnd(activeRow)
    for i in range(end + 1):
        myObject = activeRow[i]
        #TODO: my object is not none instead for next line?
        if isinstance(myObject, Tile):
            newTile = None
            #TODO: set image instead of tile?
            if myObject.image is TileSet.bY:
                newTile = Tile(TileSet.rYB)
            elif (myObject.image is TileSet.rB or myObject.image is
                    TileSet.bR):
                newTile = Tile(TileSet.y)
            start = i
            if newTile is not None:
                #foo
                #print("in")
                #print("activerow", activeRow)
                isConflict, clickedTiles, clickedTile, isSnapped, \
                        sidesToSnap, snapdTile = self.tryConnectNewTile(
                        newTile.upperRight.rightSide,
                        myObject.upperLeft.leftSide, toDraws,
                        clickedTiles, clickedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, isArranging)
                #foo
                #print("lefttile", sidesToSnap)
                #toDraws.append(newTile)
                #foo
                #print("isConflict")
                if isConflict:
                    if newTile.image is TileSet.y:
                        image = TileSet.rYB
                    elif newTile.image is TileSet.rYB:
                        image = TileSet.y
                    #print("in", image is TileSet.y)
                    isConflict, clickedTiles, clickedTile, isSnapped, \
                        sidesToSnap, snapdTile = self.tryConnectNewTile(
                        Tile(image).upperRight.rightSide,
                        myObject.upperLeft.leftSide, toDraws,
                        clickedTiles, clickedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, isArranging)
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
    return (isConflict, activeRow, clickedTiles, clickedTile, isSnapped,
            sidesToSnap, snapdTile)

def checkAddRight(self, myObject, newTile):
    if (myObject.image is TileSet.bY or myObject.image is TileSet.y or
            myObject.image is TileSet.bR or myObject.image is TileSet.rYB):
        newTile = Tile(TileSet.rB)
    return newTile

def checkMerge(self, myObject, activeRow, i, toDraws):
    if ((myObject.image is TileSet.rY or myObject.image is TileSet.rB) and
            i + 1 < len(activeRow) and activeRow[i + 1] is not None and
            (activeRow[i + 1].image is TileSet.y or
            activeRow[i + 1].image is TileSet.rYB or
            activeRow[i + 1].image is TileSet.rY)):
        tileA = tileB = None
        if myObject.image is TileSet.rY:
            #foo
            #print("in")
            myObject.oldImage = myObject.image
            myObject.oldScaledImage = myObject.scaledImage
            myObject.setImage(TileSet.rYB)
            tileA = myObject
            #toDraws.append(myObject)
        elif myObject.image is TileSet.rB:
            myObject.oldImage = myObject.image
            myObject.oldScaledImage = myObject.scaledImage
            myObject.setImage(TileSet.bR)
            tileA = myObject
            #toDraws.append(myObject)
        if activeRow[i + 1].image is TileSet.y:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(TileSet.bY)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        elif activeRow[i + 1].image is TileSet.rYB:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(TileSet.bR)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        elif activeRow[i + 1].image is TileSet.rY:
            activeRow[i + 1].oldImage = myObject.image
            activeRow[i + 1].oldScaledImage = myObject.scaledImage
            activeRow[i + 1].setImage(TileSet.rB)
            tileB = activeRow[i + 1]
            #toDraws.append(self.activeRow[j + 1])
        toDraws = self.tryFinishSetImages([tileA, tileB], toDraws)
    return toDraws

def generateRow(self, activeRow, arrangeIndex, groupGrid):
    #foo
    #print("arrangein", arrangeIndex)
    #TODO: only do this if there isn't already a tile in the position!!
    isInGroupGrid = arrangeIndex < len(groupGrid.grid)
    leftTiles = []
    rightTiles = []
    #foo
    #print("in2")
    for i in range(len(activeRow) + 1):
        leftObject = getOrDefault(activeRow, i - 2, None)
        leftBin = self.objectToBin(leftObject)
        centerObject = getOrDefault(activeRow, i - 1, None)
        centerBin = self.objectToBin(centerObject)
        rightObject = getOrDefault(activeRow, i, None)
        rightBin = self.objectToBin(rightObject)
        #foo
        #print(leftBin, centerBin, rightBin)
        newBin = (self.rules["".join(map(str, [leftBin, centerBin,
                rightBin]))])
        #print(newBin)
        newTile = None
        if not (leftObject is None and centerObject is None and
                rightObject is None):
            if centerObject is None:
                if rightObject is not None:
                    newTile = Tile()
                    newTile.binary = newBin
                    newTile.matchCorner(newTile.upperRight,
                            rightObject.lower.getAbsPosition())
            else:
                newTile = Tile()
                newTile.binary = newBin
                newTile.matchCorner(newTile.upperLeft,
                        centerObject.lower.getAbsPosition())
                newTile.upperLeft.rightSide.adjSide = \
                        centerObject.lower.rightSide
            if newTile is not None:
                if isInGroupGrid:
                    xIndex = groupGrid.getTileIndex("x",
                            x(newTile.absPosition))
                    if xIndex < 0:
                        leftTiles.append(newTile)
                    elif xIndex >= len(groupGrid.grid[arrangeIndex]):
                        rightTiles.append(newTile)
                    else:
                        newSpace = groupGrid.grid[arrangeIndex][xIndex]
                        if newSpace is None:
                            groupGrid.grid[arrangeIndex][xIndex] = newTile
                else:
                    #TODO: change this to newrow maybe
                    leftTiles.append(newTile)
    if isInGroupGrid:
        #foo
        #print(leftTiles, groupGrid.grid[arrangeIndex], rightTiles)
        #print("in")
        #print(leftTiles, groupGrid.grid[arrangeIndex], rightTiles)
        newRow = leftTiles + groupGrid.grid[arrangeIndex] + rightTiles
        arrangeIndex += 1
        end = self.getEnd(newRow)
        for i in range(len(newRow), end + 1):
            if newRow[i] is not None:
                newRow = newRow[i:end + 1]
                break
    else:
        #print("in2")
        newRow = leftTiles
    #foo
    #print("newrow", newRow)
    return newRow, arrangeIndex

def setColor(self, newRow, tileIndex, activeRow, clickedTiles, clickedTile,
        isSnapped, sidesToSnap, snapdTile, toDraws, tiles, isArranging):
    #print(newRow, tileIndex)
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
    centerBin = self.objectToBin(centerObject)
    if tileIndex >= 1:
        leftBin = self.objectToBin(newRow[tileIndex - 1])
    else:
        leftBin = 0
    if tileIndex < len(newRow) - 1:
        rightBin = self.objectToBin(newRow[tileIndex + 1])
    else:
        rightBin = 0
    adjSide = centerObject.upperLeft.rightSide.adjSide
    if adjSide is None:
        topBin = 0
    else:
        topBin = self.objectToBin(adjSide.tile)
    #print(leftBin, centerBin, rightBin)
    #TODO: change equals's to is's
    image = None
    if centerBin:
        if leftBin:
            if rightBin:
                if topBin:
                    #if tileIndex >= 1:
                        #print(newRow[tileIndex + 1])
                    image = TileSet.bR
                else:
                    image = TileSet.bY
            else:
                #if i == len(newRow) - 1:
                #foo
                #print(isEnd, isRight)
                image = TileSet.rB
        else:
            if rightBin:
                if topBin:
                    image = TileSet.rYB
                else:
                    image = TileSet.y
            else:
                image = TileSet.rY
    else:
        image = TileSet.w
    #print(sidesToSnap)
    #Next few lines necessary?
    if image is not None:
        #if centerObject.isSnapped:
        isConflict = False
        #'''
        if centerObject.image is not Tile.delTile:
            #foo
            #print("in")
            #TODO: if image is not centerObject.image:
            oldImage = centerObject.image
            if not (oldImage is TileSet.bR and image is TileSet.bY):
                oldScaledImage = centerObject.scaledImage
                centerObject.setImage(image)
                #isConflict = False
                isConflict = self.checkBorders([centerObject])
                if isConflict:
                    centerObject.setImage(oldImage)
                    centerObject.scaledImage = oldScaledImage
                else:
                    centerObject.scaleImage(Canvas.scale)
                    toDraws.append(centerObject)
        #'''
        #if centerObject.image is Tile.delTile:
        centerObject.setImage(image)
        centerObject.scaleImage(Canvas.scale)
        #'''
        #print("in", sidesToSnap)
        #fooo
        #print(activeRow)
        isConflict, isSnapped, sidesToSnap, snapdTile, clickedTile, \
                clickedTiles = self.checkBordersAdd(centerObject, [],
                activeRow[-1].tileGroup, clickedTiles, clickedTile,
                isSnapped, sidesToSnap, snapdTile, toDraws, tiles,
                isArranging)
        #print(sidesToSnap)
        #'''
        #isConflict = False
        if isConflict:
            #print(newRow)
            newRow[newRow.index(centerObject)] = None
            #print(newRow)
        #else:
            #self.addToPlayGroup(centerObject, activeRow)
    return isConflict, clickedTile, clickedTiles

'''
def trySetColor(self):
    centerObject = newRow[tileIndex]
    assert centerObject is not None
    centerObject.oldImage = centerObject.image
    cetnerObject.oldScaledImage = centerObject.scaledImage
    isConflict = setColor(newRow, i)
    if isConflict:
'''

def setColors(self, newRow, clickedTiles, clickedTile, isSnapped,
        sidesToSnap, snapdTile, toDraws, tiles, isArranging, activeRow):
    indecesToCheck = []
    #foo
    #print(newRow)
    for i in range(len(newRow)):
        #move next line down into line after that
        centerObject = newRow[i]
        if centerObject.image is Tile.delTile:
            #foo
            #print("in2", newRow)
            isConflict, clickedTile, clickedTiles = self.setColor(newRow,
                    i, activeRow, clickedTiles, clickedTile, isSnapped,
                    sidesToSnap, snapdTile, toDraws, tiles, isArranging)
            #foo
            #print("in3", newRow)
            if newRow[i] is None:
                #print("in", i)
                indecesToCheck.append(i)
        #print(newRow)
            #foo
        #tilePosition =
        #newTile = Tile(image)
        #newRow.append(newTile)
        #tiles.append(newTile)
    #print("in", sidesToSnap)
    #'''
    neighborIndeces = []
    for i in indecesToCheck:
        if i - 1 > 0:
            neighborIndeces.append(i - 1)
        if i + 1 < len(newRow) - 1:
            neighborIndeces.append(i + 1)
        #foo
    #print(neighborIndeces)
    for i in set(neighborIndeces):
        if newRow[i] is not None:
            isConflict, clickedTile, clickedTiles = self.setColor(newRow,
                    i, activeRow, clickedTiles, clickedTile, isSnapped,
                    sidesToSnap, snapdTile, toDraws, tiles, isArranging)
        #assert not isConflict
    #foo
    #print(indecesToCheck)
    #print("in2", newRow)
    for i in indecesToCheck:
        myObject = newRow[i]
        leftTile = getOrDefault(newRow, i - 1, None)
        newTile = Tile(TileSet.w)
        if leftTile is not None:
            isConflict, clickedTiles, clickedTile, isSnapped, \
                    sidesToSnap, snapdTile = self.tryConnectNewTile(
                    newTile.upperLeft.leftSide,
                    leftTile.upperRight.rightSide, toDraws, clickedTiles,
                    clickedTile, isSnapped, sidesToSnap, snapdTile, tiles,
                    isArranging)
        else:
            rightTile = newRow[i + 1]
            isConflict, clickedTiles, clickedTile, isSnapped, \
                    sidesToSnap, snapdTile = self.tryConnectNewTile(
                    newTile.upperRight.rightSide,
                    rightTile.upperLeft.leftSide, toDraws, clickedTiles,
                    clickedTile, isSnapped, sidesToSnap, snapdTile, tiles,
                    isArranging)
        if not isConflict:
            newRow[i] = newTile
    #'''
    return isSnapped, sidesToSnap, snapdTile, clickedTile, clickedTiles
#'''
def halfSetImage(self, tile, image):
    tile.oldImage = tile.image
    tile.oldScaledImage = tile.scaledImage
    tile.setImage(image)
#'''
def tryFinishSetImages(self, tiles, toDraws):
    isConflict = self.checkBorders(tiles)
    if isConflict:
        for tile in tiles:
            tile.setImage(tile.oldImage)
            tile.scaledImage = tile.oldScaledImage
    else:
        for tile in tiles:
            tile.scaleImage(Canvas.scale)
            toDraws.append(tile)
    return toDraws

def doArranging(self, grid, groupGrid, arrangeIndex, mouseLoc, isClick, toDraws,
        dirtyRects, isDrawClicked, isArrangeStep, isArranging, activeRow,
        clickedTiles, clickedTile, oldClickedTiles, isSnapped, sidesToSnap,
        snapdTile, playCopy, oldPlayPosition, isUnSelectOld, tiles):
    isDrawClicked, isArrangeStep, isArranging = self.checkPause(mouseLoc,
            tiles, oldPlayPosition, dirtyRects, oldClickedTiles, playCopy, grid,
            isUnSelectOld, isDrawClicked, isArrangeStep, isArranging,
            activeRow)
    now = pygame.time.get_ticks()
    if isArranging and now - self.lastTick >= self.ARRANGE_TIME:
        #foo
        self.lastTick = now
        isArrangeStep = True
        #newRow = []
        #activeRowPrime = []
        #foo
        #print(self.activeRow)
        self.removeWhiteEnds(activeRow)
        '''
        isLeftConflict, activeRow, clickedTiles, clickedTile, isSnapped, \
                sidesToSnap, snapdTile = self.checkAddLeft(activeRow,
                toDraws, clickedTiles, clickedTile, isSnapped, sidesToSnap,
                snapdTile, tiles, isArranging
        '''
        #print("in2")
        #print(sidesToSnap)
        #isRightConflict = False
        for i in range(len(activeRow)):
            myObject = activeRow[i]
            isLast = i == len(activeRow) - 1
            #newTile = None
            #if isLast:
                #self.activeRow.append(myObject)
                #newTile = self.checkAddRight(myObject, newTile)
            if not isLast and isinstance(myObject, Tile):
                toDraws = self.checkMerge(myObject, activeRow, i, toDraws)
                #self.connectNewTile(newTileA
                #self.activeRow.append(myObject)
            #TODO: try moving this stuff into previous if block
            #print(sidesToSnap)
            '''
            if newTile is not None:
                isRightConflict, clickedTiles, clickedTile, isSnapped, \
                        sidesToSnap, snapdTile = self.tryConnectNewTile(
                        newTile.upperLeft.leftSide,
                        myObject.upperRight.rightSide, toDraws,
                        clickedTiles, clickedTile, isSnapped, sidesToSnap,
                        snapdTile, tiles, isArranging)
                if not isRightConflict:
                    #self.addToPlayGroup(newTile, activeRow)
                    #toDraws.append(newTile)
                    activeRow.append(newTile)
            '''
            #print(sidesToSnap)
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
        newRow, arrangeIndex = self.generateRow(activeRow, arrangeIndex,
                groupGrid)
        #print("newrow", newRow)
        #nextRow = groupGrid.grid[arrangeIndex]
        #for i in range(len(activeRow) + 1):
        #print(sidesToSnap)
        isSnapped, sidesToSnap, snapdTile, clickedTile, clickedTiles = \
                self.setColors(newRow, clickedTiles, clickedTile,
                isSnapped, sidesToSnap, snapdTile, toDraws, tiles,
                isArranging, activeRow)
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
        isDrawClicked = True
    else:
        isArrangeStep = False
    #self.arrangeTicks += 1
    return (arrangeIndex, isDrawClicked, isArrangeStep, isArranging,
            activeRow, clickedTiles, clickedTile, isSnapped, sidesToSnap,
            snapdTile)

