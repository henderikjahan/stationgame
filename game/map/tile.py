from random import randint
from panda3d.core import Vec3

class Tile():
    def __init__(self):
        self.char = "#"
        self.solid = True


class TileWall(Tile):
    pass


class TileSpace(Tile):
    def __init__(self):
        self.char = " "
        self.solid = False


class TileDoor(Tile):
    def __init__(self):
        self.char = "+"
        self.is_open = False
        self.solid = True
        self.door = None

    def open(self, duration):
        self.is_open = True
        self.solid = False
        start_pos = self.door.get_pos()
        next_pos = start_pos + Vec3(0,0,2)
        base.sequencer.add(self.door.posInterval(duration, next_pos, startPos=start_pos))


class TileBillboardProp(Tile):
    def __init__(self):
        self.char = "%"
        self.solid = True
        # TODO: randomize U
        if randint(0,1):
            self.size = "tall"
            self.uv = 0, 6
        else:
            self.size = "short"
            self.uv = 0, 7
