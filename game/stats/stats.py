
from ..moves import move_list as move

class Stats:
    def __init__(self, statdict = {}, equipment = {}, psi = {}, basic_attack = None):

        # !When having thoughts about certain stats, please share!
        # base stats
        self.stat = {
            "Current HP": 50,   # Current HP
            "Max HP": 50,	# Maximum Hit points
            "HP Regen": 0,
            
            # Attack stats
            "Assault": 10,
            "Tactics": 10,
            "Psi": 10,

            # Defense stats, damageReceived = 100/(100+defense)
            "Assault Defense": 10,
            "Tactical Defense": 10,
            "Psi Defense": 10,

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

        # changes/add stats based on statdict
        for entry in statdict:
            self.stat[entry] = statdict[entry]
        
        # changes/add equipment based on given equipment
        self.equipment = {}
        for entry in equipment:
            self.equipment[entry] = equipment[entry]
        
        #changes/add moves based on given moves
        self.psi = {}
        for entry in psi:
            self.psi[entry] = psi[entry]
        
        # basic attack, expects a move class object
        if basic_attack == None:
            self.basic_attack = move.Attack()
    