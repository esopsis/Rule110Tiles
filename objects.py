from __future__ import division
import pygame
import common
import drawers
import misc

# An object which has tiles drawn on it
class Canvas:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SNAP_DISTANCE = 300
    scale = .04
    BACK_COLOR = WHITE
    LEFT = 1
    RIGHT = 3
    PLAY_AREA_FACTOR = .5

    def __init__(self, windowSurface):
        self.windowSurface = windowSurface
        self.WIDTH = windowSurface.get_width()
        self.HEIGHT = windowSurface.get_height()
        self.isMouseDown = self.isLDown = self.isRDown = False
        windowSurface.fill(Canvas.BACK_COLOR)
        self.tilePallet = []
        for i in range(len(TileSet.palletImgs)):
            image = TileSet.palletImgs[i]
            tile = Tile(self, image, (i * Tile.ADJ_WIDTH, 0), False)
            self.tilePallet.append(tile)
        self.oldMouseLoc = None
        self.lastTick = pygame.time.get_ticks()
        #Time for each step of auto arranging function, in seconds.
        self.ARRANGE_TIME = 480
        self.rules = {"000": 0, "001": 1, "010": 1, "011": 1, "100": 0,
                "101": 1, "110": 1, "111": 0}

# Represents one side of a tile
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
        self.color = None
        self.type = myType
        self.adjType = Side.toAdjacents[myType]
        self.isSnapped = False
        self.adjSide = None
        self.corner = corner
        self.tile = corner.tile
        self.myCanvas = self.tile.myCanvas

    def setColor(self, tileColors):
        self.color = tileColors[self.type]

# Keeps track of teach of the tiles
class TileSet:
    palletFiles = ["bY.png", "y.png", "rYB.png", "rY.png", "rB.png", "bR.png",
            "w.png"]
    palletImgs = [misc.load(image) for image in palletFiles]
    bY = palletImgs[0]
    y = palletImgs[1]
    rYB = palletImgs[2]
    rY = palletImgs[3]
    rB = palletImgs[4]
    bR = palletImgs[5]
    w = palletImgs[6]

# A corner of a tile
class Corner:
    UPPER_LEFT = 0
    UPPER_RIGHT = 1
    LOWER = 2

    def __init__(self, myType, tile):
        self.tile = tile
        self.myCanvas = tile.myCanvas
        self.adjRadius = Tile.ABS_RADIUS - Tile.LINE_WIDTH / 3 ** .5
        self.gridRow = None
        self.gridCol = None
        self.isSnapped = False
        if myType == Corner.UPPER_LEFT:
            self.offset = (-Tile.ADJ_WIDTH / 2, -Tile.ADJ_HEIGHT / 4)
            self.rightSide = Side(Side.UPPER_LEFT, self)
            self.leftSide = Side(Side.LEFT, self)
        elif myType == Corner.UPPER_RIGHT:
            self.offset = (Tile.ADJ_WIDTH / 2, -Tile.ADJ_HEIGHT / 4)
            self.leftSide = Side(Side.UPPER_RIGHT, self)
            self.rightSide = Side(Side.RIGHT, self)
        elif myType == Corner.LOWER:
            self.offset = (0, Tile.ADJ_HEIGHT / 2)
            self.leftSide = Side(Side.LOWER_LEFT, self)
            self.rightSide = Side(Side.LOWER_RIGHT, self)
        self.sides = [self.leftSide, self.rightSide]

    def getAbsPosition(self):
        return map(int, map(round, common.myAdd(self.tile.absPosition,
                self.offset)))

    # absPosition with zooming applied to it
    def getPosition(self):
        return map(int, map(round, common.adjToScreen(self.getAbsPosition(),
                Canvas.scale, self.myCanvas.WIDTH, self.myCanvas.HEIGHT)))

    # The offset between the center of a tile and the corner
    def getOffset(self):
        return common.myMult(Canvas.scale, self.offset)

