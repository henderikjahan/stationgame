from collections import defaultdict
from random import randint

'''
# This is an old generator of mostly random shapes clumped together
# but contains a maze generator that could prove useful
class OldGenMap():
    def __init__(self):
        self.start = Vec2(17,1)
        self.cursor = Vec2(self.start)
        self.stack = []

        self.step_size = 2
        self.size = size = 32
        self.grid = grid = []
        for y in range(size):
            grid.append([])
            for x in range(size):
                if Vec2(x,y) == self.start:
                    grid[y].append("S")
                else:
                    grid[y].append("#")

    def print(self):
        for i in self.grid:
            print("".join(i))

    def clear(self):
        for y in range(self.size):
            for x in range(self.size):
                if not self.grid[y][x] == "S":
                    self.grid[y][x] = " "

    def take_step(self, direction, char=" "):
        for i in range(self.step_size):
            self.cursor += direction
            self.grid[int(self.cursor.y)][int(self.cursor.x)] = char

    def step(self):
        directions = ['n', 'e', 's', 'w']
        shuffle(directions)
        while len(directions):
            direction = DIRS[directions.pop(0)]
            go_toward = self.cursor+(direction*self.step_size)
            if not is_in(go_toward.x, go_toward.y, self.size) or not self.grid[int(go_toward.y)][int(go_toward.x)] == "#":
                continue
            else:
                self.take_step(direction, " ")
                self.stack.append(Vec2(self.cursor))
                return True

    def walk_maze(self):
        while True:
            if not self.step():
                if len(self.stack):
                    self.cursor = self.stack.pop()
                else:
                    break

    def carve_room(self, pos, scale, char = " "):
        scale = evenvec2(scale)
        pos = evenvec2(pos)
        for y in range(int(scale.y)):
            for x in range(int(scale.x)):
                p = Vec2(x+pos.x, y+pos.y)
                if not p.x == 0 and not p.y == 0:
                    self.grid[int(p.y)][int(p.x)] = char

    def carve_rooms(self, room_grid=[4,4], chance=1):
        min_size = Vec2(4,4)
        max_size = Vec2(int((self.size+1)/room_grid[0]), int((self.size+1)/room_grid[1]))
        for y in range(room_grid[1]):
            for x in range(room_grid[0]):
                # TODO: check what room the start_tile is in and skip that one instead
                if not (y == 0 and x == 2):
                    if randint(0,1):
                        size = evenvec2(Vec2(randint(min_size.x, max_size.x), randint(min_size.y, max_size.y)))
                        offset = ((max_size-size)*0.5)
                        pos = evenvec2(multvec2(Vec2(x,y), max_size)+offset)
                        self.carve_room(pos, size)

    def seal(self):
        for y in range(self.size):
            self.grid[y][0] = "#"
            self.grid[y].append("#")
        self.grid.append([])
        for x in range(self.size+1):
            self.grid[0][x] = "#"
            self.grid[self.size].append("#")
'''
            
            
class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def area(self):
        return self.w*self.h

    def center(self):
        return int(self.x+(self.w/2)), int(self.y+(self.h/2))

    def random_point(self):
        return randint(self.x+1, self.x+self.w-2), randint(self.y+1, self.y+self.h-2)

    def __add__(self, other):
        return Rect(self.x+other.x, self.y+other.y, self.w+other.w, self.h+other.h)

    def __sub__(self, other):
        return Rect(self.x-other.x, self.y-other.y, self.w-other.w, self.h-other.h)

    def __mult__(self, other):
        return Rect(self.x*other.x, self.y*other.y, self.w*other.w, self.h*other.h)

    def __iter__(self):
        return iter((self.x, self.y, self.w, self.h))

    def __get_item__(self, index):
        return [self.x, self.y, self.w, self.h][index]

    def __str__(self):
        return "x:{}\ty:{}\tw:{}\th:{}".format(self.x, self.y, self.w, self.h)

    def set(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def split_w(self, i):
        if i > self.w:
            raise ValueError("Can't split rect by {}".format(i))
        rect_a, rect_b = Rect(*self), Rect(*self)
        rect_a.w = i
        rect_b.w = self.w-i
        rect_b.x += i
        return rect_a, rect_b

    def split_h(self, i):
        if i > self.h:
            raise ValueError("Can't split rect by {}".format(i))
        rect_a, rect_b = Rect(*self), Rect(*self)
        rect_a.h = i
        rect_b.h = self.h-i
        rect_b.y += i
        return rect_a, rect_b


class BSP:
    def __init__(self, rect=Rect(0,0,64,64), root=None, parent=None):
        self.rect = self.original_rect = rect
        self.connected = False
        self.parent = parent
        if root:
            self.root = root
        else:
            self.root = self
            self.leafs = []
        self.min = 4
        self.split()

    def split(self):
        minn = self.min
        if self.rect.h-minn >= minn and self.rect.w-minn >= minn:
            if self.rect.w > self.rect.h:
                a,b = self.rect.split_w(randint(minn, self.rect.w-minn))
                split = 0
            else:
                a,b = self.rect.split_h(randint(minn, self.rect.h-minn))
                split = 1
            self.a, self.b = BSP(a, self.root, self), BSP(b, self.root, self)
            self.a.split = self.b.split = split
            self.a.sibling, self.b.sibling = self.b, self.a
        else:
            self.root.leafs.append(self)

    def random_shrink(self):
        self.original_rect = Rect(*self.rect)
        w, h = randint(self.min, self.rect.w), randint(self.min, self.rect.h)
        self.rect.set(
            randint(self.rect.x, self.rect.x+(self.rect.w-w)),
            randint(self.rect.y, self.rect.y+(self.rect.h-h)),
            w, h
        )

    def make_corridor(self):
        self.connected = self.sibling.connected = True
        a = list(self.rect.random_point())
        b = list(self.sibling.rect.random_point())
        corridor = []
        while True:
            corridor.append(a[:])
            if a == b:
                return corridor
            if a[0] < b[0]:
                a[0] += 1
            elif a[0] > b[0]:
                a[0] -= 1
            elif a[1] < b[1]:
                a[1] += 1
            elif a[1] > b[1]:
                a[1] -= 1

    def get_corridor(self, corridors):
        if not self.connected and self.parent:
            corridors.append(self.make_corridor())
        if self.parent:
            self.parent.get_corridor(corridors)

    def get_corridors(self):
        corridors = []
        for leaf in self.leafs:
            leaf.get_corridor(corridors)
        return corridors


class Tile:
    def __init__(self, char="#"):
        self.solid = True
        self.char = char


class TileMap:
    def __init__(self):
        self.tiles = defaultdict(Tile)
        self.corridors = []
        self.bsp = BSP(rect=Rect(0,0,32,32))
        for leaf in self.bsp.leafs:
            leaf.random_shrink()
        self.corridors = self.bsp.get_corridors()
        self.apply_bsp()
        self.start = (0,0,0)

    def apply_bsp(self):
        for leaf in self.bsp.leafs:
            for sx in range(leaf.rect.w-1):
                for sy in range(leaf.rect.h-1):
                    self.tiles[sx+leaf.rect.x, sy+leaf.rect.y].char = " "
        for corridor in self.corridors:
            for step in corridor:
                self.tiles[step[0], step[1]].char = " "

    def __str__(self, rect=Rect(0,0,80,64)):
        a = ""
        for sy in range(rect.h):
            s = ""
            for sx in range(rect.w):
                s += self.tiles[sx+rect.x, sy+rect.y].char
            a += s+'\n'
        return a


if __name__ == "__main__":
    gmap = Map()
    gmap.apply_bsp()
    print(gmap)
