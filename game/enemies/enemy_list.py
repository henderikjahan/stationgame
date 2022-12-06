from ..battle.battle_gameplay import EnemyBattler
from ..moves import move_list as move


class BorgerBurger(EnemyBattler):
    def __init__(self, battle_ref):

        statsdict = {
            "Current HP": 15,
            "Max HP": 15,

            "Base Attack": 5,
            "Physical Defense": 0,
            "Psi Defense": 0,

            "Current AP": 0,
            "Turn AP": 1,
            "Max AP": 5
        }
        weakness = []
        status = None
        name = "Borger Burger"

        EnemyBattler.__init__(
            self,
            statsdict = statsdict,
            weakness = weakness,
            status = status,
            name = name,
            battle_ref = battle_ref
        )


    def self_behaviour(self):
        while self.stat["Current AP"] >= 1:
            if self.stat["Current AP"] >= 1:
                move.attack(
                    user_battler= self,
                    target_battler= self.player()
                )



class MagicalMayonaise(EnemyBattler):
    def __init__(self, battle_ref):

        statsdict = {
            "Current HP": 8,
            "Max HP": 8,

            "Base Attack": 8,
            "Physical Defense": 0,
            "Psi Defense": 0,

            "Current AP": 0,
            "Turn AP": 1,
            "Max AP": 5
        }
        weakness = []
        status = None
        name = "Magical Mayonaise"

        EnemyBattler.__init__(
            self,
            statsdict = statsdict,
            weakness = weakness,
            status = status,
            name = name,
            battle_ref = battle_ref
        )


    def self_behaviour(self):
        while self.stat["Current AP"] >= 1:
            if self.stat["Current AP"] >= 1:
                move.attack(
                    user_battler= self,
                    target_battler= self.player()
                )





# <----->
class Placeholder(EnemyBattler):
    def __init__(self, battle_ref):

        statsdict = {
            "Current HP": 11,
            "Max HP": 11,

            "Base Attack": 11,
            "Physical Defense": 11,
            "Psi Defense": 11,

            "Current AP": 0,
            "Turn AP": 0,
            "Max AP": 5
        }
        weakness = []
        status = None
        name = "Placeholder"

        EnemyBattler.__init__(
            self,
            statsdict = statsdict,
            weakness = weakness,
            status = status,
            name = name,
            battle_ref = battle_ref
        )


    def self_behaviour(self):
        while self.stat["Current AP"] >= 1:
            if self.stat["Current AP"] >= 1:
                move.attack(
                    user_battler= self,
                    target_battler= self.player()
                )