# A tile object
class Tile:
    LINE_WIDTH = 20
    DEL_TILE_TRANSPARENCY = 116
    delTile = misc.load("delTile.png")
    TILE_WHITE = 0
    RED = 1
    YELLOW = 2
    BLUE = 3
    ADJ_WIDTH = TileSet.w.get_width() - LINE_WIDTH
    ADJ_HEIGHT = TileSet.w.get_height() - LINE_WIDTH * 2 / 3**.5
    ABS_RADIUS = TileSet.w.get_height() / 2
    tileToColors = {TileSet.rB : [TILE_WHITE, TILE_WHITE, RED, TILE_WHITE,
            BLUE, RED], TileSet.bY : [YELLOW, BLUE, TILE_WHITE, TILE_WHITE,
            BLUE, TILE_WHITE], TileSet.rYB : [TILE_WHITE, BLUE, RED, YELLOW,
            TILE_WHITE, RED], TileSet.rY : [TILE_WHITE, TILE_WHITE, RED,
            YELLOW, TILE_WHITE, RED], TileSet.bR : [TILE_WHITE, BLUE,
            TILE_WHITE, TILE_WHITE, BLUE, RED], TileSet.y : [YELLOW, BLUE, RED,
            YELLOW, TILE_WHITE, TILE_WHITE], TileSet.w : [TILE_WHITE,
            TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE, TILE_WHITE]}

    def __init__(self, myCanvas, image = None, absPosition = None, \
            isMovable = True):
        self.myCanvas = myCanvas
        self.absPosition = absPosition
        self.mouseOffset = None
        self.isMovable = isMovable
        self.gridRow = self.gridCol = None
        self.groupOffset = None
        self.isToDel = self.isToPlay = self.isInPlayGroup = False
        self.image = None
        if isMovable:
            self.upperLeft = None
            self.upperLeft = Corner(Corner.UPPER_LEFT, self)
            self.upperRight = Corner(Corner.UPPER_RIGHT, self)
            self.lower = Corner(Corner.LOWER, self)
            self.corners = [self.upperLeft, self.upperRight, self.lower]
            self.sides = []
            self.sides.append(self.upperRight.leftSide)
            self.sides.append(self.upperRight.rightSide)
            self.sides.append(self.lower.rightSide)
            self.sides.append(self.lower.leftSide)
            self.sides.append(self.upperLeft.leftSide)
            self.sides.append(self.upperLeft.rightSide)
            self.tileGroup = [self]
            self.sideOptions = {
                    Side.UPPER_RIGHT : self.upperRight.leftSide,
                    Side.RIGHT : self.upperRight.rightSide,
                    Side.LOWER_RIGHT : self.lower.rightSide,
                    Side.LOWER_LEFT : self.lower.leftSide,
                    Side.LEFT : self.upperLeft.leftSide,
                    Side.UPPER_LEFT : self.upperLeft.rightSide}
            self.image = Tile.delTile
        if image is not None:
            self.setImage(image)
        if absPosition is not None:
            self.scalePosition(Canvas.scale)
        self.adjTile = None

    def setImage(self, image):
        if image is not self.image:
            self.image = image
            if self.isMovable:
                for side in self.sides:
                    side.setColor(Tile.tileToColors[self.image])

    def isSnapped(self):
        for side in self.sides:
            if side.isSnapped:
                return True
        return False

    def unSnapSides(self):
        for side in self.sides:
            side.isSnapped = False
            if side.adjSide is not None:
                side.adjSide.isSnapped = False
                side.adjSide.adjSide = None
                side.adjSide = None

    def unSnap(self):
        self.tileGroup.remove(self)
        self.adjTile = None
        self.unSnapSides()
        self.tileGroup = [self]

    def setPosition(self, position):
        self.position = position
        self.absPosition = map(int, map(round, common.myDiv(common.mySub(
                position, (self.myCanvas.WIDTH / 2, self.myCanvas.HEIGHT / 2)),
                Canvas.scale)))
        self.scalePosition(Canvas.scale)

    def getPosition(self):
        return self.position

    # Moves one corner of a tile to a point, and moves the rest of the
    # tile along with it
    def matchCorner(self, corner, adjPoint):
        self.absPosition = map(int, map(round, common.mySub(adjPoint,
                corner.offset)))
        self.scalePosition(Canvas.scale)

    def isFree(self):
        for side in self.sides:
            if not side.isSnapped:
                return True
        return False

    def draw(self):
        self.myCanvas.windowSurface.blit(self.scaledImage, self.getRect())
        if self.isToDel:
            common.blitAlpha(self.myCanvas.windowSurface, self.scaledDelTile,
                    self.getRect(), Tile.DEL_TILE_TRANSPARENCY)

    def scaleImage(self, scale):
        self.adjWRad = Tile.ADJ_WIDTH * scale * .5
        self.adjHRad = Tile.ADJ_HEIGHT * scale * .5
        self.adjWidth = int(round(common.x(self.position) + self.adjWRad)) - \
                int(round(common.x(self.position) - self.adjWRad)) + 1
        self.adjHeight = int(round(common.y(self.position) + self.adjHRad)) - \
                int(round(common.y(self.position) - self.adjHRad)) + 1
        self.scaledImage  = pygame.transform.smoothscale(self.image,
            (self.adjWidth, self.adjHeight))

    def resize(self, scale):
        self.scaleImage(scale)
        self.radius = self.adjHeight / 2
        self.scaledDelTile = pygame.transform.smoothscale(Tile.delTile,
                (self.adjWidth, self.adjHeight))

    def scalePosition(self, scale):
        self.position = common.myMult(scale, self.absPosition)
        if self.isMovable:
            self.position = common.myAdd(self.position,
                    (self.myCanvas.windowSurface.get_width() / 2,
                     self.myCanvas.windowSurface.get_height() / 2))
        else:
            self.position = common.myAdd(self.position,
                    common.myMult(Canvas.scale, (self.image.get_width() / 2,
                    self.image.get_height() / 2)))
        self.resize(scale)

    def getSide(self, myType):
        return self.sideOptions[myType]

    def getRect(self):
        return pygame.Rect(map(int, map(round,
                common.mySub(self.position, (self.adjWRad, self.adjHRad)))),
                (self.adjWidth, self.adjHeight))
