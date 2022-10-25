from setuptools import Command
from game.tools import print

# -- classes --

class CommandBase:
    def __init__(self):

        self.ap_cost = 0
        self.command_power = 1
        self.attack_type = "Placeholder"

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

        print("!check_legality_target from command_list cannot find")
        return False

    def use(self, user_battler, target_battler):
        pass

    def damage_single_target(self, user_battler, target_battler, command_power, attack_type= "Placeholder"):

        raw_damage = user_battler.deal_damage_Base(
            command_power= command_power
            )

        target_battler.take_damage(
            raw_damage= raw_damage
            )

    def _old_weakness_check(self, target_battler, attack_type= "Placeholder"):
        # !deprecated element
        # applies break on target etc.
        weakness_hit = False
        if attack_type in target_battler.weakness:
            weakness_hit = True

        return weakness_hit

    def _old_damage_single_target(self, user_battler, target_battler, command_power, attack_type= "Placeholder"):
        # !depecrated element
        weakness_hit = self.weakness_check(
            target_battler= target_battler, 
            attack_type= attack_type
            )

        raw_damage = user_battler.deal_damage_Base(
            command_power= command_power,
            weakness_hit= weakness_hit
            )

        target_battler.take_damage(
            raw_damage= raw_damage
            )
        
        if weakness_hit == True:
            target_battler.apply_break_status()


class Attack(CommandBase):
    def __init__(self):
        self.ap_cost = 1
        self.command_power = 1.0
        self.attack_type = "Something"


class Fire(CommandBase):
    def __init__(self):
        
        self.ap_cost = 2
        self.command_power = 2.0
        self.attack_type = "Heat"

    def use(self, user_battler, target_battler):
        if not check_legality_target(target_battler= target_battler):
            return False

        continue_command = user_battler.reduce_self_ap(self.ap_cost)
        # continue command is True or False, depending whether the cost can be paid

        if continue_command:
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} used Fire on {str_targetbattler}!")

            # target_battler takes damage
            self.damage_single_target(
                user_battler= user_battler,
                target_battler= target_battler,
                command_power= self.command_power,
                attack_type= self.attack_type
            )

        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")



# -- normal functions --

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

    print("!check_legality_target from command_list cannot find")
    return False


def attack(user_battler, target_battler = None):

    if not check_legality_target(target_battler= target_battler):
        return False

    ap_cost = 1
    continue_command = user_battler.reduce_self_ap(ap_cost)
    # continue command is True or False, depending whether the cost can be paid

    if continue_command:

        command_power = 1.0
        
        raw_damage = user_battler.deal_damage_Base(command_power= command_power)
        
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
        print("Command Fire cannot find Base Attack")
        return 0.0


def armorbash(stat):
    # for testing using alternative stats
    if "Physical Defense" in stat:
        return stat["Physical Defense"]
    else:
        print("Command Armorbash cannot find Physical Defense")
        return 0.0

