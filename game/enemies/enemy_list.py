from ..battle.battle_gameplay import EnemyBattler
from ..moves import move_list as move

# inherited from enemybattler class

class BorgerBurger(EnemyBattler):
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
            "Max AP": 1,
        }
        weakness = []   #unused
        status = None
        name = "Borger Burger"

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



class MagicalMayonaise(EnemyBattler):
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
        name = "Magical Mayonaise"

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





# <----->
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