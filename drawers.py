import pygame
#import canvas
import objects
import misc

def initDraw(canvas, tiles, palletBack, windowSurface):
    windowSurface.fill(objects.Canvas.BACK_COLOR)
    #canvas.fill(WHITE)
    for tile in tiles:
        #tile.resize(canvas.Canvas.scale)
        tile.scalePosition(objects.Canvas.scale)
        tile.draw()
    drawPalletBack(palletBack, windowSurface)
    for tile in canvas.tilePallet:
        tile.draw()
    #print(type(self.fromPallet))
    #if self.fromPallet is not None:
        #print("in2")
        #self.fromPallet.draw()
    #print("flip")
    #self.trash.draw()
    canvas.playIcon.draw()
    pygame.display.flip()

def drawPalletBack(palletBack, windowSurface):
    pygame.draw.rect(windowSurface, objects.Canvas.BACK_COLOR, palletBack)
    #return backRect

def drawInOrder(tiles, allTiles, windowSurface):
    for tile in sorted(tiles, key=lambda tile: allTiles.index(tile)):
        tile.draw()

#Objects should all be of the same type
def drawNearTiles(canvas, myObjects, allTiles, oldPositions, dirtyRects,
        oldSelectedTiles, playCopy, grid, gridRes, isUnSelectOld,
        windowSurface):
    #if len(myObjects) == 0 or isinstance(myObjects[0], Tile):
    #print("in3")
    areasToCheck = []
    #print(self.selectedTiles)
    #print("next")
    tilesToDraw = []
    if len(myObjects) > 0 and isinstance(myObjects[0], objects.Tile):
        for tile in myObjects:
            misc.addAreas(canvas, tile.position, areasToCheck, grid, gridRes)
        for position in oldPositions:
            misc.addAreas(canvas, position, areasToCheck, grid, gridRes)
    if playCopy is not None:
        for tile in allTiles:
            if playCopy.getRect().colliderect(tile.getSmallRect()):
                tilesToDraw.append(tile)
            else:
                '''
                for oldPosition in oldPositions:
                    oldRect = self.playCopy.getRect()
                    #oldRect.position = mySub(oldPosition,
                            #(icon.image.get_width(),
                            #icon.image.get_height()))
                    oldRect.center = oldPosition
                '''
                if (playCopy.oldRect is not None and
                        playCopy.oldRect.colliderect(tile.getSmallRect())):
                    tilesToDraw.append(tile)
    if isUnSelectOld:
        #print("in2")
        for tile in oldSelectedTiles:
            misc.addAreas(canvas, tile.position, areasToCheck, grid, gridRes)
    for area in areasToCheck:
        tilesToDraw.extend(area)
        #for tile in area:
            #tilesToDraw.append(tile)
    #foo
    #print("tilestodraw", tilesToDraw)
    drawInOrder(tilesToDraw, allTiles, windowSurface)
    '''
    for tile in sorted(tilesToDraw, key=lambda tile:
            allTiles.index(tile)):
        print("in")
        tile.draw()
    '''
                    
def drawPallet(canvas, palletBack, dirtyRects, windowSurface):
    drawPalletBack(palletBack, windowSurface)
    dirtyRects.append(palletBack)
    for tile in canvas.tilePallet:
        tile.draw()

def drawTileGroups(canvas, tiles, oldPositions, isUnClick, toDraws, dirtyRects,
        isArrangeStep, selectedTile, oldSelectedTiles, playCopy, palletBack,
        grid, gridRes, isUnSelectOld, windowSurface):
    #print("in")
    #for tile in self.selectedTiles:
        #print(tile.position)
    #print(self.selectedTile)
    #print(isUnClick)
    #if self.arrangeStep or self.selectedTile is not None:
        #toDraw = []
    #toDraws = []
    #foo
    '''
    if self.isArrangeStep:
        #print("in")
        toDraws = toDraws + self.activeRow
    '''
    if not isArrangeStep and selectedTile is not None:
        #print("in2")
        toDraws.extend(selectedTile.tileGroup)
    if len(toDraws) > 0 or playCopy is not None:
        #foo
        #print("todraws", toDraws)
        for tile in toDraws:
            tile.scalePosition(objects.Canvas.scale)
        #print("in2")
        drawNearTiles(canvas, toDraws, tiles, oldPositions, dirtyRects,
                oldSelectedTiles, playCopy, grid, gridRes, isUnSelectOld,
                windowSurface)
        drawPallet(canvas, palletBack, dirtyRects, windowSurface)
        #if self.fromPallet is None:
        #for tile in self.selectedTile.tileGroup:
        for tile in toDraws:
            #print("in2")
            #print(tile.position)
            tile.draw(True)
            dirtyRects.append(tile.getLargeRect())
    #print("dirtyrects ", self.selectedTiles)
    #for tile in self.oldSelectedTiles:
        #dirtyRects.append(tile.getLargeRect())
    #return isArrangeStep

