from panda3d.core import DirectionalLight
from panda3d.core import CardMaker
from panda3d.core import Fog

from game.audio.sunvoxer import Sunvoxer


class Game:
    def __init__(self):
        self.sunvoxer = Sunvoxer("friendly.sunvox")
        data_mgr.build_level("start")
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
