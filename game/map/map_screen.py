from panda3d.core import LineSegs


class MapScreen:
    def __init__(self, tilemap):
        self.root = base.aspect2d.attach_new_node("map screen")
        self.root.set_scale(0.04)
        self.root.set_z(-0.5)

        self.cursor = base.loader.load_model("models/smiley")
        self.cursor.reparent_to(self.root)
        self.cursor.set_scale(0.5)
        
        self.line_segs = LineSegs("map lines")
        self.line_segs.set_color((1,0,1,1))
        self.tilemap = tilemap
        self.explored = []
            
    def draw_tile(self, a):
        print("drawing corridor")
        pass
        
    def draw_leaf(self, leaf):
        print("drawing leaf")
        x, y, w, h = leaf.x, leaf.y, leaf.w, leaf.h
        self.line_segs.move_to(x,0,y)
        self.line_segs.draw_to(x+w,0,y)
        self.line_segs.draw_to(x+w,0,y+h)
        self.line_segs.draw_to(x,0,y+h)
        self.line_segs.draw_to(x,0,y)
        self.root.attach_new_node(self.line_segs.create())
        #self.root.flatten_strong()

    def update(self, x, y):
        self.cursor.set_pos(x+0.5,0,y+0.5)
        leaf = self.tilemap.get_leaf(x, y)
        if leaf:
            if not leaf in self.explored:
                self.draw_leaf(leaf)
                self.explored.append(leaf)
                return
        corridor = None
        if corridor:
            if not corridor in self.explored:
                self.draw_tile(corridor)
                self.explored.append(leaf)
                return