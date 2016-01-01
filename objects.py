from __future__ import division
import pygame
#import os
import common
import drawers
#import canvas
import misc
#import common

class Canvas:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SNAP_DISTANCE = 300
    scale = .04
    BACK_COLOR = WHITE
    LEFT = 1
    RIGHT = 3
    PLAY_AREA_FACTOR = .5
    ARRANGE_TIME = 480
    def __init__(self, tiles, windowSurface):
        self.windowSurface = windowSurface
        self.WIDTH = windowSurface.get_width()
        self.HEIGHT = windowSurface.get_height()
        self.isMouseDown = self.isLDown = self.isRDown = False
        windowSurface.fill(Canvas.BACK_COLOR)
        self.tilePallet = []
        self.playImage = misc.load("play.png")
        self.pauseImage = misc.load("pause.png")
        #self.playIcon = Icon(self.playImage, (WIDTH - 80, 60), 90,
                #90)
        self.playIcon = Icon(Icon.PLAY, (self.WIDTH - 80, 60), 90, 90, self)
        for i in range(len(TileSet.palletImgs)):
            image = TileSet.palletImgs[i]
            tile = Tile(self, image, (i * Tile.ADJ_WIDTH, 0), False,
                    self.tilePallet)
            self.tilePallet.append(tile)
        self.oldMouseLoc = None
        self.lastTick = pygame.time.get_ticks()
        #Time for each step of auto arranging function, in seconds.
        self.rules = {"000": 0, "001": 1, "010": 1, "011": 1, "100": 0,
                "101": 1, "110": 1, "111": 0}

class Side:
    UPPER_RIGHT = 0
    RIGHT = 1
    LOWER_RIGHT = 2
    LOWER_LEFT = 3
    LEFT = 4
    UPPER_LEFT = 5
    toAdjacents = {UPPER_RIGHT : LOWER_LEFT, RIGHT : LEFT,
            LOWER_RIGHT : UPPER_LEFT, LOWER_LEFT : UPPER_RIGHT,
            LEFT : RIGHT, UPPER_LEFT: LOWER_RIGHT}
    
    def __init__(self, myType, corner):
        #self.color = color
        self.color = None
        self.type = myType
        self.adjType = Side.toAdjacents[myType]
        #self.sideGroup = sideGroup
        self.isSnapped = False
        self.adjSide = None
        self.corner = corner
        self.tile = corner.tile
        self.canvas = self.tile.canvas
        #self.endA = corner.getPosition()
        self.endBs = {Side.UPPER_RIGHT : self.getUpper, Side.RIGHT :
                self.getLowerRight, Side.LOWER_RIGHT : self.getLowerRight,
                Side.LOWER_LEFT : self.getLowerLeft, Side.LEFT :
                self.getLowerLeft, Side.UPPER_LEFT : self.getUpper}

    def getEndA(self):
        return self.corner.getPosition()

    def getEndB(self):
        return self.endBs[self.type]()

    def getUpper(self):
        return common.adjToScreen((x(self.tile.absPosition),
                y(self.tile.absPosition) - self.corner.adjRadius),
                canvas.Canvas.scale, self.canvas.WIDTH, self.canvas.HEIGHT)

    def getLowerRight(self):
        return common.adjToScreen((x(self.tile.absPosition) + (3 ** .5 *
                self.corner.adjRadius / 2), y(self.tile.absPosition) + .5 *
                self.corner.adjRadius), canvas.Canvas.scale,
                self.canvas.WIDTH, self.canvas.HEIGHT)

    def getLowerLeft(self):
        return common.adjToScreen((x(self.tile.absPosition) - (3 ** .5 *
                self.corner.adjRadius / 2), y(self.tile.absPosition) + .5 *
                self.corner.adjRadius), canvas.Canvas.scale,
                self.canvas.WIDTH, self.canvas.HEIGHT)

    def setColor(self, tileColors):
        self.color = tileColors[self.type]

'''
class SideGroup:
    def __init__(self):
        self.sides = []	
        adjGroup = None
'''

class TileSet:
    #fooo
    #print("in7")
    palletFiles = ["bY.png", "y.png", "rYB.png", "rY.png", "rB.png", "bR.png",
            "w.png"]
    palletImgs = [misc.load(image) for image in palletFiles]
    #print(palletImgs)
    bY = palletImgs[0]
    y = palletImgs[1]
    rYB = palletImgs[2]
    rY = palletImgs[3]
    rB = palletImgs[4]
    bR = palletImgs[5]
    w = palletImgs[6]
    #print(w)

