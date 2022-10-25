
# When changing the file location of this file, don't forget about the import:
# battle_v02    
# *list updated in 12-9-2022

class Item:
    def __init__(self):
        pass
        
class Equipment:
    def __init__(self):
        self.stats = {
            "Physical Defense": 10,
        }

class PlayerStat:
    def __init__(self, playerstatdict = {}, player_equipment = {}, psi = {}):

        # !When having thoughts about certain stats, please share!
        # base stats
        self.stat = {
            "Current HP": 50,   # Current HP
            "Max HP": 50,	# Maximum Hit points
            "HP Regen": 0,
            
            "Assault": 5,	# Base attack stat
            "Tactics": 10,	# Damage reduction of receiving Physical attacks: damageReceived = 100/(100+defense)
            "Psi": 10,

            "Assault Defence": 5, # Base attack stat
            "Tactical Defense": 10,	# Damage reduction of receiving Physical attacks: damageReceived = 100/(100+defense)
            "Psi Defense": 10,	# Damage reduction of receiving Psi attacks: damageReceived = 100/(100+defense)

            "Dodge": 10, # Avoid rage and tactical, but not psi.
         
            # Elemental types - affinity is resistance and a bonus to damage 
            "Heat Affinity": 10,
            "Elec Affinity": 10,
            "Data Affinity": 10,
            
            "Turn AP": 3,	# Turn Action points, determines the amount of AP the battlers can gain per turn at start
            "Max AP": 5,    # Maximum Action points, which can be banked
            
            # Out of combat stats:
            "Hacking": 10, # Basically lockpicking
            "Tinkering": 10, # Making / crafting stuff
            "Light radius": 10, # For discovering mini map

            "Charisma": 1, # in case we have stores, make items cheaper to buy "bartering"
            "Stealth": 1, # reduced battle chance, when sneaking. Can increase run chance. Base run chance scaled by enemy hp.
            "Robotica": 1 # handle droid companions (maybe scale damage or allow new pets to be used)

            "Stability": 10, # Innate stability scaling - so that items can increase or decrease stability
            
        }
        self.equipment = {}

        # changes/add stats based on playerstatdict
        for entry in playerstatdict:
            self.stat[entry] = playerstatdict[entry]
        
        # changes/add equipment based on player_equipment
        for entry in player_equipment:
            self.equipment[entry] = player_equipment[entry]
        
        #changes/add psi commands based on psi
        for entry in psi:
            self.psi[entry] = psi["entry"]
    

