from panda3d.core import LineSegs


class MapScreen:
    def __init__(self, tilemap):
        map_scale = 0.06
        self.root = base.aspect2d.attach_new_node("map screen")
        self.root.set_scale(map_scale)
        self.root.set_z(tilemap.h*(map_scale*0.5))
        self.root.set_x(-(tilemap.w*(map_scale*0.5)))

        self.cursor = base.loader.load_model("models/smiley")
        self.cursor.reparent_to(self.root)
        self.cursor.set_scale(0.5)

        self.line_segs = LineSegs("map lines")
        self.line_segs.set_color((1,0,1,1))
        self.tilemap = tilemap
        self.explored = []

    def draw_openings(self, leaf):
        x1,y1,x2,y2 = leaf.x, leaf.y, leaf.x+leaf.w, leaf.y+leaf.h
        for x in range(x1-1, x2+1):
            if not self.tilemap.tiles[x, y1-1].char == "#":
                self.draw_tile(x, y1-1)
            elif not self.tilemap.tiles[x, y2].char == "#":
                self.draw_tile(x, y2)

        for y in range(y1-1, y2+1):
            if not self.tilemap.tiles[x1-1, y].char == "#":
                self.draw_tile(x1-1, y)
            elif not self.tilemap.tiles[x2, y].char == "#":
                self.draw_tile(x2, y)


    def draw_tile(self, x, y):
        if not (x,y) in self.explored:
            tile = self.tilemap.tiles[x, y]
            self.line_segs.set_color((0,1,1,1))
            if tile.char == "+":
                self.line_segs.set_color((1,1,0,1))
            self.line_segs.move_to(x,0, -y)
            self.line_segs.draw_to(x+1,0, -y)
            self.line_segs.draw_to(x+1,0, -(y+1))
            self.line_segs.draw_to(x,0, -(y+1))
            self.line_segs.draw_to(x,0, -y)
            self.root.attach_new_node(self.line_segs.create())
            self.explored.append((x,y))

    def draw_leaf(self, leaf):
        if not leaf in self.explored:
            self.line_segs.set_color((1,0,1,1))
            x1,y1,x2,y2 = leaf.x, leaf.y, leaf.x+leaf.w, leaf.y+leaf.h
            self.line_segs.move_to(x1,0,-y1)
            self.line_segs.draw_to(x2,0,-y1)
            self.line_segs.draw_to(x2,0,-y2)
            self.line_segs.draw_to(x1,0,-y2)
            self.line_segs.draw_to(x1,0,-y1)
            self.root.attach_new_node(self.line_segs.create())
            self.draw_openings(leaf)
            #self.root.flatten_strong()
            self.explored.append(leaf)
            
    def update(self, x, y):
        self.cursor.set_pos(x+0.5,0,-(y+0.5))
        leaf = self.tilemap.get_room(x, y)
        if leaf:
            self.draw_leaf(leaf)
        else:
            self.draw_tile(x,y)