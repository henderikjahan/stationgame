
# When changing the file location of this file, don't forget about the import:
# battle_v02    
# *list updated in 12-9-2022


class playerstat:
    def __init__(self, playerstatdict = {}, player_equipment = {}, psi = {}):

        # !When having thoughts about certain stats, please share!
        # base stats
        self.stat = {
            "Current HP": 50,   # Current HP
            "Max HP": 50,	# Maximum Hit points
            "Base Attack": 5,	# Base attack stat
            "Physical Defense": 10,	# Damage reduction of receiving Physical attacks: damageReceived = 100/(100+defense)
            "Psi Defense": 10,	# Damage reduction of receiving Psi attacks: damageReceived = 100/(100+defense)
            "Turn AP": 3,	# Turn Action points, determines the amount of AP the battlers can gain per turn at start
            "Max AP": 5,    # Maximum Action points, which can be banked
        }
        self.equipment = {}
        self.psi = {
            "Fire": {
                "Skill Name": "Fire",
                "AP Cost": 2,
                "Type": "psi",
                "Attribute": "Fire",
                "Power": command_fire
            },
            "ArmorBash": {
                "Skill Name": "ArmorBash",
                "AP Cost": 1,
                "Type": "psi",
                "Attribute": "None",
                "Power": command_armorbash
            }
        }

        # changes/add stats based on playerstatdict
        for entry in playerstatdict:
            self.stat[entry] = playerstatdict[entry]
        
        # changes/add equipment based on player_equipment
        for entry in player_equipment:
            self.equipment[entry] = player_equipment[entry]
        
        #changes/add psi commands based on psi
        for entry in psi:
            self.psi[entry] = psi["entry"]
    



def command_fire(stat):
    # for testing weakness stuff
    if "Base Attack" in stat:
        return stat["Base Attack"] * 1.8
    else:
        print("Command Fire cannot find Base Attack")
        return 0.0

def command_armorbash(stat):
    # for testing using alternative stats
    if "Physical Defense" in stat:
        return stat["Physical Defense"]
    else:
        print("Command Armorbash cannot find Physical Defense")
        return 0.0