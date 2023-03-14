from copy import deepcopy
from math import inf
import nestedtext

from game.map.construct import MeshMap
from game.map.walkers import AutoWalker, CameraWalker
from game.tools import load_as_dict, render_to_texture


def parse(filename):
    def recurse(data):
        for d in data:
            if type(data[d]) == dict:
                recurse(data[d])
            else:
                try:
                    if "." in data[d]:
                       data[d] = float(data[d])
                    else:
                       data[d] = int(data[d])
                except (TypeError, ValueError):
                    if data[d] == "inf":
                        data[d] = inf
                    else:
                        data[d] = str(data[d])
    data = nestedtext.load(filename)
    recurse(data)
    return data


class Enemy:
    def __init__(self, name, data, x, y):
        self.name = name
        self.data = data
        self.stats = data["Stats"]
        self.moves = data["Moves"]
        self.image = loader.load_texture("assets/image/enemies/data/enemies/"+data["Image"]+".png")
        self.walker = CameraWalker(tilemap.tilemap, camera)


class Player:
    def __init__(self, stats, tilemap, camera):
        self.equipment = {}
        self.inventory = []
        self.walker = CameraWalker(tilemap.tilemap, camera)
        self.walker.root.reparent_to(render)
        self.walker.set_pos(*tilemap.start)
        base.task_mgr.add(self.walker.update)


class Level:
    def __init__(self, data=None): # supply data later
        self.data = data
        self.mesh_map = MeshMap(load_as_dict("assets/bam/tiles.bam"))
        self.mesh_map.root.reparent_to(render)
        data_mgr.build_player(self.mesh_map, camera=render_to_texture(render))


class DataMgr:
    def __init__(self):
        self.built = []
        self.battle_data = parse("assets/data/battle.nt")

    def build_level(self, name):
        result = Level()
        self.built.append(result)
        return result

    def build_player(self, tilemap, camera):
        result = Player(deepcopy(self.battle_data["Stats"]), tilemap, camera)
        self.built.append(result)
        return result

    def build_enemy(self, name, x, y):
        enemy_data = deepcopy(self.battle_data["Enemies"][name])
        for stat in self.battle_data["Stats"]:
            if not stat in enemy_data["Stats"]:
                enemy_data["Stats"][stat] = self.battle_data["Stats"][stat]
        result = Enemy(name, data)
        self.built.append(result)
        return result
