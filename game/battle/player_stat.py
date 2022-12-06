from ..moves import move_list as move

# When changing the file location of this file, don't forget about the import:
# battle_gameplay.py
# battle_test.py
# *list updated in 27-10-2022


class PlayerStat:
    def __init__(self, playerstatdict = {}, player_equipment = {}, psi = {}, basic_attack = None):

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
        self.psi = {}
        self.equipment = {}


        # changes/add stats based on playerstatdict
        for entry in playerstatdict:
            self.stat[entry] = playerstatdict[entry]
        
        # changes/add equipment based on player_equipment
        for entry in player_equipment:
            self.equipment[entry] = player_equipment[entry]

        #changes/add psi moves based on psi
        for entry in psi:
            self.psi[entry] = psi[entry]
        
        # basic attack, expects a move class object
        if basic_attack == None:
            self.basic_attack = move.Attack()
    

