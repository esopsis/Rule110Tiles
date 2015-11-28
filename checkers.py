#TODO: is isunselectold needed?
import pygame
import common
import objects
import drawers
import movers
import misc
import copy

def checkPallet(canvas, tiles, mouseLoc, isDrag, selectedTile, fromPallet):
        #print("in")
    for tile in canvas.tilePallet:
        '''
        screenLocation = (x(tile.position) - WIDTH / 2 +
                tile.scaledImage.get_width() / 2, y(tile.position) -
                HEIGHT / 2 + tile.scaledImage.get_height() / 2)
        '''
        #if tile.image == rB:
            #print(getDistance(mouseLoc, screenLocation))
        #fooo
        #print(isDrag, common.isInSquare(mouseLoc, tile.position,
                #tile.radius), common.getDistance(mouseLoc, tile.position) <
                #tile.radius)
        if (not isDrag and common.isInSquare(mouseLoc, tile.position,
                tile.radius) and common.getDistance(mouseLoc, tile.position) <
                tile.radius):
            #newTile = copy.copy(tile)
            #newTile.isMovable = True
            newTile = objects.Tile(canvas, tile.image)
            #print(tile.position)
            newTile.setPosition(tile.position)
            #print(newTile.position)
            #newTile.resize(Canvas.scale)
            #tile.scalePosition(Canvas.scale)
            #print("in", newTile.position)
            tiles.append(newTile)
            #print(tiles)
            fromPallet = newTile
            newTile.mouseOffset = common.mySub(mouseLoc, tile.position)
            #print(newTile.mouseOffset)
            selectedTile = newTile
            #foo
            #print(selectedTile)
            #self.selectedTiles = [newTile]
            isDrag = True
            #return newTile
            '''
            if self.selectedTile is None:
                print("None")
            else:
                print(self.selectedTile.position)
            '''
            #test = Tile(tile.image, screenLocation)
        #print(isUnClick, isinstance(self.fromPallet, Tile))
        #print(getDistance(self.fromPallet.position, screenLocation))
    return isDrag, selectedTile, fromPallet

def checkTrash(canvas, tiles, selectedTiles, oldPositions, isUnClick,
            dirtyRects, selectedTile, oldselectedTiles, playCopy, grid, gridRes, palletBack,
            isUnSelectOld, isDeleted, windowSurface):
    if selectedTile is not None and (selectedTile.isToDel or
            (canvas.isRDown or not selectedTile.isSnapped())):
        #print("in")
    #if (self.selectedTile is not None and not (self.isLDown and
            #self.selectedTile.isSnapped)):
        #foo
        #print("trash", selectedTile.getSmallRect(), self.palletBack)
        if selectedTile.getSmallRect().colliderect(palletBack):
            #print("in")
            #print("in", self.isLDown, self.selectedTile.isSnapped)
            for tile in selectedTiles:
                tile.isToDel = True
            #print("in2 ", isUnClick)
            if isUnClick:
                #print("in3")
                #self.checkTrash(tiles, dirtyRects)
                #foo
                #print(len(self.selectedTiles))
                for tile in selectedTiles:
                    #print("toPop", tile.position)
                    #print(tile.gridRow, tile.gridCol)
                    #print("in")
                    if tile.gridRow is not None:
                        #print(tile.position)
                        #foo
                        #print(tile.gridRow, tile.gridCol, grid[tile.gridRow][tile.gridCol])
                        grid[tile.gridRow][tile.gridCol].remove(tile)
                    tiles.pop()
                    #print(tile)
                    pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                            tile.getLargeRect())
                    dirtyRects.append(tile.getLargeRect())
                #print(self.grid)
                drawers.drawNearTiles(canvas, selectedTiles, tiles,
                        oldPositions, dirtyRects, oldselectedTiles, playCopy,
                        grid, gridRes, isUnSelectOld, windowSurface)
                isDeleted = True
        else:
            if selectedTile.isToDel:
                for tile in selectedTile.tileGroup:
                    tile.isToDel = False
        return isDeleted

