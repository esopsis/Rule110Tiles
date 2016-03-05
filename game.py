import objects
import checkers
import misc

def checkBordersAdd(canvas, tile, checkedTiles, tileGroup, selectedTiles,
        selectedTile, isSnapped, sidesToSnap, snapdTile, toDraws, tiles, grid,
        gridRes):
    isSnapped, sidesToSnap, snapdTile, isConflict = checkers.checkBordersSnap(
            canvas, None, [tile], checkedTiles, grid, gridRes, False,
            isSnapped, sidesToSnap, snapdTile, selectedTiles)
    if isConflict:
        tile.setImage(objects.TileSet.w)
        tile.scaleImage(objects.Canvas.scale)
    isSnapped, sidesToSnap, snapdTile, isConflict = checkers.checkBordersSnap(
            canvas, None, [tile], checkedTiles, grid, gridRes, False,
            isSnapped, sidesToSnap, snapdTile, selectedTiles)
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
        selectedTile, isSnapped, sidesToSnap, snapdTile, tiles, grid, gridRes):
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
                gridRes)
        #foo
        #print(isConflict)
        #foo
        #print(isConflict)
        #print(sidesToSnap)
    #print("in", tiles)
    return (isConflict, selectedTiles, selectedTile, isSnapped, sidesToSnap,
            snapdTile)

def computerPlay(canvas, inPlay, selectedTiles, selectedTile,
        isSnapped, sidesToSnap, snapdTile, tiles, toDraws, grid, gridRes):
    for tile in inPlay:
        for corner in tile.corners:
            for side in corner.sides:
                if side.adjSide is None:
                    for image in objects.TileSet.palletImgs:
                        newTile = objects.Tile(canvas, image)
                        isConflict, selectedTiles, selectedTile, isSnapped, \
                                sidesToSnap, snapdTile = tryConnectNewTile(
                                canvas, newTile.getSide(side.adjType), side,
                                toDraws, selectedTiles, selectedTile,
                                isSnapped, sidesToSnap, snapdTile, tiles, grid,
                                gridRes)
                        if not isConflict:
                            
                            return (inPlay, selectedTiles, selectedTile,
                                    isSnapped, sidesToSnap, snapdTile)
