# This code is released into the Public Domain.
from collections import defaultdict
from math import sqrt
from random import random
from random import randrange
from random import choice
from random import randint

from .tile import TileWall, TileSpace, TileDoor, TileBillboardProp


class Room:
    def __init__(self, x, y, h, w):
        self.x, self.y, self.h, self.w = x, y, h, w
        self.randint = randint(0,3)

    def __str__(self):
        return str("room:{}-{}-{}-{}".format(self.x, self.y, self.w, self.h))

class BSP:
    def __init__(self, w=30, h=30):
        # Cutoff for when we want to stop dividing sections, should be range
        self.MAX = 8
        self.w, self.h = w, h
        self.leaves = []
        self.tiles = defaultdict(TileWall)
        self.rooms = []
        self.generate_map()

    def get_room_bordered(self, x, y):
        for room in self.rooms:
            if x >= room.x-1 and x < room.x + room.w+1:
                if y >= room.y-1 and y < room.y + room.h+1:
                    return room

    def get_room(self, x, y):
        for room in self.rooms:
            if x >= room.x and x < room.x + room.w:
                if y >= room.y and y < room.y + room.h:
                    return room

    def random_split(self, min_y, min_x, max_y, max_x):
        # We want to keep splitting until the sections get down to the threshold
        seg_height = max_y - min_y
        seg_width = max_x - min_x

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_y, min_x, max_y, max_x))
        elif seg_height < self.MAX and seg_width >= self.MAX:
            self.split_on_vertical(min_y, min_x, max_y, max_x)
        elif seg_height >= self.MAX and seg_width < self.MAX:
            self.split_on_horizontal(min_y, min_x, max_y, max_x)
        else:
            if random() < 0.5:
                self.split_on_horizontal(min_y, min_x, max_y, max_x)
            else:
                self.split_on_vertical(min_y, min_x, max_y, max_x)

    def split_on_horizontal(self, min_y, min_x, max_y, max_x):
        split = (min_y + max_y) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_y, min_x, split, max_x)
        self.random_split(split + 1, min_x, max_y, max_x)

    def split_on_vertical(self, min_y, min_x, max_y, max_x):
        split = (min_x + max_x) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_y, min_x, max_y, split)
        self.random_split(min_y, split + 1, max_y, max_x)

    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the
            # dungeon looks too uniform
            if random() > 0.80: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-100% of the
            # available section.
            room_width = round(randrange(50, 100) / 100 * section_width)
            room_height = round(randrange(50, 100) / 100 * section_height)

            # If the room doesn't occupy the entire section we are carving it from,
            # 'jiggle' it a bit in the square
            if section_height > room_height:
                room_start_y = leaf[0] + randrange(section_height - room_height)
            else:
                room_start_y = leaf[0]

            if section_width > room_width:
                room_start_x = leaf[1] + randrange(section_width - room_width)
            else:
                room_start_x = leaf[1]

            self.rooms.append(Room(room_start_x, room_start_y, room_height, room_width))
            for y in range(room_start_y, room_start_y + room_height):
                for x in range(room_start_x, room_start_x + room_width):
                    self.tiles[x, y] = TileSpace()

            try:
                for i in range(5):
                    x = randint(room_start_x+2, (room_start_x+room_width)-2)
                    y = randint(room_start_y+2, (room_start_y+room_height)-2)
                    self.tiles[x, y] = TileBillboardProp()
            except ValueError:
                pass

    def are_rooms_adjacent(self, room1, room2):
        adj_ys = []
        adj_xs = []
        for r in range(room1.y, room1.y + room1.h):
            if r >= room2.y and r < room2.y + room2.h:
                adj_ys.append(r)

        for c in range(room1.x, room1.x + room1.w):
            if c >= room2.x and c < room2.x + room2.w:
                adj_xs.append(c)

        return (adj_ys, adj_xs)

    def distance_between_rooms(self, room1, room2):
        centre1 = (room1.y + room1.h // 2, room1.x + room1.w // 2)
        centre2 = (room2.y + room2.h // 2, room2.x + room2.w // 2)

        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2)

    def carve_corridor_between_rooms(self, room1, room2):
        if room2[2] == 'ys':
            y = choice(room2[1])
            # Figure out which room is to the left of the other
            if room1.x + room1.w < room2[0].x:
                start_x = room1.x + room1.w
                end_x = room2[0].x
            else:
                start_x = room2[0].x + room2[0].w
                end_x = room1.x
            for x in range(start_x, end_x):
                self.tiles[x, y] = TileSpace()

            if end_x - start_x >= 4:
                self.tiles[start_x, y] = TileDoor()
                self.tiles[end_x - 1, y] = TileDoor()
            elif start_x == end_x - 1:
                self.tiles[start_x, y] = TileDoor()
        else:
            x = choice(room2[1])
            # Figure out which room is above the other
            if room1.y + room1.h < room2[0].y:
                start_y = room1.y + room1.h
                end_y = room2[0].y
            else:
                start_y = room2[0].y + room2[0].h
                end_y = room1.y

            for y in range(start_y, end_y):
                self.tiles[x, y] = TileSpace()

            if end_y - start_y >= 4:
                self.tiles[x, start_y] = TileDoor()
                self.tiles[x, end_y - 1] = TileDoor()
            elif start_y == end_y - 1:
                self.tiles[x, start_y] = TileDoor()

    # Find two nearby rooms that are in difference groups, draw
    # a corridor between them and merge the groups
    def find_closest_unconnect_groups(self, groups, room_dict):
        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.y, room.x)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group

        self.carve_corridor_between_rooms(start, nearest)

        # Merge the groups
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)

    def connect_rooms(self):
        # Build a dictionary containing an entry for each room. Each bucket will
        # hold a list of the adjacent rooms, weather they are adjacent along ys or
        # xumns and the distance between them.
        #
        # Also build the initial groups (which start of as a list of individual rooms)
        groups = []
        room_dict = {}
        for room in self.rooms:
            key = (room.y, room.x)
            room_dict[key] = []
            for other in self.rooms:
                other_key = (other.y, other.x)
                if key == other_key: continue
                adj = self.are_rooms_adjacent(room, other)
                if len(adj[0]) > 0:
                    room_dict[key].append((other, adj[0], 'ys', self.distance_between_rooms(room, other)))
                elif len(adj[1]) > 0:
                    room_dict[key].append((other, adj[1], 'xs', self.distance_between_rooms(room, other)))

            groups.append([room])

        while len(groups) > 1:
            self.find_closest_unconnect_groups(groups, room_dict)

    def generate_map(self):
        self.random_split(1, 1, self.h - 1, self.w - 1)
        self.carve_rooms()
        self.connect_rooms()

