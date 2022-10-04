import math
import command_list as command
import status_list as status

# <-- general battler class -->
# For editing stats and mechanics which affects all battlers
class Battler:
    def __init__(self, statsdict = None, weakness = None, status = None, name = None, battle_ref = None):
        
        if name == None:
            name = "Unnamed"
        if statsdict == None:
            statsdict = {}
        if weakness == None:
            weakness = []
        if status == None:
            status = {}

        self.battle_ref = battle_ref
        self.name = name
        self.set_true_stat(statsdict)
        self.weakness = weakness
        self.status = status
        
    def set_true_stat(self, statsdict):
        # set stats to the inputed statsdict
        # here under are the base stats
        self.stat = {
            "Current HP": 10,
            "Max HP": 10,

            "Base Attack": 5,
            "Physical Defense": 0,
            "Psi Defense": 0,

            "Current AP": 0,
            "Turn AP": 1,
            "Max AP": 5
            }

        for entry in statsdict:
            self.stat[entry] = statsdict[entry]

    def start_of_battle(self):
        # set AP
        self.stat["Current AP"] = self.stat["Turn AP"]
        if self.stat["Current AP"] > self.stat["Max AP"]:
            self.stat["Current AP"] = self.stat["Max AP"]

        # at start of battle passives

        pass

    def gain_turn_AP(self):
        # checks whether the character is felled
        if "Felled" in self.status:
            return  # return ends the function prematurely, before the turn AP gain

        # AP
        self.stat["Current AP"] += self.stat["Turn AP"]
        if self.stat["Current AP"] > self.stat["Max AP"]:
            self.stat["Current AP"] = self.stat["Max AP"]

    def start_of_turn(self):
        # at start of turn passives/statuses
        
        pass

    def end_of_turn(self):
        # AP
        self.gain_turn_AP()

        # at end of turn passives


    def deal_damage_Base(self, command_power):
        # deal damage with base attack in mind
        raw_damage = self.stat["Base Attack"] * command_power

        return raw_damage
    
    def take_damage(self, raw_damage):
        # Take damage based on physical defense
        end_damagepre = raw_damage * 100 / (100 + self.stat["Physical Defense"])
        end_damage = math.ceil(end_damagepre)

        self.stat["Current HP"] -= end_damage
        if self.stat["Current HP"] < 0:
            self.stat["Current HP"] = 0

        # message about taking damage
        str_selfname = str(self.name)
        str_enddamage = str(end_damage)
        print(f"{str_selfname} has taken {str_enddamage} damage!")

        # checks whether it's felled
        if self.stat["Current HP"] <= 0.0:
            self.apply_felled_status()

        return end_damage   # Returns resulting damage

    def apply_felled_status(self):
        str_selfname = str(self.name)
        print(f"{str_selfname} has been felled!")

        self.status["Felled"] = status.felled(
            name= "Felled",
            turn= None,
            strength= 1,
            afflicted_object= self
        )

        if self.battle_ref != None:
            self.battle_ref.check_victory()


    def check_ap_cost(self, cost = 1):
        # mainly usefull for enemies for checking what's the best option
        # returns True and False depending on the cost versus current AP
        if self.stat["Current AP"] < cost:
            return False
        else:
            return True

    def reduce_self_ap(self, cost = 1):
        # checks and reduce the current ap of 'self'
        # returns True and False depending on the cost versus current AP
        
        if self.stat["Current AP"] < cost:
            return False
        else:
            self.stat["Current AP"] -= cost
            return True

    def self_behaviour(self):
        pass

    # to-do in battler:
    #   status handling
    #   passive handling
    #   

# <-- Enemy Battler class -->
class Enemy_Battler(Battler):
    def __init__(self, statsdict=None, weakness=None, status=None, name=None, battle_ref=None):
        super().__init__(statsdict, weakness, status, name, battle_ref)

    def player(self):
        return self.battle_ref.player_battler

# <-- Player battler class -->
class Player_Battler(Battler):
    def __init__(self, statsdict = None, weakness = None, status = None, equipment = None, psi = None, battle_ref = None):

        Battler.__init__(
            self, 
            statsdict = statsdict, 
            weakness = weakness, 
            status = status,
            name = "Player",
            battle_ref= battle_ref
        )

        if equipment == None:
            equipment = {}
        if psi == None:
            psi = {}
        
        self.equipment = equipment
        self.psi = psi

    def low_ap_message(self):
        str_selfname = str(self.name)
        print(
            f"{str_selfname} is too low!"
        )



