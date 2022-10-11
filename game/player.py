#ATM basically connect all player gameplay parts into one class (battle, exploration, inventory)

from game.map.walkers import CameraWalker
from game.battle import PlayerStat
from game.battle import enemy
from game.battle import BattleGameplay


class Player:
    def __init__(self, map, camera):
        self.inventory = {}
    
        self.walker = CameraWalker(map.tilemap, camera)
        self.walker.root.reparent_to(render)
        self.walker.set_pos(*map.start)
        self.stat = PlayerStat()

        self.battle = None
        self.counter = 0
        base.task_mgr.add(self.update)

    def update(self, task):
        if base.sequencer.running:
            return task.cont

        if self.battle:
            self.battle.player_turn("attack")
            self.battle =  None
        else:
            if self.counter > 10:
                self.battle = BattleGameplay(
                    player_gl = self.stat,
                    enemies_data = [
                        enemy.BorgerBurger,
                        enemy.MagicalMayonaise
                    ]
                )
                self.counter = 0
            if self.walker.movement():
                self.counter += 1
        return task.cont