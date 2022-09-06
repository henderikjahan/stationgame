from panda3d.core import NodePath, Vec2, Vec3
from panda3d.core import PointLight

from .common import DIRS, OPPO
from game.tools import roundvec


class TileWalker:
    def __init__(self, tiles):
        self.tiles = tiles
        self.root = NodePath("walker")
        self.direction = 0

    def set_pos(self, x, y):
        self.root.set_pos(x, -y, 0)

    def forward(self, duration=0.3):
        x, y = DIRS["nesw"[self.direction]]
        start_pos = roundvec(self.root.get_pos())
        next_pos = Vec3(start_pos.x+x,start_pos.y+y, 0)
        tile = self.tiles[next_pos.x, -next_pos.y]
        if not tile.char == "#":
            return self.root.posInterval(duration, next_pos, startPos=start_pos)

    def turn(self, a=1, duration=0.3):
        self.direction += a
        self.direction %= 4
        start_hpr = roundvec(self.root.get_hpr(render))
        next_hpr = start_hpr+Vec3(a*-90, 0, 0)
        return self.root.quatInterval(duration, next_hpr, startHpr=start_hpr, blendType='easeOut')


class CameraWalker(TileWalker):
    def __init__(self, tiles):
        super().__init__(tiles)
        base.cam.reparent_to(self.root)
        base.cam.set_pos(0,0,0.5)
        base.camLens.set_near(0.1)
        base.camLens.set_fov(90)
        base.task_mgr.add(self.update)
        self.light = self.root.attach_new_node(PointLight("walker"))
        self.light.node().set_attenuation(Vec3(0.1,0.1,0.1))
        render.set_light(self.light)

    def update(self, task):
        if base.sequencer.running:
            return task.cont
        context = base.device_listener.read_context("player")
        if context["moveforward"]:
            base.sequencer.add(self.forward())
        elif context["turnright"]:
            base.sequencer.add(self.turn())
        elif context["turnleft"]:
            base.sequencer.add(self.turn(-1))

        return task.cont
