from setuptools import Command
from game.tools import print


# <--- Base Class --->
class MoveBase:
    def __init__(self):

        self.name = "MoveBase"
        self.ap_cost = 1
        self.move_power = 1
        self.attack_type = "Assault"
        self.affinity = None

    def return_name(self):
        return self.name

    def check_legality_target(self, target_battler, status_list = ["Felled"], check_for_illegality = True):
        # checks whether the target is legal based on status
        # checks for Felled on default
        # returns True if the target is legal, False when the the target is illegal
        if check_for_illegality == True and status_list != None:
            # Returns True when the target DOES NOT HAVE the status in status_list
            for status in status_list:
                if status in target_battler.status:
                    str_targetbattler = str(target_battler.name)
                    str_status = str(status)
                    print( f"{str_targetbattler} already has been {str_status}")
                    return False

            return True

        elif check_for_illegality == False and status_list != None:
            # For checking when the target HAVES the status in status_list
            for status in status_list:
                if status in target_battler.status:
                    return True
            
            str_targetbattler = str(target_battler)
            print( f"{str_targetbattler} is not afflicted with anything!")
            return False

        print("!check_legality_target from move_list cannot find")
        return False

    def use(self, user_battler, target_battler):
        # basic attack function, can be used as a generic single attack
        # do be wary of the prints when inheriting
        if not self.check_legality_target(target_battler= target_battler):
            return False

        continue_move = user_battler.reduce_self_ap(self.ap_cost)
        # continue move is True or False, depending whether the cost can be paid

        if continue_move:
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} attacked {str_targetbattler}!")
            
            # damage
            raw_damage = user_battler.deal_damage_Base(
                attack_type= self.attack_type,
                move_power= self.move_power
                )
            
            target_battler.take_damage(
                raw_damage= raw_damage,
                attack_type= self.attack_type
                )


        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")

    def calc_affinity(self, user_battler= None, target_battler= None):
        # returns a multiplier for related affinity
        
        # when affinity is not defined in the move
        if self.affinity == None:
            print(f"{self.name}.apply_affinity used with None affinity")
            return 1
        else:
            affinity = self.affinity

        if user_battler == None or affinity not in user_battler.stat:
            user_var = 1
        else:
            user_var = user_battler.stat[affinity]
        
        if target_battler == None or affinity not in target_battler.stat:
            target_var = 1
        else:
            target_var = target_battler.stat[affinity]
        

        multiplier = user_var / target_var
        return multiplier
        

    def damage_single_target(self, user_battler, target_battler, move_power, attack_type= "Placeholder"):
        # old
        raw_damage = user_battler.deal_damage_Base(
            move_power= move_power
            )

        target_battler.take_damage(
            raw_damage= raw_damage
            )


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
            print( f"{str_userbattler} used Fire on {str_targetbattler}!")

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

