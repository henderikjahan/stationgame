from game.character.character import Enemy
from game.moves import move_list as move


class BorgerBurger(Enemy):
    def __init__(self):
        Enemy.__init__(self, name="Borger Burger")
        self.stats.basic_stats |= {
            # HP
            "HP_current": 10,
            "HP_max": 10,
            # Attack stats
            "assault": 10,
            "tactics": 10,
            "psi": 10,
            # Defense stats, damageReceived = 100/(100+defense)
            #"Assault Defense": 10,
            #"Tactical Defense": 10,
            #"Psi Defense": 10,
            "AP_regen": 1,
            "AP_max": 1,
        }


class MagicalMayonaise(Enemy):
    def __init__(self):
        Enemy.__init__(self, "Magical Mayonaise")
        self.stats.basic_stats |= {
            # HP
            "HP_current": 10,
            "HP_max": 10,
            # Attack stats
            "assault": 10,
            "tactics": 10,
            "psi": 10,
            # Defense stats, damageReceived = 100/(100+defense)
            #"Assault Defense": 10,
            #"Tactical Defense": 10,
            #"Psi Defense": 10,
            # AP
            "AP_regen": 1,
            "AP_max": 5,
        }


class SpoiledEggBoy(Enemy):
    def __init__(self):
        Enemy.__init__(self, "Spoiled Egg Boy")
        self.stats.basic_stats |= {
            # HP
            "HP_current": 20,
            "HP_max": 20,

            # Attack stats
            "assault": 10,
            "tactics": 10,
            "psi": 10,

            # Defense stats, damageReceived = 100/(100+defense)
            #"Assault Defense": 10,
            #"Tactical Defense": 10,
            #"Psi Defense": 10,

            # AP
            "AP_current": 3,
            "AP_turn": 2,
            "AP_max": 5,
        }
        self.moves |= {"rotten egg" : move.RottenEgg()}


    def battle_behaviour(self, user_battler, target_battler):
        stats = self.stats.current_stat
        str_ap = str(stats["AP_current"])
        print(
            f"{self.name} AP: {str_ap}"
        )
        moves = self.moves
        if stats["AP_current"] >= 1:
            if stats["AP_current"] >= 3 and "rotten egg" in moves:
                moves["rotten egg"].use(
                    user_battler= user_battler,
                    target_battler= target_battler
                )
            else:
                moves["attack"].use(
                    user_battler= user_battler,
                    target_battler= target_battler
                )




# <-----> HISTORICAL BATTLER CLASS
'''
class Placeholder(EnemyBattler):
    def __init__(self, battle_ref):

        statsdict = {
            # HP
            "Current HP": 10,
            "Max HP": 10,

            # Attack stats
            "Assault": 10,
            "Tactics": 10,
            "Psi": 10,

            # Defense stats, damageReceived = 100/(100+defense)
            "Assault Defense": 10,
            "Tactical Defense": 10,
            "Psi Defense": 10,

            "Heat Affinity": 1.0,
            "Elec Affinity": 1.0,
            "Data Affinity": 1.0,

            # AP
            "Current AP": 0,
            "Temporary AP": 0,
            "Turn AP": 1,
            "Max AP": 5,
        }
        weakness = []
        status = None
        name = "Placeholder"

        move_dict = {
            "Attack": move.BaseAttackAssault()
        }

        EnemyBattler.__init__(
            self,
            statsdict = statsdict,
            weakness = weakness,
            status = status,
            name = name,
            battle_ref = battle_ref,
            move_dict= move_dict
        )


    def self_behaviour(self):
        while self.stat["Current AP"] >= 1:
            if self.stat["Current AP"] >= 1:
                self.move_dict["Attack"].use(
                    user_battler= self,
                    target_battler= self.player()
                )
'''
