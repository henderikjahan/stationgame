import sys
from direct.showbase.ShowBase import ShowBase

sys.path.append('..')
from game.audio.sunvoxer import Sunvoxer

base = ShowBase()
base.sunvoxer = Sunvoxer("test.sunvox")
base.run()