class Corner:
    UPPER_LEFT = 0
    UPPER_RIGHT = 1
    LOWER = 2
    '''
    TILE_WHITE = 0
    RED = 1
    YELLOW = 2
    BLUE = 3
    LEFT_COLOR = 0
    RIGHT_COLOR = 1
    tileToColors = {TileSet.rB : [TILE_WHITE, TILE_WHITE, RED, TILE_WHITE,
            BLUE, RED], TileSet.bY : [YELLOW, BLUE, TILE_WHITE, TILE_WHITE,
            BLUE, TILE_WHITE], TileSet.rYB : [TILE_WHITE, BLUE, RED, YELLOW,
            TILE_WHITE, RED], TileSet.rY : [TILE_WHITE, TILE_WHITE, RED,
            YELLOW, TILE_WHITE, RED], TileSet.bR : [TILE_WHITE, BLUE,
            TILE_WHITE, TILE_WHITE, BLUE, RED], TileSet.y : [YELLOW, BLUE, RED,
            YELLOW, TILE_WHITE, TILE_WHITE], TileSet.w : [TILE_WHITE,
            TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE]}
    '''
    
    def __init__(self, myType, tile):
        self.tile = tile
        self.canvas = tile.canvas
        self.adjRadius = Tile.ABS_RADIUS - Tile.LINE_WIDTH / 3 ** .5
        self.gridRow = None
        self.gridCol = None
        self.isSnapped = False
        #colors = Corner.tileToColors[tile.image]
        #print("next")
        #if self.tile.upperLeft is not None:
            #print(self.tile.upperLeft.leftSide.sideGroup.sides)
        if myType == Corner.UPPER_LEFT:
            self.offset = (-Tile.ADJ_WIDTH / 2, -Tile.ADJ_HEIGHT / 4)
            self.rightSide = Side(Side.UPPER_LEFT, self)
            self.leftSide = Side(Side.LEFT, self)
            #print("in")
        elif myType == Corner.UPPER_RIGHT:
            self.offset = (Tile.ADJ_WIDTH / 2, -Tile.ADJ_HEIGHT / 4)
            self.leftSide = Side(Side.UPPER_RIGHT, self)
            self.rightSide = Side(Side.RIGHT, self)
            #print("in2")
        elif myType == Corner.LOWER:
            self.offset = (0, Tile.ADJ_HEIGHT / 2)
            self.leftSide = Side(Side.LOWER_LEFT, self)
            self.rightSide = Side(Side.LOWER_RIGHT, self)
            #print("in3")
        self.sides = [self.leftSide, self.rightSide]
        #print("setcorner ", self.leftSide.sideGroup.sides)
        #self.position = tuple(map(add, tile.position, self.offset))
        #if self.tile.upperLeft is not None:
            #print(self.tile.upperLeft.leftSide.sideGroup.sides)
            
    def getAbsPosition(self):
        #print(self.tile.position, self.offset)
        return map(int, map(round, common.myAdd(self.tile.absPosition,
                self.offset)))  

    def getPosition(self):
        #absPosition = self.getAbsPosition()
        #return (x(absPosition) * Canvas.scale + WIDTH / 2, y(absPosition) *
                #Canvas.scale + HEIGHT / 2)
        #print ((x(absPosition) * Canvas.scale + WIDTH / 2, y(absPosition) *
                #Canvas.scale + HEIGHT / 2), myAdd(myMult(Canvas.scale, self.getAbsPosition()), (WIDTH / 2, HEIGHT / 2)))
        return map(int, map(round, common.adjToScreen(self.getAbsPosition(),
            Canvas.scale, self.canvas.WIDTH,
                self.canvas.HEIGHT)))
    
    def getOffset(self):
        return common.myMult(Canvas.scale, self.offset)
        #return (x(self.offset) * Canvas.scale, y(self.offset) * Canvas.scale)
        
