from random import shuffle, randint
from panda3d.core import LVector2i, Vec2
from panda3d.core import NodePath

from game.tools import multvec2, evenvec2, is_in, rotate_mat3
from .common import DIRS

from .generate import TileMap

class MeshMap():
    def __init__(self, tiles):
        self.tiles = tiles
        self.root = NodePath("map")
        self.tilemap = TileMap()
        self.start = self.tilemap.start
        self.build_map(self.tilemap.tiles)

    def build_wall(self, pos, tile_name, direction):
        tile = self.tiles[tile_name].copy_to(self.root)
        tile.set_pos(pos.x*2, -pos.y*2, 0)
        tile.set_h((-direction)*90)
        print("building wall", tile_name, pos)

    def build_walls(self, pos, tiles):
        # TODO: make this work like this instead:
        # a,b,c,d = int(pos.x-1), int(pos.x+1), int(pos.y-1), int(pos.y+1)
        # sub = [x[a:b] for x in grid[c:d]]
        sub = [[],[],[]]
        for y in range(3):
            for x in range(3):
                sub[y].append(tiles[pos.x-1+x, pos.y-1+y].char)

        for d, direction in enumerate(DIRS.keys()):
            l = r = "none"
            if not sub[0][1] == "#":
                if sub[0][0] == "#":
                    l = "out"
                if not sub[1][0] == "#":
                    l = "in"
                if sub[0][2] == "#":
                    r = "out"
                if not sub[1][2] == "#":
                    r = "in"
                self.build_wall(pos, "l_{}_r_{}".format(l, r), -d)
            sub = rotate_mat3(sub)

    def build_tile(self, pos, tiles):
        if tiles[*pos].char == "#":
            self.build_walls(pos, tiles)

    def build_map(self, tiles):
        for tile in tiles:
            self.build_tile(tile, tiles)


if __name__ == "__main__":
    from panda3d.core import DirectionalLight
    from direct.showbase.ShowBase import ShowBase
    from .tools import load_as_dict

    base = ShowBase()
    tiles = load_as_dict("../assets/bam/tiles.bam")
    map = BuildMap(tiles)
    map.root.reparent_to(render)

    sun = render.attach_new_node(DirectionalLight("sun"))
    sun.node().set_color((1,0,1,0.5))
    sun.set_hpr(30,30,30)
    render.set_light(sun)

    moon = sun.attach_new_node(DirectionalLight("moon"))
    moon.node().set_color((0,1,1,0.5))
    moon.set_hpr(0,170,0)
    render.set_light(moon)

    base.run()
