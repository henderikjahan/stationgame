from game.stats.stats import CharacterStats
from game.map.walkers import CameraWalker
from game.moves import move_list as move


class Character:
    def __init__(self, name):
        self.name = name
        self.equipment = {}
        self.inventory = {}
        # TODO: Retrieve moves from equipment!
        self.moves = {"attack": move.BaseAttackAssault()}
        self.stats = CharacterStats(self)

    def battle_behavior(self, user, target):
        pass


class Enemy(Character):
    def __init__(self, name):
        Character.__init__(self, name)

    # TODO: is this Move logic?
    def battle_behaviour(self, user_battler, target_battler):
        stat = self.stats.current_stat
        while stat["AP_current"] >= 1:
            if stat["AP_current"] >= 1:
                self.moves["attack"].use(
                    user_battler = user_battler,
                    target_battler = target_battler
                )


class Player(Character):
    def __init__(self, map=None, camera=None):
        Character.__init__(self, "player")
        if camera and map:
            self.walker = CameraWalker(map.tilemap, camera)
            self.walker.root.reparent_to(render)
            self.walker.set_pos(*map.start)
            base.task_mgr.add(self.update)
        self.counter = 0

    def get_basic_attack(self):
        #TODO: retrieve from equipment
        return move.BaseAttackAssault()

    def update(self, task):
        self.walker.update()
        return task.cont