def checkUnclick(canvas, isUnClick, isClick, tiles, selectedTiles,
        isDrawClicked, oldPositions, dirtyRects, selectedTile, fromPallet,
        oldselectedTiles, isSnapped, sidesToSnap, snapdTile, playCopy, grid, gridRes,
        isArrange, oldPlayPosition, isUnSelectOld, snapdSide):
    if isUnClick and not isClick:
        '''
        if(isinstance(self.fromPallet, Tile) and
            getDistance(self.fromPallet.position, screenLocation) <
            tile.radius * 2):
            #print("in")
            tiles.pop()
        '''
        if isSnapped:
            #print("in")
            #print(self.sidesToSnap)
            #snapdTile.isSnapped = True
            #snapdTile.adjTile.isSnapped = True
            for side in sidesToSnap:
                #print(side, side.adjSide)
                if side.adjSide.tile not in selectedTile.tileGroup:
                    for tile in selectedTile.tileGroup:
                        side.adjSide.tile.tileGroup.append(tile)
                        tile.tileGroup = side.adjSide.tile.tileGroup
                side.isSnapped = side.adjSide.isSnapped = True
                #side.tile.neighbors.append(side.adjSide.tile)
        if selectedTile is not None:
            #print("in")
            isDrawClicked = True
            #print(self.selectedTile.getLargeRect(), self.trash.rect)
            for tile in selectedTiles:
                #print(tile.position)
                oldPositions.append(tile.position)
                #print("in2")
                misc.toGrid(canvas, tile, grid, gridRes)
                #self.oldselectedTiles = []
            oldselectedTiles = []
            oldselectedTiles.extend(selectedTile.tileGroup)
            #foo
            #print("in2", oldselectedTiles)
            #for tile in self.selectedTile.tileGroup:
                #self.oldselectedTiles.append(tile)
        fromPallet = None
        #self.selectedTile = None
        isSnapped = False
        #self.adjTile = None
        snapdSide = None
        ajdSide = None
        snapdTile = None
        #self.selectedTiles = None
        #self.selectedTiles = None
        sidesToSnap = []
        #self.selectedTile = None
        if playCopy is not None:
            #foo
            #print("in")
            pygame.draw.rect(canvas.windowSurface, objects.Canvas.BACK_COLOR,
                    playCopy.getRect())
            dirtyRects.append(playCopy.getRect())
            pygame.draw.rect(canvas.windowSurface, objects.Canvas.BACK_COLOR,
                    canvas.playIcon.getRect())
            dirtyRects.append(canvas.playIcon.getRect())
            drawers.drawNearTiles([playCopy, canvas.playIcon], tiles,
                    oldPlayPosition, dirtyRects, oldselectedTiles, playCopy, grid,
                    gridRes, isUnSelectOld)
            playCopy = None
            isDrawClicked = True
            offset = (-canvas.playIcon.getRect().width *
                    (1 - objects.Canvas.PLAY_AREA_FACTOR))
            if len(tiles) > 0:
                if canvas.playIcon.getRect().inflate(offset, offset). \
                        collidepoint(mouseLoc):
                    isArrange = True
                    #self.activeTileRow = tiles
                    #foo
                    #print("in7")
                    selectedTile = tiles[0]
                elif selectedTile is not None:
                    isArrange = True
                    #self.activeRow = self.selectedTile.tilegroup
                    '''
                    activationPoint = myAdd(mouseLoc,
                            (self.playIcon.getRect().width, 0))
                    for area in self.getAreasToCheck(activationPoint):
                        for tile in area:
                            if tile.getSmallRect().collidepoint(
                                    activationPoint):
                                self.isArrange = True
                    '''
    return (isDrawClicked, selectedTile, fromPallet, oldselectedTiles,
            isSnapped, sidesToSnap, snapdTile, playCopy, isArrange, snapdSide)

def checkBorderSnap(mouseLoc, sideA, sideB, checkedTiles, isDragging,
        isSnapped, sidesToSnap, snapdTile, isConflict, selectedTiles):
    #print("in3")
    #foo
    #print(sideA.tile, sideB.tile)
    #print(sideA.corner.getAbsPosition(), sideB.corner.getAbsPosition())
    if common.isInSquare(sideA.corner.getAbsPosition(),
            sideB.corner.getAbsPosition(), 1):
        #foo
        #print("in2")
        if not isConflict:
            #isPeaking(sideB)
            #foo
            #print("sidesToSnap")
            #for side in self.sidesToSnap:
                #print(side)
            #foo
            #print(sideA.color, sideB.color)
            if (sideA.color == sideB.color and
                    sideA.isSnapped == sideB.isSnapped):
                #foo
                #print("in4")
                if not sideA.isSnapped and not sideB.isSnapped:
                    sideA.adjSide = sideB
                    sideB.adjSide = sideA
                    #foo
                    #print("in", sideA.adjSide)
                    sidesToSnap.append(sideA)
                    #print("in5")
                #sideA.isSnapped = sideB.isSnapped = True
            #foo
            else:
                #print(sideA.type, sideB.type)
                #print(sideA, sideB.adjSide, sideB, sideA.adjSide)
                '''
                print("sideA")
                for side in sideA.tile.sides:
                    print(side.color)
                print("sideB")
                for side in sideB.tile.sides:
                    print(side.color)
                print(sideA.color, sideB.color, sideA.isSnapped,
                        sideB.isSnapped)
                #foo
                '''
                #print("in3")
                #print(self.selectedTiles, self.selectedTile.tileGroup).
                if isDragging:
                    movers.noSnapMove(mouseLoc, selectedTiles)
                    isSnapped, sidesToSnap, snapdTile, isConflict = \
                            misc.unSnapAll(sidesToSnap)
                '''
                else:
                    for side in sideA.tile.sides:
                        if side.adjSide is not None:
                            sidesToSnap.pop()
                            side.adjSide.adjSide = None
                '''
                isConflict = True
                #pass
        checkedTiles.append(sideB.tile)
    return isSnapped, sidesToSnap, snapdTile, isConflict