class Tile:
    LINE_WIDTH = 20
    HILIGHT_WIDTH = 50
    DEL_TILE_TRANSPARENCY = 116
    delTile = misc.load("delTile.png")
    playTile = misc.load("playTile.png")
    TILE_WHITE = 0
    RED = 1
    YELLOW = 2
    BLUE = 3
    #fooo
    #print("in8")
    ADJ_WIDTH = TileSet.w.get_width() - LINE_WIDTH
    ADJ_HEIGHT = TileSet.w.get_height() - LINE_WIDTH * 2 / 3**.5
    ABS_RADIUS = TileSet.w.get_height() / 2
    #LEFT_COLOR = 0
    #RIGHT_COLOR = 1
    tileToColors = {TileSet.rB : [TILE_WHITE, TILE_WHITE, RED, TILE_WHITE,
            BLUE, RED], TileSet.bY : [YELLOW, BLUE, TILE_WHITE, TILE_WHITE,
            BLUE, TILE_WHITE], TileSet.rYB : [TILE_WHITE, BLUE, RED, YELLOW,
            TILE_WHITE, RED], TileSet.rY : [TILE_WHITE, TILE_WHITE, RED,
            YELLOW, TILE_WHITE, RED], TileSet.bR : [TILE_WHITE, BLUE,
            TILE_WHITE, TILE_WHITE, BLUE, RED], TileSet.y : [YELLOW, BLUE, RED,
            YELLOW, TILE_WHITE, TILE_WHITE], TileSet.w : [TILE_WHITE,
            TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE]}
    def __init__(self, canvas, image=None, absPosition=None, \
            isMovable=True, palletGroup=None):
        self.canvas = canvas
        self.absPosition = absPosition
        #self.position = absPosition
        #print("init", self.position)
        self.mouseOffset = None
        '''
        self.image = image
        self.scaledImage = image
        self.absRadius = image.get_height() / 2
        '''
        self.isMovable = isMovable
        self.gridRow = self.gridCol = None
        self.groupOffset = None
        self.isToDel = self.isToPlay = self.isInPlayGroup = False
        self.binary = None
        self.image = None
        #self.fromPallet = False
        if isMovable:
            self.upperLeft = None
            #print("in")
            self.upperLeft = Corner(Corner.UPPER_LEFT, self)
            #print(self.upperLeft.leftSide.sideGroup.sides)
            #print(self.upperLeft.leftSide.sideGroup == canvas.lefts)
            self.upperRight = Corner(Corner.UPPER_RIGHT, self)
            #print("settile ", self.upperLeft.leftSide.sideGroup.sides)
            self.lower = Corner(Corner.LOWER, self)
            #print(self.upperLeft.leftSide.sideGroup.sides)
            self.corners = [self.upperLeft, self.upperRight, self.lower]
            self.sides = []
            self.sides.append(self.upperRight.leftSide)
            self.sides.append(self.upperRight.rightSide)
            self.sides.append(self.lower.rightSide)
            self.sides.append(self.lower.leftSide)
            self.sides.append(self.upperLeft.leftSide)
            self.sides.append(self.upperLeft.rightSide)
            '''
            for corner in self.corners:
                for side in corner.sides:
                    self.sides.append(side)
            '''
            #self.isSnapped = False
            #self.snapdCorner = None
            #self.adjCorner = None
            self.tileGroup = [self]
            #print(self.upperLeft.leftSide.sideGroup.sides)
            #print("sides ", self.sides[0].sideGroup.sides)
            self.sideOptions = {
                    Side.UPPER_RIGHT : self.upperRight.leftSide,
                    Side.RIGHT : self.upperRight.rightSide,
                    Side.LOWER_RIGHT : self.lower.rightSide,
                    Side.LOWER_LEFT : self.lower.leftSide,
                    Side.LEFT : self.upperLeft.leftSide,
                    Side.UPPER_LEFT : self.upperLeft.rightSide}
            self.image = Tile.delTile
            #self.binary = 0
            self.oldImage = None
            self.oldScaledImage = None
        if image is not None:
            self.setImage(image)
        if absPosition is not None:
            self.scalePosition(Canvas.scale, palletGroup)
        '''
        if image is None:
            self.resize(canvas.Canvas.scale)
        else:
            self.setImage(image)
            self.resize(canvas.Canvas.scale)
        '''
        #self.absRadius = image.get_height() / 2
        #self.neighbors = []
        #if absPosition is not None:
            #self.scalePosition(canvas.Canvas.scale)
        self.adjTile = None
        #self.resizeDelTile()
        #sides = self.sides[0].sideGroup.sides
        #print(self.isMovable)

    def setImage(self, image):
        if image is not self.image:
            self.image = image
            #self.scaledImage = image
            if image is TileSet.w:
                self.binary = 0
            else:
                self.binary = 1
            #self.absRadius = image.get_height() / 2
            if self.isMovable:
                for side in self.sides:
                    side.setColor(Tile.tileToColors[self.image])
                '''
                self.upperRight.leftSide.color = colors[0]
                self.upperRight.rightSide.color = colors[1]
                self.lower.rightSide.color = colors[2]
                self.lower.leftSide.color = colors[3]
                self.upperLeft.leftSide.color = colors[4]
                self.upperLeft.rightSide.color = colors[5]
                '''

    def isSnapped(self):
        for side in self.sides:
            if side.isSnapped:
                return True
        return False

    def unSnapSides(self):
        for side in self.sides:
            side.isSnapped = False
            if side.adjSide is not None:
                #print("in")
                #side.adjSide.tile.isSnapped = False
                side.adjSide.isSnapped = False
                side.adjSide.adjSide = None
                side.adjSide = None

    def unSnap(self):
        #print("unsnap()")
        #self.isSnapped = False
        #self.printGroup()
        self.tileGroup.remove(self)
        self.adjTile = None
        #self.printGroup()
        #print("")
        #for corner in self.corners:
        #print("next")
        '''
        for tile in tiles:
            print(tile.position)
            for side in tile.sides:
                print (side.isSnapped)
        '''
        self.unSnapSides()
        '''
        for tile in tiles:
            print(tile.position)
            for side in tile.sides:
                print (side.isSnapped)
        '''
        #for tile in self.neighbors:
            #tile.neighbors.remove(self)
        self.tileGroup = [self]
        #self.neighbors = []
    
    def setPosition(self, position, pallet=None):
        self.position = position
        self.absPosition = map(int, map(round, common.myDiv(common.mySub(
                position, (self.canvas.WIDTH / 2, self.canvas.HEIGHT / 2)),
                Canvas.scale)))
        self.scalePosition(Canvas.scale, pallet)
        #self.absPosition = ((x(position) - WIDTH / 2) / Canvas.scale,
                #(y(position) - HEIGHT / 2) / Canvas.scale)

    def getPosition(self):
        return self.position

    def matchCorner(self, corner, adjPoint):
        #foo
        #print("in")
        self.absPosition = map(int, map(round, common.mySub(adjPoint,
                corner.offset)))
        self.scalePosition(Canvas.scale)

    def isFree(self):
        #'''
        for side in self.sides:
            if not side.isSnapped:
                return True
        return False
        #'''
        '''
        isFree = False
        for side in self.sides:
            if not side.isSnapped:
                isFree = True
        return isFree
        '''
        
    def draw(self, isHilight=False):
        '''
        windowSurface.blit(self.scaledImage, (x(self.position) -
                self.scaledImage.get_width() / 2, y(self.position) -
                self.scaledImage.get_height() / 2))
        '''
        #if self.isMovable:
            #print(self.position)
        #windowSurface.blit(self.scaledImage, common.mySub(self.position,
                #(self.scaledImage.get_width() / 2,
                #self.scaledImage.get_height() / 2)))
        self.canvas.windowSurface.blit(self.scaledImage, self.getSmallRect())
        #print("draw ", self.isToDel)
        if self.isToDel or self.isToPlay:
            if self.isToDel:
                overlay = self.scaledDelTile
            elif self.isToPlay:
                overlay = self.scaledPlayTile
            common.blitAlpha(self.canvas.windowSurface, overlay,
                    self.getSmallRect(), Tile.DEL_TILE_TRANSPARENCY)
            '''
            common.blitAlpha(windowSurface, self.scaledDelTile,
                    common.mySub(self.position, (self.scaledImage.get_width() /
                    2, self.scaledImage.get_height() / 2)),
                    Tile.DEL_TILE_TRANSPARENCY)
            '''
        '''
        if self.isToPlay:
            #print("in")
            blitAlpha(windowSurface, self.scaledPlayTile, mySub(self.position,
                    (self.scaledImage.get_width() / 2,
                    self.scaledImage.get_height() / 2)),
                    Tile.DEL_TILE_TRANSPARENCY)
        '''
        '''
        if isHilight:
            for side in self.sides:
                if not side.isSnapped:
                    pygame.draw.line(windowSurface, BLACK, side.getEndA(),
                            side.getEndB(), int(round(Tile.HILIGHT_WIDTH *
                            Canvas.scale)))
        '''
        #print(self.radius, self.scaledImage.get_height() / 2,
                #self.scaledImage.get_width() / 2)
        '''
        else:
            windowSurface.blit(self.scaledImage, (x(self.position) -
                    WIDTH / 2, y(self.position) - HEIGHT / 2))
        windowSurface.blit(self.scaledImage, (x(self.position) -
                    self.scaledImage.get_width() / 2, y(self.position) -
                    self.scaledImage.get_height() / 2))
        '''

    def scaleImage(self, scale):
        self.adjWRad = Tile.ADJ_WIDTH * scale * .5
        self.adjHRad = Tile.ADJ_HEIGHT * scale * .5
        self.adjWidth = int(round(common.x(self.position) + self.adjWRad)) - \
                int(round(common.x(self.position) - self.adjWRad)) + 1
        self.adjHeight = int(round(common.y(self.position) + self.adjHRad)) - \
                int(round(common.y(self.position) - self.adjHRad)) + 1
        #self.scaledImage  = pygame.transform.smoothscale(self.image,
            #(int(round(self.image.get_width() * scale)),
            #int(round(self.image.get_height() * scale))))
        self.scaledImage = pygame.transform.smoothscale(self.image,
            (self.adjWidth, self.adjHeight))
        
    def resize(self, scale):
        #self.position = (0, 0)
        #self.position = (scale * x(self.absPosition) + WIDTH / 2,
                #scale * y(self.absPosition) + HEIGHT / 2)
        self.scaleImage(scale)
        self.radius = self.adjHeight / 2
        #self.resizeDelTile()
        self.scaledDelTile = pygame.transform.smoothscale(Tile.delTile,
                (self.adjWidth, self.adjHeight))
        self.scaledPlayTile = pygame.transform.smoothscale(Tile.playTile,
                (self.adjWidth, self.adjHeight))
        #pygame.display.flip()
        
    def scalePosition(self, scale, pallet=None):
        #print(self.absPosition)
        #self.position = (scale * x(self.absPosition), scale *
                #y(self.absPosition))
        #foo
        #print("in", self.absPosition)
        self.position = common.myMult(scale, self.absPosition)
        self.resize(scale)
        if self.isMovable:
            self.position = common.myAdd(self.position,
                    map(round, (self.canvas.windowSurface.get_width() / 2,
                     self.canvas.windowSurface.get_height() / 2)))
        else:
            if len(pallet) == 0:
                tile = self
            else:
                tile = pallet[0]
                #print(tile.adjWidth / 2)
            self.position = common.myAdd(self.position, map(round,
                    (tile.adjWidth / 2, tile.adjHeight / 2)))
        #print("in2", self.position)

    def getSide(self, myType):
        return self.sideOptions[myType]

    def getSmallRect(self):
        #TODO: fix this?
        return pygame.Rect(map(int, map(round,
                common.mySub(self.position, (self.adjWRad, self.adjHRad)))),
                (self.adjWidth, self.adjHeight))
        '''
        return self.scaledImage.get_rect().move(common.mySub(self.position,
                (self.scaledImage.get_width() / 2,
                self.scaledImage.get_height() / 2)))
        '''
        #return Rect(x(self.position) - self.scaledImage.get_width() / 2,
                #y(self.position) - self.scaledImage.get_height() / 2,
                #self.scaledImage.get_width(), self.scaledImage.get_height())

    def getLargeRect(self):
        #Next line is a bit hacky, designed to make up for glitchy
        #highlights being off.  Shouldn't matter too much since I won't
        #be including highlights in the final version.
        extra = Canvas.scale * 6 * Tile.HILIGHT_WIDTH
        '''
        return Rect(x(self.position) - (self.scaledImage.get_width() + extra) /
                2, y(self.position) - (self.scaledImage.get_height() + extra) /
                2, self.scaledImage.get_width() + extra,
                self.scaledImage.get_height() + extra)
        '''
        return self.getSmallRect().inflate(extra, extra)

    def printGroup(self):
        #if self is not None:
        #'''
        for tile in self.tileGroup:
            print(tile.position)
        print("")
        #'''

