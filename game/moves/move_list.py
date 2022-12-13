from setuptools import Command
from game.tools import print

# -- classes --

class MoveBase:
    def __init__(self):

        self.name = "MoveBase"
        self.ap_cost = 0
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
        if not check_legality_target(target_battler= target_battler):
            return False

        continue_move = user_battler.reduce_self_ap(self.ap_cost)
        # continue move is True or False, depending whether the cost can be paid

        if continue_move:
            move_power = self.move_power
            
            raw_damage = user_battler.deal_damage_Base(
                attack_type= self.attack_type,
                move_power= move_power
                )
            
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} attacked {str_targetbattler}!")

            target_battler.take_damage(
                raw_damage= raw_damage,
                attack_type= self.attack_type
                )


        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")

    def damage_single_target(self, user_battler, target_battler, move_power, attack_type= "Placeholder"):

        raw_damage = user_battler.deal_damage_Base(
            move_power= move_power
            )

        target_battler.take_damage(
            raw_damage= raw_damage
            )


class BaseAttackAssault(MoveBase):
    def __init__(self):

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "Assault"
        self.affinity = None

class FireBall(MoveBase):
    def __init__(self):

        self.name = "Fire"
        self.ap_cost = 2
        self.move_power = 2.0
        self.attack_type = "Psi"
        self.affinity = "Heat"

    def use(self, user_battler, target_battler):
        if not check_legality_target(target_battler= target_battler):
            return False

        continue_move = user_battler.reduce_self_ap(self.ap_cost)
        # continue move is True or False, depending whether the cost can be paid

        if continue_move:
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} used Fire on {str_targetbattler}!")

            # target_battler takes damage
            self.damage_single_target(
                user_battler= user_battler,
                target_battler= target_battler,
                move_power= self.move_power,
                attack_type= self.attack_type
            )

        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")



# -- normal functions --
# !is unused

def check_legality_target(target_battler, status_list = ["Felled"], check_for_illegality = True):
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


def attack(user_battler, target_battler = None):

    if not check_legality_target(target_battler= target_battler):
        return False

    ap_cost = 1
    continue_move = user_battler.reduce_self_ap(ap_cost)
    # continue move is True or False, depending whether the cost can be paid

    if continue_move:

        move_power = 1.0
        
        raw_damage = user_battler.deal_damage_Base(move_power= move_power)
        
        # message
        str_userbattler = str(user_battler.name)
        str_targetbattler = str(target_battler.name)
        print( f"{str_userbattler} attacked {str_targetbattler}!")

        target_battler.take_damage(raw_damage= raw_damage)


    else:
        # ap cost too low
        str_userbattler = str(user_battler.name)
        print( f"{str_userbattler}'s AP is too low!")


def fire(stat):
    # for testing weakness stuff
    if "Base Attack" in stat:
        return stat["Base Attack"] * 1.8
    else:
        print("Move Fire cannot find Base Attack")
        return 0.0


def armorbash(stat):
    # for testing using alternative stats
    if "Physical Defense" in stat:
        return stat["Physical Defense"]
    else:
        print("Move Armorbash cannot find Physical Defense")
        return 0.0

