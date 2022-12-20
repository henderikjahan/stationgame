from setuptools import Command
from game.tools import print
from .movebase import MoveBase


# <--- Moves --->

# -- Basic attacks --
class BaseAttackAssault(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "Assault"
        self.affinity = None


class BaseAttackTactics(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "Assault"
        self.affinity = None

        self.standard_attribute()
        
class BaseAttackTactics(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "Assault"
        self.affinity = None

# -- Attack Moves --
class FireBall(MoveBase):
    def __init__(self):
        super().__init__()
        self.name = "Fire"
        self.ap_cost = 2
        self.move_power = 2.0
        self.attack_type = "Psi"
        self.affinity = "Heat Affinity"


    def use(self, user_battler, target_battler):
        if not self.check_legality_target(target_battler= target_battler):
            return False

        continue_move = user_battler.reduce_self_ap(self.ap_cost)
        # continue move is True or False, depending whether the cost can be paid

        if continue_move:
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} used {self.name} on {str_targetbattler}!")

            # damage
            raw_damage = user_battler.deal_damage_Base(
                attack_type= self.attack_type,
                move_power= self.move_power
                )
            affinity = self.calc_affinity(
                user_battler= user_battler,
                target_battler= target_battler
                )

            raw_damage = raw_damage * affinity

            target_battler.take_damage(
                raw_damage= raw_damage,
                attack_type= self.attack_type
            )

        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")


class CatchMe(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "CatchMe"
        self.ap_cost = 2
        self.move_power = 1
        self.attack_type = "Current HP"

class CatchMe2(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "CatchMe"
        self.ap_cost = 2
        self.move_power = 1
        self.attack_type = "Assault"
    
    def use(self, user_battler, target_battler):
        return super().use(user_battler, target_battler)