def draw(canvas, tiles, oldPositions, isUnClick, toDraws, dirtyRects,
        isArrangeStep, isDrawClicked, isDrawAll, selectedTile,
        oldSelectedTiles, playCopy, palletBack, grid, gridRes, isUnSelectOld,
        windowSurface):
    #print(self.isUnSelectOld, selfself.isDrawClicked)
    #if isDrawClicked:
    #print("in4")
    #print(isUnClick)
    '''
    if self.selectedTile is not None:
        for i in range(len(tiles) - 1):
            tile = tiles[i]
            if isInSquare(tile.position,
                    self.selectedTile.position, 2 * tile.radius):
                tile.draw()
                dirtyRects.append(tile.getLargeRect())
    '''
    #foo
    #print("in", oldSelectedTiles)
    #print(self.isUnSelectOld)
    if isDrawClicked:
        if isUnSelectOld:
            #print("in3")
            for tile in oldSelectedTiles:
                pygame.draw.rect(canvas.windowSurface,
                    objects.Canvas.BACK_COLOR, tile.getLargeRect())
                dirtyRects.append(tile.getLargeRect())
        #print("in2")
        '''
        for tile in self.oldSelectedTiles:
            print("in2")
            pygame.draw.rect(windowSurface, Canvas.BACK_COLOR,
                    tile.getLargeRect())
        '''
        #self.drawPallet(dirtyRects)
            #dirtyRects.append(tile.getLargeRect())
        #print(self.selectedTiles)
        drawTileGroups(canvas, tiles, oldPositions, isUnClick,toDraws,
                dirtyRects, isArrangeStep, selectedTile, oldSelectedTiles,
                playCopy, palletBack, grid, gridRes, isUnSelectOld,
                windowSurface)
        if isUnClick:
            drawPallet(canvas, palletBack, dirtyRects, windowSurface)
        '''
        if self.fromPallet is not None:
            self.fromPallet.scalePosition(Canvas.scale)
            self.fromPallet.draw()
        if self.selectedTile is not None:
            dirtyRects.append(self.selectedTile.getLargeRect())
        '''
        #self.trash.draw()
        #dirtyRects.append(self.trash.rect)
        #self.playIcon.draw()
        #dirtyRects.append(self.playIcon.getRect())
        #print("in5")
        canvas.playIcon.draw()
        dirtyRects.append(canvas.playIcon.getRect())
        #foo
        #print("in6", self.playCopy)
        if playCopy is not None:
            #print("in5")
            '''
            self.drawNearTiles([self.playCopy], tiles,
                self.oldPlayPosition, dirtyRects)
            self.drawPallet(dirtyRects)
            '''
            playCopy.draw()
            dirtyRects.append(playCopy.getRect())
            #print(self.playCopy.rect)
        #print(dirtyRects)
        #if isUnClick:
            #for rect in dirtyRects:
                #pygame.draw.rect(windowSurface, BLACK, rect)
        pygame.display.update(dirtyRects)
        #Tile.delTile.set_alpha(200)
        #delTile = Tile.delTile.convert_alpha()
        #print(tile.delTile.get_alpha())
        #blitAlpha(windowSurface, pygame.transform.smoothscale(Tile.delTile,
                #(100, 100)), (100, 100), 200)
        #windowSurface.blit(pygame.transform.smoothscale(delTile, (100, 100)), (100, 100))
        #pygame.display.flip()
        #return isArrangeStep
    if isDrawAll:
        for tile in tiles:
            dirtyRects.append(tile.getLargeRect())
            tile.draw()
        #i = 0
        drawPalletBack(palletBack, windowSurface)
        dirtyRects.append(palletBack)
        for tile in canvas.tilePallet:
            tile.draw()
            #dirtyRects.append(tile.getLargeRect())
            '''
            if i == 0:
                print(tile.position, tile.scaledImage.get_width() / 2)
            i += 1
            '''
        #self.draw(tiles)
        #self.trash.draw()
        #dirtyRects.append(self.trash.rect)
        canvas.playIcon.draw()
        dirtyRects.append(canvas.playIcon.getRect())
        pygame.display.update(dirtyRects)
