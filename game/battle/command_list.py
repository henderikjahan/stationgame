


def attack(user_battler, target_battler):
    
    ap_cost = 1
    continue_command = user_battler.reduce_self_ap(ap_cost)
    # continue command is True or False, depending whether the cost can be paid

    if continue_command:

        command_power = 1.0
        
        raw_damage = user_battler.deal_damage_Base(command_power= command_power)
        
        # message
        print(str(user_battler.name) + " attacked " + str(target_battler.name) + "!")

        target_battler.take_damage(raw_damage= raw_damage)


    else:
        # ap cost too low
        print(str(user_battler.name) + "'s AP is too low!")


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


psi = {
            "Fire": {
                "Skill Name": "Fire",
                "AP Cost": 2,
                "Type": "psi",
                "Attribute": "Fire",
                "Power": fire
            },
            "ArmorBash": {
                "Skill Name": "ArmorBash",
                "AP Cost": 1,
                "Type": "psi",
                "Attribute": "None",
                "Power": armorbash
            }
        }