class GroupGrid:
    def __init__(self, tiles):
        self.minX = self.minY = float("inf")
        self.maxX = self.maxY = float("-inf")
        self.tiles = tiles
        for tile in tiles:
            if common.x(tile.absPosition) < self.minX:
                self.minX = common.x(tile.absPosition)
                xMinTile = tile
            if common.x(tile.absPosition) > self.maxX:
                self.maxX = common.x(tile.absPosition)
                yMinTile = tile
            if common.y(tile.absPosition) < self.minY:
                self.minY = common.y(tile.absPosition)
            if common.y(tile.absPosition) > self.maxY:
                self.maxY = common.y(tile.absPosition)
        #print(int(round(
                #(maxY - minY) / tiles[0].image.get_width())) + 1)
        #rows = int(round((maxY - minY) / tiles[0].image.get_width())) + 1
        #cols = int(round((maxX - minX) / tiles[0].image.get_height())) + 1
        rows = self.getTileIndex("y", self.maxY) + 1
        cols = self.getTileIndex("x", self.maxX) + 1
        #groupGrid = [[None for i in range(cols)] for j in range(rows)]
        self.grid = common.makeGrid(rows, cols, None)
        #print(groupGrid)
        #print(int((y(tile.absPosition) - minY + .1 *
                    #tile.image.get_height()) // tile.image.get_height()))
        minXsRow = self.getTileIndex("y", common.y(yMinTile.absPosition))
        for tile in tiles:
            yIndex = self.getTileIndex("y", common.y(tile.absPosition))
            xIndex = self.getTileIndex("x", common.x(tile.absPosition),
                    minXsRow, yIndex)
            self.grid[yIndex][xIndex] = tile

    def getTileIndex(self, xOrY, loc, minXsRow=None, yIndex=None):
        if xOrY == "x":
            resolution = Tile.ADJ_WIDTH
            if minXsRow is None:
                myMin = self.minX
            else:
                if (yIndex - minXsRow) % 2 == 0:
                    myMin = self.minX
                else:
                    myMin = self.minX + Tile.ADJ_WIDTH / 2
        elif xOrY == "y":
            resolution = common.y(self.tiles[0].upperLeft.offset) + \
                    Tile.ADJ_HEIGHT
            myMin = self.minY
        return int((loc - myMin + .1 * resolution) // resolution)

    #def getCoord(self, loc):
        #return(self.getTileIndex("x", loc), self.getTileIndex("y", loc))

#'''
class Icon:
    PLAY_IMAGE = misc.load("play.png")
    PAUSE_IMAGE = misc.load("pause.png")
    PLAY = 0
    PAUSE = 1
    def __init__(self, myType, position, width, height, canvas):
        self.canvas = canvas
        self.position = position
        if myType == Icon.PLAY:
            image = Icon.PLAY_IMAGE
        elif myType == Icon.PAUSE:
            image = Icon.PAUSE_IMAGE
        self.myType = myType
        self.image = pygame.transform.smoothscale(image, (width, height))
        #self.rect = image.get_rect().move(position)
        #print(self.rect)
        self.mouseOffset = None
        self.oldRect = None

    def setPlay(self):
        self.myType = Icon.PLAY
        self.image = pygame.transform.smoothscale(Icon.PLAY_IMAGE,
                (self.image.get_width(), self.image.get_height()))

    def setPause(self):
        self.myType = Icon.PAUSE
        self.image = pygame.transform.smoothscale(Icon.PAUSE_IMAGE,
                (self.image.get_width(), self.image.get_height()))

    def getRect(self):
        #return Rect(x(self.position) - self.image.get_width() / 2,
                #y(self.position) - self.image.get_height() / 2,
                #self.image.get_width(), self.image.get_height())
        return self.image.get_rect().move(common.mySub(self.position,
                (self.image.get_width() / 2, self.image.get_height() / 2)))

    def draw(self):
        #print(self.position, self.image.get_rect())
        self.canvas.windowSurface.blit(self.image, common.mySub(self.position,
                    (self.image.get_width() / 2, self.image.get_height() / 2)))
#'''
