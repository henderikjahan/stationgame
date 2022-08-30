from panda3d.core import NodePath

from .common import DIRS, OPPO


class GridWalker:
    def __init__(self, grid):
        self.grid = grid
        self.root = NodePath("walker")
        self.direction = 0

    def set_pos(self, v2):
        self.root.set_pos(int(v2.x), -int(v2.y), 0)

    def forward(self, duration):
        direction = DIRS.keys()[self.direction]
        pos = self.root.get_xy()
        pos.y = -pos.y
        next_tile_pos =  pos + DIRS[direction]
        tile = self.grid[-next_tile_pos.y][next_tile_pos.x]
        if not tile == "#":
            self.root.set_pos()
        return self.root.posInterval(duration, self.root.get_pos(), startPos=pos)

    def turn(self, a=1, duration=0.5):
        self.direction += a
        hpr = round_vec(self.root.get_hpr())
        self.root.set_h(self.root, -90)
        return self.root.quatInterval(duration, self.root.get_hpr(), startHpr=hpr, blendType='easeOut')


class CameraWalker(GridWalker):
    def __init__(self, grid):
        super().__init__(grid)
        base.cam.reparent_to(self.root)
        base.cam.set_pos(0,0,1)


