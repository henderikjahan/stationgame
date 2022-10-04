from battle_gameplay import Enemy_Battler
import command_list as command


class Borger_Burger(Enemy_Battler):
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

        Enemy_Battler.__init__(
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
                command.attack(
                    user_battler= self,
                    target_battler= self.player()
                )



class Magical_Mayonaise(Enemy_Battler):
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

        Enemy_Battler.__init__(
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
                command.attack(
                    user_battler= self,
                    target_battler= self.player()
                )





# <----->
class Placeholder(Enemy_Battler):
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

        Enemy_Battler.__init__(
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
                command.attack(
                    user_battler= self,
                    target_battler= self.player()
                )