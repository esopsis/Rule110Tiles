from __future__ import division
import os
import pygame
import objects
import common
#import canvas
import checkers
import drawers
import movers
import arrangers

def load(image):
    return common.load(os.path.join("images", image))

def getAdjTileRad():
    return objects.TileSet.w.get_height() * objects.Canvas.scale / 2

def toGrid(canvas, myObject, grid, resolution):
    row = int(common.y(myObject.getPosition()) // resolution) + 1
    col = int(common.x(myObject.getPosition()) // resolution) + 1
    #print("in")
    #print(myObject)
    #if isinstance(myObject, Tile):
        #print("in2")
    #print("togrid ", row, myObject.gridRow, col, myObject.gridCol)
    if not (row == myObject.gridRow and col == myObject.gridCol):
        #print("in3")
        #try:
        #if myObject.gridRow >= 0 and myObject.gridCol >= 0:
            #print("in4")
        if myObject.gridRow is not None:
            grid[myObject.gridRow][myObject.gridCol].remove(myObject)
            #print("in5")
        #Happens when creating new tile from pallet.  Removing tile
        #not in list.
        #except ValueError:
            #print("in")
            #pass
        #except IndexError:
            #print("in2")
            #pass
        #Should get an error for commenting out the next few lines,
        #but I can't remember what causes it.
        #except TypeError:
            #print("in3")
            #pass
        if myObject.getSmallRect().colliderect(0, 0, canvas.WIDTH,
                canvas.HEIGHT):
            #print(myObject.position)
            myObject.gridRow = row
            myObject.gridCol = col
            #print(row, col)
            grid[row][col].append(myObject)
        else:
            myObject.gridRow = myObject.gridCol = None

def setGrid(canvas, tiles):
    gridRes = 2.2 * getAdjTileRad()
    #self.grid = []
    #print(WIDTH, Canvas.scale)
    #Add 3 to make up for tiles going off edges of screen, and roudning
    #down of //.
    rowNum = int(canvas.HEIGHT // gridRes + 3)
    #print("rownum", rowNum)
    colNum = int(canvas.WIDTH // gridRes + 3)
    #print("setGrid ", rowNum, colNum)
    #print(colNum, rowNum)
    '''
    for i in range(rowNum):
        self.grid.append([])
        for j in range (colNum):
            self.grid[i].append([])
    '''
    grid = common.makeGrid(rowNum, colNum, "empty")
    #self.grid = [[[] for j in range(colNum)] for i in range(rowNum)]
    for tile in tiles:
        tile.gridRow = tile.gridCol = None
        toGrid(canvas, tile, grid, gridRes)
        #for corner in tile.corners:
            #self.toGrid(corner, self.grid, self.gridRes)
    return grid, gridRes

def resizePalletBack(canvas):
    lastTile = canvas.tilePallet[-1]
    palletBack = pygame.Rect(0, 0, common.x(lastTile.position) +
            lastTile.scaledImage.get_width() / 2,
            lastTile.scaledImage.get_height())
    return palletBack

def scrollSize(canvas, tiles, grid, gridRes, palletBack, isScrollDown, isScrollUp, dirtyRects,
        isDrawAll, windowSurface):
    if isScrollDown or isScrollUp:
        #print("in")
        for tile in tiles:
            pygame.draw.rect(windowSurface, canvas.Canvas.BACK_COLOR,
                    tile.getLargeRect())
            dirtyRects.append(tile.getLargeRect())
            tile.resize(canvas.Canvas.scale)
            tile.scalePosition(canvas.Canvas.scale)
            #print("in4")
            #self.toGrid(tile, self.grid, self.gridRes)
        grid, gridRes = setGrid(canvas, tiles)
        for tile in canvas.tilePallet:
            pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR,
                    tile.getLargeRect())
            dirtyRects.append(tile.getLargeRect())
            tile.resize(objects.Canvas.scale)
            tile.scalePosition(objects.Canvas.scale)
            dirtyRects.append(tile.getLargeRect())
        palletBack = resizePalletBack(canvas)
        isDrawAll = True
    return grid, gridRes, palletBack, isDrawAll

def getAreasToCheck(location, grid, gridRes):
    row = int(common.y(location) // gridRes) + 1
    col = int(common.x(location) // gridRes) + 1
    #print("next")
    #print(row, col)
    #print("mouse ", row, col)
    #if len(tiles) > 0:
        #print("tile ", tiles[0].gridRow, tiles[0].gridCol)
    #print(len(self.grid), len(self.grid[0]))
    #print(len(self.grid), len(self.grid[0]))
    areasToCheck = []
    for i in range(-1, 1 + 1):
        for j in range(-1, 1 + 1):
            if (row + i >= 0 and col + j >= 0 and row + i < len(grid) and
                    col + j < len(grid[0])):
                #print(row + i, col + j)
                areasToCheck.append(grid[row + i][col + j])
    return areasToCheck

def setMouseOffset(canvas, tiles, selectedTiles, mouseLoc, isDrag,
        selectedTile, isUnSelectOld, grid, gridRes):
    #print("in")
    areasToCheck = getAreasToCheck(mouseLoc, grid, gridRes)
    #print("mouseoffset ", areasToCheck)
    #print("next")
    #if self.selectedTile is not None:
        #self.selectedTile.printGroup()
    for area in areasToCheck:
        for tile in area:
            if (not isDrag and common.isInSquare(mouseLoc, tile.position,
                    tile.radius) and
                    common.getDistance(mouseLoc, tile.position) <
                    tile.radius and (selectedTile is None or
                    tiles.index(tile) > tiles.index(selectedTile))):
                #print("in3")
                selectedTile = tile
    if selectedTile is not None:
        #print("in3")
        #self.selectedTile = tile
        #print(button)
        isUnSelectOld = True
        #print(self.isUnSelectOld)
        if canvas.isLDown:
            #print(self.selectedTile)
            selectedTiles = [selectedTile]
            #print("in5")
        else:
            #print("in4")
            #self.selectedTile.printGroup()
            selectedTiles = []
            for tile in selectedTile.tileGroup:
                selectedTiles.append(tile)
            #self.selectedTiles = self.selectedTile.tileGroup
        #print(self.selectedTiles, self.selectedTile.tileGroup)
        #print(self.selectedTiles)
        #self.selectedTile.mouseOffset = mySub(mouseLoc,
                #tile.position)
        isDrag = True
        for tile in selectedTile.tileGroup:
            tile.mouseOffset = common.mySub(mouseLoc, tile.position)
            #Next lines make it so the clicked tile's group gets sent to
            #the top layer.
            #print("movetotop")
            tiles.remove(tile)
            tiles.append(tile)
            #print("in")
            #tilesToTop.append(tile)
    return selectedTiles, isDrag, selectedTile, isUnSelectOld

def addNeighbors(tile, selectedTile):
    for side in tile.sides:
        if (side.isSnapped and side.adjSide.tile is not selectedTile and
                side.adjSide.tile not in tile.tileGroup):
            tile.tileGroup.append(side.adjSide.tile)
            side.adjSide.tile.tileGroup = tile.tileGroup
            addNeighbors(side.adjSide.tile, selectedTile)

def snapTiles(selectedTile, snapdSide, adjSide):
    #foo
    snapdTile = snapdSide.tile
    #print("in", snapdTile.getSmallRect())
    #print(self.snapdTile)
    for tile in selectedTile.tileGroup:
        if tile is not snapdTile:
            tile.groupOffset = common.mySub(tile.absPosition,
                    snapdTile.absPosition)
        else:
            tile.groupOffset = (0, 0)
    for tile in selectedTile.tileGroup:
        #print(self.adjSide.type)
        #print("in4")
        tile.matchCorner(snapdSide.corner,
                common.myAdd(adjSide.corner.getAbsPosition(),
                tile.groupOffset))
        #tile.absPosition = map(int, map(round, myAdd(mySub(
                #self.adjSide.corner.getAbsPosition(),
                #self.snapdSide.corner.offset), tile.groupOffset)))
    snapdTile.adjTile = adjSide.tile
    snapdTile.adjTile.adjTile = snapdTile
    isSnapped = True
    #foo
    #print(snapdTile.getSmallRect())
    return isSnapped, snapdTile, snapdSide

    #self.snapdTile.snapdCorner = self.snapdSide.corner
    #self.snapdTile.adjCorner = self.adjSide.corner

    #self.snapdTile.adjTile.snapdCorner = self.snapdTile.adjCorner
    #self.snapdTile.adjTile.adjCorner = self.snapdTile.snapdCorner

def unSnapAll(sidesToSnap):
    #self.noSnapMove(selectedTiles)
    #print("unsnap2")
    for side in sidesToSnap:
        #print(side.adjSide)
        side.adjSide.adjSide = None
        side.adjSide = None
    sidesToSnap = []
    snapdTile = None
    isSnapped = False
    #break
    isConflict = True
    return isSnapped, sidesToSnap, snapdTile, isConflict

def findMatch(sideA, sideB, minDistance, isMatch, snapdSide, adjSide):
    if (sideA.color == sideB.color and
            common.isInSquare(sideA.corner.getPosition(),
            sideB.corner.getPosition(), minDistance) and not sideB.isSnapped):
        #print("in3")
        distance = common.getDistance(sideA.corner.getPosition(),
                sideB.corner.getPosition())
        if distance < minDistance:
            minDistance = distance
            #self.snapdTile = tile
            snapdSide = sideA
            adjSide = sideB
            isMatch = True
    return minDistance, isMatch, snapdSide, adjSide

'''
def addToPlayGroup(self, tile, tiles):
    tile.isInPlayGroup = True
    tileGroup = tiles[len(tiles) - 1].tileGroup
    tiles[len(tiles) - 1].tileGroup.append(tile)
    tile.tileGroup = tiles[len(tiles) - 1].tileGroup
'''

def addAreas(canvas, position, areasToCheck, grid, gridRes):
    for area in getAreasToCheck(position, grid, gridRes):
        if not area in areasToCheck:
            areasToCheck.append(area)

def update(canvas, tiles, selectedTiles, mouseLoc, button, isUnClick,
        isClick, isScrollDown, isScrollUp, isSpace, isArrangeStep, grid, gridRes, groupGrid,
        arrangeIndex, isArranging, activeRow, isDrag, selectedTile, fromPallet, palletBack,
        oldSelectedTiles, isSnapped, sidesToSnap, snapdTile, playCopy, 
        isArrange, oldPlayPosition, isUnSelectOld, snapdSide, adjSide, clock,
        FPS, oldMouseLoc, windowSurface):
    #print("grid", self.grid)
    #print("tick")
    #oldSelectedTiles = []
    #if len(tiles) > 0:
        #print("in", tiles[0].position, tiles[0].getSmallRect())
    oldPositions = []
    dirtyRects = []
    toDraws = []
    isDrawClicked = isDrawAll = False
    #foo
    #print(isArranging)
    if isUnClick:
        #print("in1")
        canvas.isMouseDown = canvas.isLDown = canvas.isRDown = \
                isClick = isDrag = False
        #isPastClick = False
    #print(button)
    else:
        if button == canvas.RIGHT:
            canvas.isRDown = True
            canvas.isMouseDown = True
        elif button == canvas.LEFT:
            canvas.isLDown = True
            canvas.isMouseDown = True
    if isArranging:
        arrangeIndex, isDrawClicked, isArrangeStep, isArranging, activeRow, \
                selectedTiles, selectedTile, isSnapped, sidesToSnap, \
                snapdtile = arrangers.doArranging(canvas, grid, gridRes,
                groupGrid, arrangeIndex,
                mouseLoc, isClick, toDraws, dirtyRects, isDrawClicked,
                isArrangeStep, isArranging, activeRow, selectedTiles,
                selectedTile, oldSelectedTiles, isSnapped, sidesToSnap,
                snapdTile, playCopy, oldPlayPosition, isUnSelectOld, tiles)
    else:
        clock.tick(FPS)
        isUnSelectOld = False
        isDeleted = False
        #self.isDraw = False
        #dirtyRects = []
        #'''
        #print(self.isMouseDown, isScrollDown, isScrollUp, isUnClick)
        #print(isScrollDown, isScrollUp)
        grid, gridRes, palletBack, isDrawAll = scrollSize(canvas, tiles, grid, gridRes, palletBack, isScrollDown, isScrollUp,
                dirtyRects, isDrawAll, windowSurface)
        #areasToCheck = self.getAreasToCheck(mouseLoc)
        #print(areasToCheck)
        #backTiles = []
        #isPlayMove = False
        selectedTiles, isDrawClicked, isDrag, selectedTile, fromPallet, \
                playCopy, isUnSelectOld = checkers.checkClick(canvas, mouseLoc, tiles,
                selectedTiles, isClick, isDrawClicked, isDrag, selectedTile,
                fromPallet, playCopy, grid, gridRes, isUnSelectOld)
        #foo
        #print("in5", self.playCopy)
            #self.toCheckSnaps = tiles[:-len(self.selectedTile.tilegroup)]
        #print(self.selectedTile)
        #oldPositions = []
        isDrawClicked, selectedTile, fromPallet, oldSelectedTiles, isSnapped, \
                sidesToSnap, snapdTile, playCopy, isArrange, snapdSide = \
                checkers.checkUnclick(canvas, isUnClick, isClick, tiles,
                selectedTiles, isDrawClicked, oldPositions, dirtyRects,
                selectedTile, fromPallet, oldSelectedTiles, isSnapped,
                sidesToSnap, snapdTile, playCopy, grid, gridRes, isArrange, oldPlayPosition,
                isUnSelectOld, snapdSide, mouseLoc)
        #'''
        #if isSpace:
            #self.isArranging = not self.isArranging
        #foo
        '''
        if self.selectedTile is not None:
            print(len(self.selectedTiles))
            for tile in self.selectedTiles:
                print(tile)
        '''
        isDeleted = checkers.checkTrash(canvas, tiles, selectedTiles,
                oldPositions, isUnClick, dirtyRects, selectedTile,
                oldSelectedTiles, playCopy, grid, gridRes, palletBack, isUnSelectOld, isDeleted,
                windowSurface)
        #Set mouse offset if drag background 
        if not isDrag and isClick:
            #print("in5")
            for tile in tiles:
                tile.mouseOffset = common.mySub(mouseLoc, tile.position)
        #print(isClicked, isUnClick)
        #print(self.isDrag)
        '''
        if self.selectedTile is None:
            print("None")
        else:
            print(self.selectedTile.position)
        '''
        #print(self.selectedTile)
        #print("in ", self.isUnSelectOld)
        #print(mouseLoc, self.oldMouseLoc)
        #print("ismousedown ", self.isMouseDown, not mouseLoc == self.oldMouseLoc)
        #print("in")
        if canvas.isMouseDown and mouseLoc != oldMouseLoc:
            #print("in6")
            #self.toGrid(self.selectedTile, self.cornerGrid, WIDTH, HEIGHT,
                    #self.gridRes)
            #print(self.selectedTile)
            #foo
            #print("in3", isDrag)
            if isDrag:
                #print("in")
                #isDrawClicked = True
                #foo
                #print("playcopy", self.playCopy)
                if playCopy is not None:
                    isDrawClicked, activeRow, selectedTile, oldSelectedTiles, \
                            oldPlayPosition, isUnSelectOld = \
                            movers.movePlayIcon(canvas, dirtyRects, tiles,
                            activeRow, selectedTile, oldSelectedTiles,
                            playCopy, isUnSelectOld, mouseLoc)
                    #if isUnClick:
                        #foo
                        #print("in2")
                        #self.playCopy = None
                    #foo
                    #print("in", selectedTile)
                else:
                    #foo
                    #print("in2", selectedTiles)
                    isDrawClicked, oldSelectedTiles, isSnapped, sidesToSnap, \
                            snapdTile, isUnSelectOld, snapdSide, adjSide = \
                            movers.moveSome(canvas, mouseLoc, tiles,
                            selectedTiles, oldPositions, isUnClick, dirtyRects,
                            selectedTile, oldSelectedTiles, isSnapped,
                            sidesToSnap, snapdTile, palletBack, isUnSelectOld, snapdSide,
                            adjSide, grid, gridRes, isArranging, windowSurface)
                #foo
                #print("in", isDrawClicked)
            #Move all tiles if dragging background
            elif (len(tiles) > 0 and
                    tiles[-1].mouseOffset is not None):
                #foo
                #print("in2")
                isDrawAll = movers.tryMoveAll(canvas, tiles, mouseLoc, grid, gridRes,
                        dirtyRects, isDrawAll)
                    #print("in")
            #print(self.isDrawClicked)
            #print(self.isDrawClicked)
            #if self.isUnSelectOld == True:
            #print("in")
        if isDeleted:
            selectedTile = None
        groupGrid, arrangeIndex, isArranging, activeRow, isArrange = \
                arrangers.checkArrangeInit(canvas, arrangeIndex, isArranging,
                activeRow, selectedTile, isArrange, groupGrid, tiles)
    #'''
    #if self.selectedTile is not None:
        #print("isSnapped", self.selectedTile.isSnapped)
    #print("in2", self.isLDown, self.selectedTile)
    if isDrawClicked or isDrawAll:
        #print("in6", isDrawClicked)
        drawers.draw(canvas, tiles, oldPositions, isUnClick, toDraws,
                dirtyRects, isArrangeStep, isDrawClicked, isDrawAll,
                selectedTile, oldSelectedTiles, playCopy, palletBack, grid, gridRes, isUnSelectOld,
                windowSurface)
    #self.oldSelectedTiles = []
    #TODO: These next two lines MAY be problematic.
    #TODO: It MAY be better to move this to earlier in the program.
    if isUnClick:
        #print("in")
        selectedTile = None
    oldMouseLoc = mouseLoc
    if playCopy is not None:
        playCopy.oldRect = playCopy.getRect()
    return (selectedTiles, isArrangeStep, grid, gridRes, groupGrid, arrangeIndex,
            isArranging, activeRow, isDrag, selectedTile, fromPallet, palletBack,
            oldSelectedTiles, isSnapped, sidesToSnap, snapdTile, playCopy,
            isArrange, oldPlayPosition, isUnSelectOld, snapdSide, adjSide,
            oldMouseLoc)
