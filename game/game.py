from panda3d.core import DirectionalLight
from panda3d.core import CardMaker

from .tools import load_as_dict
from game.items.items import ItemGui
from game.map.construct import MeshMap
from game.map.walkers import CameraWalker
from game.battle import player_gl, enemies
from game.battle import battle_gameplay as bgp


class Player:
    def __init__(self, map, camera):
        self.walker = CameraWalker(map.tilemap, camera)
        self.walker.root.reparent_to(render)
        self.walker.set_pos(*map.start)
        self.stat = player_gl

        self.battle = None
        self.counter = 0
        base.task_mgr.add(self.update)

    def update(self, task):
        if base.sequencer.running:
            return task.cont

        if self.battle:
            self.battle.battle_turn("attack")
            self.battle =  None
        else:
            if self.counter > 10:
                self.battle = bgp.Battle_Gameplay(
                    player_gl = player_gl,
                    enemies_data = enemies
                )
                self.counter = 0
            if self.walker.movement():
                self.counter += 1
        return task.cont

class Game:
    def __init__(self):
        self.map = MeshMap(
            load_as_dict("assets/bam/tiles.bam"),
            loader.load_texture("assets/images/tileset1.png"),
        )
        self.map.root.reparent_to(render)

        # Render to texture
        cardmaker = CardMaker("card")
        cardmaker.set_frame(-1,1,-1,1)
        screen = base.render2d.attach_new_node(cardmaker.generate())
        buffer = base.win.makeTextureBuffer("Buffer", 256, 256)
        buffer.set_clear_color_active(True)
        buffer.set_clear_color((0,0,0,1))
        texture = buffer.get_texture()
        texture.set_minfilter(0)
        texture.set_magfilter(0)
        screen.set_texture(texture, 1)
        buffer.set_sort(-100)
        camera = base.make_camera(buffer)
        camera.reparent_to(render)

        self.player = Player(self.map, camera)

        render.ls()

        #base.gui = ItemGui()

    def make_celest(self):
        celest = render.attach_new_node('celest')
        sun = celest.attach_new_node(DirectionalLight("sun"))
        sun.node().set_color((1,0,1,0.5))
        render.set_light(sun)
        moon = celest.attach_new_node(DirectionalLight("moon"))
        moon.node().set_color((1,0,1,0.5))
        moon.set_p(180)
        render.set_light(moon)
        celest.set_hpr(30,30,30)

