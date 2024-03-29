from panda3d.core import NodePath, Vec2, Vec3
from panda3d.core import PointLight
from direct.interval.IntervalGlobal import Func

from .common import DIRS, OPPO
from game.tools import roundvec
from game.gui.map_screen import MapScreen


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
    def __init__(self, tilemap, camera):
        super().__init__(tilemap)
        camera.reparent_to(self.root)
        camera.set_pos(0,0,1)
        camera.node().get_lens().set_near(0.1)
        camera.node().get_lens().set_fov(90)

        self.light = self.root.attach_new_node(PointLight("walker"))
        self.light.set_z(1)
        self.light.node().set_attenuation(Vec3(0.05,0.05,0.05))
        render.set_light(self.light)
        self.map_screen = MapScreen(tilemap, camera)
        self.next_move = None

    def update(self):
        return self.movement()

    def queue_input(self):
        context = base.device_listener.read_context("player")
        turn_movement = ["turnright", "turnleft"]
        move_movement = ["moveforward", "movebackward"]
        for i in turn_movement:
            if context[i]:
                self.next_move = i
                return
        if not base.sequencer.running and not self.next_move in turn_movement:
            for i in move_movement:
                if context[i]:
                    self.next_move = i

    def movement(self):
        self.queue_input()
        if base.sequencer.running or not self.next_move:
            return

        if self.next_move == "turnright":
            self.rotate(1)
            x,y,z = self.root.get_pos()
            self.map_screen.update(x, -y, self.direction)
        elif self.next_move == "turnleft":
            self.rotate(-1)
            x,y,z = self.root.get_pos()
            self.map_screen.update(x, -y, self.direction)
        elif self.next_move == "moveforward":
            pos = self.forward()
            if pos:
                x,y,z = pos
                self.map_screen.update(x, -y, self.direction)
        else:
            return
        self.next_move = None
        return True
