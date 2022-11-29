from panda3d.core import DirectionalLight
from panda3d.core import CardMaker
from panda3d.core import Fog

from game.tools import load_as_dict
from game.tools import render_to_texture
from game.items.items import ItemGui
from game.map.construct import MeshMap
from game.player import Player


class Game:
    def __init__(self):
        self.map = MeshMap(
            load_as_dict("assets/bam/tiles.bam"),
            loader.load_texture("assets/images/tileset_test.png"),
        )
        self.map.root.reparent_to(render)
        self.player = Player(self.map, camera=render_to_texture(render))
        self.make_celest()

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
        fog = Fog("fadefog")
        fog.set_color(0,0,0)
        fog.set_exp_density(0.1)
        render.set_fog(fog)
