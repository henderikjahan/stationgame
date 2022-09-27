from random import shuffle, randint, choice
from panda3d.core import LVector2i, Vec2
from panda3d.core import NodePath

from game.tools import multvec2, evenvec2, is_in, rotate_mat3, tile_texture
from .common import DIRS
from .bsp import BSP


class MeshMap():
    def __init__(self, tiles, texture):
        self.tiles = tiles
        self.texture = texture
        self.root = NodePath("map")
        self.flattened = self.root.attach_new_node("flattened")
        self.tilemap = BSP()
        self.start = choice(list(self.tilemap.tiles.keys()))
        self.build_map(self.tilemap.tiles)
        self.flattened.flatten_strong()
        
        for y in range(0,32):        
            s = "" 
            for x in range(0,32):
                s += self.tilemap.tiles[x, y].char
            print(s)

    def build_floor_ceiling(self, x, y):
        for i, name in enumerate(("ceiling", "floor")):
            if (x+y)%2:
                name += "_even"
            else:
                name += "_uneven"
            tile = self.tiles[name].copy_to(self.flattened)
            tile.set_pos(x, -y, 0)
            tile_texture(tile, self.texture, 6-i,7+i, 8)

    def build_wall(self, x, y, tile_name, direction):
        tile = self.tiles[tile_name].copy_to(self.flattened)
        tile.set_pos(x, -y, 0)
        tile.set_h((-direction)*90)
        tile_texture(tile, self.texture, 0,4, 8)
        self.build_floor_ceiling(x, y)
        
    def build_walls(self, px, py, tiles):
        # TODO: make this work like this instead:
        # a,b,c,d = int(pos.x-1), int(pos.x+1), int(pos.y-1), int(pos.y+1)
        # sub = [x[a:b] for x in grid[c:d]]
        sub = [[],[],[]]
        for y in range(3):
            for x in range(3):
                sub[y].append(tiles[px-1+x, py-1+y].char)

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
                self.build_wall(px, py, "l_{}_r_{}".format(l, r), -d)
            sub = rotate_mat3(sub)

    def build_doorway(self, x, y, tiles):
        doorway = self.tiles["doorway"].copy_to(self.flattened)
        tile_texture(doorway, self.texture, 0,4, 8)
        tile = tiles[x, y]
        doorway.set_pos(x,-y,0)
        if tiles[x,y-1].char == "#":
            doorway.set_h(90)
        tile.door = doorway.find("**/door")
        tile_texture(tile.door, self.texture, 2,5, 8)
        tile.door.wrt_reparent_to(self.root)
        
    def build_map(self, tiles):
        for x in range(-1,256):
            for y in range(-1,256):
                if tiles[x,y].char == "#":
                    self.build_walls(x, y, tiles)
                elif tiles[x,y].char == "+":
                    self.build_doorway(x,y,tiles)
                else:
                    self.build_floor_ceiling(x, y)


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
