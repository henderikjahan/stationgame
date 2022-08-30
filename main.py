import sys

from panda3d.core import loadPrcFile
from panda3d.core import LineSegs
from panda3d.core import CardMaker
from panda3d.core import AntialiasAttrib
from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import Parallel
#from keybindings.device_listener import add_device_listener
#from keybindings.device_listener import SinglePlayerAssigner

from game import Game
from game.tools import load_as_dict


class Sequencer():
    def __init__(self):
        self.length = 0.5
        self.wait = self.length
        self.parallel = None

    def end(self):
        self.wait = self.length
        self.parallel = None

    def hold(self, time):
        self.wait = time
        self.add_to_sequence()

    def add_to_sequence(self, *kwargs):
        if not self.parallel:
            self.parallel = Parallel()
        for item in kwargs:
            self.parallel.append(item)

    def finalize(self):
        if not self.parallel:
            self.parallel = Parallel()
        func = Sequence(Wait(self.wait), Func(self.end))
        self.parallel.append(func)
        self.parallel.start()


loadPrcFile("config.prc")
base = ShowBase()
base.win.set_clear_color((0.1,0.1,0.1,1))
#add_device_listener(assigner=SinglePlayerAssigner())
base.accept("escape", sys.exit)
base.transitions = Transitions(loader)
base.cardmaker = CardMaker("card")
base.cardmaker.set_frame(-1,1, -1,1)
base.linemaker = LineSegs("line")
base.linemaker.set_thickness(1)
base.sequencer = Sequencer()
base.render.set_antialias(AntialiasAttrib.MNone)
base.game = Game()
base.run()
