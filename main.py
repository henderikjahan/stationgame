import builtins
import sys

from panda3d.core import loadPrcFile
from panda3d.core import LineSegs
from panda3d.core import CardMaker
from panda3d.core import AntialiasAttrib
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import Parallel, Sequence, Wait, Func
from keybindings.device_listener import add_device_listener
from keybindings.device_listener import SinglePlayerAssigner

from game import Game
from game.tools import load_as_dict
from game.data import DataMgr


class Sequencer():
    def __init__(self):
        self.length = 0.2
        self.wait = self.length
        self.parallel = None
        self.running = False
        base.task_mgr.add(self.update, sort=10000)

    def update(self, task):
        if self.parallel and not self.running:
            self.finalize()
        return task.cont

    def end(self):
        self.wait = self.length
        self.parallel = None
        self.running = False

    def hold(self, time):
        self.wait = time
        self.add_to_sequence()

    def add(self, *kwargs):
        if not self.parallel:
            self.parallel = Parallel()
        for item in kwargs:
            if item:
                self.parallel.append(item)

    def finalize(self):
        if not self.parallel:
            self.parallel = Parallel()
        func = Sequence(Wait(self.wait), Func(self.end))
        self.parallel.append(func)
        self.parallel.start()
        self.running = True


class Printer:
    def __init__(self):
        self.buffer = []

    def print(self, string):
        print("printer:", string)
        self.buffer.append(string)


loadPrcFile(Filename.expand_from("$MAIN_DIR/settings.prc"))
base = ShowBase()
base.win.set_clear_color((0.1,0.1,0.1,1))
add_device_listener(assigner=SinglePlayerAssigner())
base.accept("escape", sys.exit)
base.accept("f12", render.ls)
base.sequencer = Sequencer()
base.transitions = Transitions(loader)
base.cardmaker = CardMaker("card")
base.cardmaker.set_frame(0,0,-1,1)
base.linemaker = LineSegs("line")
base.linemaker.set_thickness(1)
base.render.set_antialias(AntialiasAttrib.MNone)
base.printer = Printer(); base.print = base.printer.print
builtins.data_mgr = base.data_mgr = DataMgr()
base.game = Game()
#render.ls()
base.run()
