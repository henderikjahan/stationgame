from random import randint
from panda3d.core import Vec3


class Tile():
    def __init__(self):
        self.char = "#"
        self.solid = True
        self.g_score = float('inf')
        self.f_score = float('inf')

    def set(self, grid, pos):
        self.pos = pos
        self.neighbors = []
        for dx, dy in [(-1,-1),(0,-1),(1,-1),(-1,0), (1,0), (-1,1),(0,1),(1,1)]:
            x, y = pos[0]+dx, pos[1]+dy
            if x >= 0 and y >= 0:
                self.neighbors.append(grid[x,y])

class TileWall(Tile):
    pass


class TileSpace(Tile):
    def __init__(self):
        self.char = " "
        self.solid = False


class TileDoor(Tile):
    def __init__(self):
        self.char = "+"
        self.type = "center"
        self.is_open = False
        self.solid = True
        self.door = None

    def open(self, duration):
        self.is_open = True
        self.solid = False
        start_pos = self.door.get_pos()
        next_pos = start_pos + Vec3(0,0,2)
        self.door.play(self.type+"_open")


class TileBillboardProp(Tile):
    def __init__(self):
        self.char = "%"
        self.solid = True
        # TODO: randomize U
        if randint(0,1):
            self.size = "tall"
            self.uv = 0, 1
        else:
            self.size = "short"
            self.uv = 0, 2
