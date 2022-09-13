from panda3d.core import DirectionalLight

from .tools import load_as_dict
from game.items.items import ItemGui
from game.map.construct import MeshMap
from game.map.walkers import CameraWalker

class Game():
    def __init__(self):
        tiles = load_as_dict("assets/bam/tiles.bam")
        self.map = MeshMap(tiles)
        self.map.root.reparent_to(render)

        self.make_celest()

        self.player = CameraWalker(self.map.tilemap)
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

        base.gui = ItemGui()