# <-- battle class -->
class Battle_Gameplay:
    def __init__(self, player_gl, enemies_data):
    
        # --Variable Setup--
        self.player_battler = Player_Battler(
            statsdict = player_gl.stat,
            equipment = player_gl.equipment,
            battle_ref = self
            #,psi = player_gl.psi
        )

        self.enemies_list = []
        for enemy_data in enemies_data:
            item = enemy_data(
                battle_ref= self
            )
            self.enemies_list.append(item)
        
        self.turn = 1
        self.exit_battle = False
        self.results = "undetermined"

        # Starts battle
        self.battle_loop()

    def battle_loop(self):

        self.start_of_battle()
        
        while True:

            self.battle_turn()

            if self.exit_battle == True:
                print("battle exited")
                break
        
        print("end of battle")


    def check_victory(self):
        # checks whether the battle can be ended when either party is fully felled
        player = self.player_battler
        enemies = self.enemies_list

        # checks player for felled status
        if "Felled" in player.status:
            self.exit_battle = True
            self.results = "lose"
            print("\nThe Player's been felled!")
            return

        # checks all enemies for felled status
        felled_count = 0
        for enemy in enemies:
            if "Felled" in enemy.status:
                felled_count += 1

        if felled_count == len(enemies):
            self.exit_battle = True
            self.results = "win"
            print("\nAll enemies has been felled!")
            return


    def start_of_battle(self):
        print("\nStart Battle\n")
        # Start of battle handling per battler
        self.player_battler.start_of_battle()
        for enemy_battler in self.enemies_list:
            enemy_battler.start_of_battle()

    def battle_turn(self):
        # --Start of Turn--
        str_turn = str(self.turn)
        print(f"\n\n<--Turn {str_turn} -->")

        # --Player Turn--
        print("--Player's Turn--")
        self.player_battler.start_of_turn()
        pturn_active = True
        while pturn_active:
            pturn_active = self.player_turn()

            if self.exit_battle == True:
                # escape from battle
                return  # return is used, so that enemy doesn't get a turn
        self.player_battler.end_of_turn()


        # --Enemy Turn--
        print("\n--Enemy's Turn--")
        for enemy_battler in self.enemies_list:
            enemy_battler.start_of_turn()
        for enemy_battler in self.enemies_list:
            self.enemy_turn(enemy_battler= enemy_battler)
        for enemy_battler in self.enemies_list:
            enemy_battler.end_of_turn()

        # --End of turn--
        self.turn += 1


    def player_turn(self):

        # <Status Check>
        print("")
        print_output = ""
        for enemy_battler in self.enemies_list:
            # ! change this into f string
            str_enemy = str(enemy_battler.name)
            str_eHP = str(enemy_battler.stat["Current HP"])
            print_output += f"{str_enemy} HP: {str_eHP}   "
        print(print_output)

        str_plCHP = str(self.player_battler.stat["Current HP"])
        str_plMHP = str(self.player_battler.stat["Max HP"])
        str_plAP = str(self.player_battler.stat["Current AP"])
        print(f"\nPlayer HP: {str_plCHP}/{str_plMHP}")
        print(f"Player AP: {str_plAP}")

        print("\n--Choose command--")
        print("Attack (1*)| Psi | TurnPass | Exit")

        # creating a reference for the enemies
        short_name_list = []
        for enemy in self.enemies_list:
            short_name_list.append(''.join(letter for letter in enemy.name if letter.isupper()))

        takeninput = input(">Input: ").lower()
        
        match takeninput.split(sep= ' ', maxsplit= 1):
            
            case ["exit" | "e"]:
                self.exit_battle = True
                return False

            case ["attack" | "a", *target]: 
                #target is a single string in a list
                # note to self, please make this more neat
                command.targeting_tool(
                    user_battler= self.player_battler,
                    enemies_list= self.enemies_list,
                    command_function= command.attack,
                    target_input= target
                )

            case ["psi" | "p"]:
                print("choose psi")
                # Doesn't work at the moment
                while False:
                    takeninput = input("Input: ")
            
            case ["turnpass" | "t" | "tp"]:
                print("turn passed")
                return False

            case _:
                print("Input not recognized")
        
        return True


    def enemy_turn(self, enemy_battler):
        # --Enemy Turn--
        enemy_battler.self_behaviour()
        