def checkBorders(tiles):
    isConflict = False
    for tile in tiles:
        for side in tile.sides:
            if side.adjSide is not None and side.color != side.adjSide.color:
                isConflict = True
                return isConflict
    return isConflict

def checkBordersSnap(canvas, mouseLoc, tilesToSnap, checkedTiles, grid, gridRes, isDragging,
        isSnapped, sidesToSnap, snapdTile, isArranging, selectedTiles):
    #foo
    #print("checkingBorders")
    #print("in3")
    #self.selectedTile.printGroup()
    #self.sidesToSnap = []
    isConflict = False
    '''
    if selectedTile.getSmallRect().colliderect(self.palletBack):
        #print(self.selectedTile.getSmallRect(), self.palletBack)
        isSnapped, sidesToSnap, snapdTile, isConflict = \checkBorders
                self.undoSnapAndMove(selectedTiles, isSnapped, sidesToSnap,
                snapdtile, isConflict)
    '''
    #foo
    #print("in")
    for tileA in tilesToSnap:
        if tileA.isFree():
            #foo
            #print("in3")
            areasToCheck = misc.getAreasToCheck(tileA.position, grid, gridRes)
            #print("tileA")
            #print("areastocheck", areasToCheck)
            for sideA in tileA.sides:
                if not sideA.isSnapped:
                    #foo
                    #print("tileBs")
                    for area in areasToCheck:
                        #print("area")
                        #print(area.row, area.col)
                        for tileB in area:
                            #print("tileB", tileB)
                            if tileA is not tileB and not(isArranging and
                                    not tileB.isInPlayGroup):
                                sideB = tileB.getSide(sideA.adjType)
                                #print("SideB", sideB.type, sideB.color)
                                isSnapped, sidesToSnap, snapdTile, \
                                isConflict = checkBorderSnap(mouseLoc, sideA,
                                        sideB, checkedTiles, isDragging, 
                                        isSnapped, sidesToSnap, snapdTile,
                                        isConflict, selectedTiles)
                                #foo
                                #print("in2", isConflict)
                                if not isDragging and isConflict:
                                    return (isSnapped, sidesToSnap, snapdTile,
                                            isConflict)
    return isSnapped, sidesToSnap, snapdTile, isConflict

def checkClick(canvas, mouseLoc, tiles, selectedTiles, isClick,
        isDrawClicked, isDrag, selectedTile, fromPallet, playCopy, grid, gridRes,
        isUnSelectOld):
    #foo
    #print("in")
    if isClick:
        #print("isclick")
        if (not isDrag and canvas.playIcon.getRect().collidepoint(mouseLoc)):
            #foo
            #print("in6")
            playCopy = copy.copy(canvas.playIcon)
            playCopy.mouseOffset = common.mySub(mouseLoc, playCopy.position)
            isDrag = True
            isDrawClicked = True
            #self.isPlayMove = True
            #print(self.playCopy)
        else:
            #print("in2")
            isDrag, selectedTile, fromPallet = checkPallet(canvas, tiles,
                    mouseLoc, isDrag, selectedTile, fromPallet)
            selectedTiles, isDrag, selectedTile, isUnSelectOld = \
                    misc.setMouseOffset(canvas, tiles, selectedTiles,
                    mouseLoc, isDrag, selectedTile, isUnSelectOld, grid, gridRes)
            if selectedTile is not None:
                isDrawClicked = True
    return (selectedTiles, isDrawClicked, isDrag, selectedTile, fromPallet,
            playCopy, isUnSelectOld)

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
        groupGrid = GroupGrid(selectedTile.tileGroup)
        for tile in selectedTile.tileGroup:
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
        canvas.playIcon.setPause()
        #self.playIcon.image = pygame.transform.smoothscale(
                #self.pauseImage, (self.playIcon.image.get_width(),
                #self.playIcon.image.get_height()))
        isArrange = False
        #foo
        #print("in", self.groupGrid)
        arrangeIndex = 1
    return groupGrid, arrangeIndex, isArranging, activeRow, isArrange

def checkPause(canvas, mouseLoc, tiles, oldPlayPosition, dirtyRects,
        oldselectedTiles, playCopy, grid, isUnSelectOld, isDrawClicked,
        isArrangeStep, isArranging, activeRow, isMouseDown):
    if isMouseDown:
        if canvas.playIcon.getRect().collidepoint(mouseLoc):
            #foo
            canvas.playIcon.setPlay()
            pygame.draw.rect(windowSurface, Canvas.BACK_COLOR,
                canvas.playIcon.getRect())
            dirtyRects.append(canvas.playIcon.getRect())
            drawers.drawNearTiles([myCangas.playIcon], tiles,
                    oldPlayPosition, dirtyRects, oldselectedTiles, playCopy, grid,
                    gridRes, isUnSelectOld)
            if len(activeRow) > 0:
                for tile in activeRow[-1].tileGroup:
                    tile.isInPlayGroup = False
            isDrawClicked = True
            isArrangeStep = isArranging = False
    return isDrawClicked, isArrangeStep, isArranging
