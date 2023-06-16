from random import seed
import sys
sys.path.append("..")

from random import choice
from direct.showbase.ShowBase import ShowBase
from game.tools import load_as_dict
from game.map.construct import MeshMap
from game.map.path import a_star


seed(10)
base = ShowBase()

print("meshing")
map = MeshMap(load_as_dict("../assets/bam/tiles.bam"), "../assets/images/")
print("picking")
a = choice(map.floors)
b = choice(map.floors)
print(a,b)
print("finding path...")
print(a_star(map.tilemap.tiles, a, b))
# At the moment the tile's neighbors are always walls,
# this means they are either not set yet, or they are set
# wrong. Go back in their and set the correct neighbors.
