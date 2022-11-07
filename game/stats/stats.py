
class Stats:
    def __init__(self, statdict = {}, equipment = {}, psi = {}):

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
         
            "Heat Affinity": 10,
            "Elec Affinity": 10,
            "Data Affinity": 10,
            
            "Hacking": 10,
            "Tinkering": 10,
            "Light radius": 10,

            "Charisma": 1, # in case we have stores, make items cheaper to buy "bartering"
            "Stealth": 1, # reduced battle chance, when sneaking
            "Robotica": 1, # handle droid companions

            "Stability": 10,
            
            "Turn AP": 3,	# Turn Action points, determines the amount of AP the battlers can gain per turn at start
            "Max AP": 5,    # Maximum Action points, which can be banked
        }
        self.equipment = {}

        # changes/add stats based on playerstatdict
        for entry in statdict:
            self.stat[entry] = statdict[entry]
        
        # changes/add equipment based on player_equipment
        for entry in equipment:
            self.equipment[entry] = equipment[entry]
        
        #changes/add psi commands based on psi
        for entry in psi:
            self.psi[entry] = psi["entry"]
    