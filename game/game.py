from panda3d.core import DirectionalLight
from panda3d.core import CardMaker

from .tools import load_as_dict
from game.map.construct import MeshMap
from game.map.walkers import CameraWalker


class Game():
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

        self.player = CameraWalker(self.map.tilemap, camera)
        self.player.root.reparent_to(render)
        self.player.set_pos(*self.map.start)
        render.ls()

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
