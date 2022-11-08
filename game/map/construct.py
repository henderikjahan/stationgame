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
        self.tilemap = BSP()
        self.start = choice(list(self.tilemap.tiles.keys()))

        self.rooms = {}
        for room in self.tilemap.rooms+[None]:
            root = self.root.attach_new_node(str(room))
            self.rooms[room] = {
                "root": root,
                "flat": root.attach_new_node("flat"),
                "dynamic":root.attach_new_node("animated"),
            }

        self.build_map(self.tilemap.tiles)
        for key, value in self.rooms.items():
            value["flat"].flatten_strong()

    def print_out(self):
        for y in range(0,32):
            s = ""
            for x in range(0,32):
                s += self.tilemap.tiles[x, y].char
            print(s)

    def build_tile(self, x, y, tile_name, direction=0, frames=[]):
        # TODO: if len(frames) > 1: it's an animated tile
        room = self.rooms[self.tilemap.get_room_bordered(x, y)]
        tile = self.tiles[tile_name].copy_to(room['flat'])
        tile.set_pos(x, -y, 0)
        tile.set_h((-direction)*90)
        tile_texture(tile, self.texture, *frames[0], 8)
        return tile

    def build_floor_ceiling(self, x, y):
        for i, name in enumerate(("ceiling", "floor")):
            name = name+"_even" if (x+y)%2 else name+"_uneven"
            tx = choice((0,2,3,4)) if randint(0,4) == 0 else 0
            if (x+y)%2 and randint(0,2): tx = 1
            tile = self.build_tile(x, y, name, frames=[(tx,4*i)])

    def build_wall(self, x, y, tile_name, direction):
        u = randint(0,3) if tile_name == "l_none_r_none" and randint(0,1) else 0
        tile = self.build_tile(x, y, tile_name, direction, [(u, 2)])
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
        d = 1 if tiles[x,y-1].char == "#" else 0
        tile = tiles[x,y]
        shape = self.build_tile(x, y, 'doorway', d, frames=[(0,2)])
        tile.door = shape.find("**/door")
        tile_texture(tile.door, self.texture, 5,0, 8)
        tile.door.wrt_reparent_to(self.root)
        self.build_floor_ceiling(x, y)

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
