from panda3d.core import NodePath, Vec2, Vec3
from panda3d.core import PointLight
from direct.interval.IntervalGlobal import Func

from .common import DIRS, OPPO
from game.tools import roundvec
from game.map.map_screen import MapScreen


class TileWalker:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.root = NodePath("walker")
        self.direction = 0

    def set_pos(self, x, y):
        self.root.set_pos(x, -y, 0)

    def get_pos(self):
        x,y,z = self.root.get_pos()
        return x, -y
        
    def forward(self, duration=0.2):
        x, y = DIRS["nesw"[self.direction]]
        start_pos = roundvec(self.root.get_pos())
        next_pos = Vec3(start_pos.x+x,start_pos.y+y, 0)
        tile = self.tilemap.tiles[next_pos.x, -next_pos.y]
        if not tile.solid:
            base.sequencer.add(self.root.posInterval(duration, next_pos, startPos=start_pos))
            return next_pos
        elif tile.char == "+" and not tile.is_open:
            tile.open(duration)

    def rotate(self, a=1, duration=0.2):
        self.direction += a
        self.direction %= 4
        start_hpr = roundvec(self.root.get_hpr(render))
        next_hpr = start_hpr+Vec3(a*-90, 0, 0)
        base.sequencer.add(self.root.quatInterval(duration, next_hpr, startHpr=start_hpr, blendType='easeOut'))
        return next_hpr


class CameraWalker(TileWalker):
    def __init__(self, tilemap):
        super().__init__(tilemap)
        base.cam.reparent_to(self.root)
        base.cam.set_pos(0,0,1)
        base.camLens.set_near(0.1)
        base.camLens.set_fov(90)
        base.task_mgr.add(self.update)
        self.light = self.root.attach_new_node(PointLight("walker"))
        self.light.set_z(1)
        self.light.node().set_attenuation(Vec3(0.2,0.1,0.2))
        render.set_light(self.light)

        self.map_screen = MapScreen(tilemap)

    def movement(self):
        context = base.device_listener.read_context("player")
        if context["moveforward"]:
            pos = self.forward()
            if pos:
                x,y,z = pos
                self.map_screen.update(x, -y)
        elif context["turnright"]:
            self.rotate(1)
        elif context["turnleft"]:
            self.rotate(-1)
        else:
            return False
        return True
            
    def update(self, task):
        if base.sequencer.running:
            return task.cont
        self.movement()
        return task.cont
