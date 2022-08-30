from panda3d.core import NodePath

from .common import DIRS, OPPO
from game.tools import roundvec


class TileWalker:
    def __init__(self, tiles):
        self.tiles = tiles
        self.root = NodePath("walker")
        self.direction = 0

    def set_pos(self, x, y):
        self.root.set_pos(x, -y, 0)

    def forward(self, duration=0.5):
        direction = DIRS.keys()[self.direction]
        x, y = self.root.get_xy()
        y = -(y+DIRS[direction].y)
        x = x + DIRS[direction].x
        tile = self.tiles[x, -y]
        if not tile.char == "#":
            self.root.set_pos(x, y)
        return self.root.posInterval(duration, self.root.get_pos(), startPos=pos)

    def turn(self, a=1, duration=0.5):
        self.direction += a
        hpr = roundvec(self.root.get_hpr(render))
        self.root.set_h(self.root, -90*a)
        return self.root.quatInterval(duration, self.root.get_hpr(), startHpr=hpr, blendType='easeOut')


class CameraWalker(TileWalker):
    def __init__(self, tiles):
        super().__init__(tiles)
        base.cam.reparent_to(self.root)
        base.cam.set_pos(0,0,1)
        base.task_mgr.add(self.update)
        
    def update(self, task):
        context = base.device_listener.read_context("player")
        if context["moveforward"]:
            self.forward()
        elif context["turnright"]:
            base.sequencer.add(self.turn())
        elif context["turnleft"]:
            base.sequencer.add(self.turn(-1))
            
        
        return task.cont