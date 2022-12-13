import math
import random
from game.moves import move_list as move
from game.battle import status_list as status
from game.tools import print


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
        
        # !temp stats, minmax are integers
        self.weapon_attack_min = 1
        self.weapon_attack_max = 2

    def set_true_stat(self, statsdict):
        # set stats to the inputed statsdict
        # here under are the base stats
        self.stat = {
            # HP
            "Current HP": 10,
            "Max HP": 10,

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

            # AP
            "Current AP": 0,
            "Temporary AP": 0,
            "Turn AP": 1,
            "Max AP": 5,

            # old stats
            "Base Attack": 5,
            "Physical Defense": 0
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

    def gain_temporary_AP(self, AP= 1):
        mst = self.stat
        if AP < (mst["Max AP"] - mst["Current AP"]):
            AP = (mst["Max AP"] - mst["Current AP"])

        self.stat["Temporary AP"] += AP

    def start_of_turn(self):
        # at start of turn passives/statuses
        # triggers


        pass

    def end_of_turn(self):
        # AP
        self.gain_turn_AP()

        # at end of turn passives

        # status turn reduction



    def deal_damage_Base(self, move_power= 1, attack_type= None, affinity_type= None):
        # use etc here
        # deals damage with base attack in mind

        # Unique cases
        if attack_type == None:
            raw_damage = 1 * move_power
            return raw_damage
        elif not attack_type in self.stat:
            print(f"attack_type: {attack_type} not found; from deal_damage_base")
            return 1
        
        # -- start actual function --
        raw_min = self.stat[attack_type] * self.weapon_attack_min * move_power
        raw_max = self.stat[attack_type] * self.weapon_attack_max * move_power

        random.seed()
        raw_damage = random.randint(
            raw_min,
            raw_max
            )

        return raw_damage
    
    def take_damage(self, raw_damage= 0, attack_type= None, extra_info = None):
        # Take damage based on known attack type
        attdef_dict = {
            "Assault": "Assault Defense",
            "Tactics": "Tactical Defense",
            "Psi": "Psi Defense"
        }
        if attack_type in attdef_dict:
            def_value = self.stat[attdef_dict[attack_type]]
            end_damagepre = raw_damage * 100 / (100 + def_value)
        else:
            end_damagepre = raw_damage
            print(f"None damage perceived, no defense used; battler.take_damage")
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

    def apply_break_status(self):
        str_selfname = str(self.name)
        print(f"{str_selfname} has been breaked!")

        self.status["Break"] = status.Break(
            name= "Break",
            turn= None,
            strength= 1,
            afflicted_object= self
        )

    def apply_felled_status(self):
        str_selfname = str(self.name)
        print(f"{str_selfname} has been felled!")

        self.status["Felled"] = status.Felled(
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

# <-- Enemy Battler class -->
class EnemyBattler(Battler):
    def __init__(self, statsdict=None, weakness=None, status=None, name=None, battle_ref=None, move_dict=None):
        super().__init__(statsdict, weakness, status, name, battle_ref)

        # setup of move_list
        if isinstance(move_dict, dict):
            self.move_dict = move_dict
        else:
            self.move_dict = {
                "Attack": move.BaseAttackAssault()
            }

    def player(self):
        return self.battle_ref.player_battler

# <-- Player battler class -->
class PlayerBattler(Battler):
    def __init__(self, statsdict = None, weakness = None, status = None, equipment = None, equipped_moves = None, basic_attack = None, battle_ref = None):

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
        if equipped_moves == None:
            equipped_moves = {}
        if basic_attack == None:
            basic_attack = move.BaseAttackAssault()
        
        self.equipment = equipment
        self.equipped_moves = equipped_moves
        self.basic_attack = basic_attack

    def low_ap_message(self):
        str_selfname = str(self.name)
        print(
            f"{str_selfname} is too low!"
        )



# <-- battle class -->
class BattleGameplay:
    def __init__(self, player_gl, enemies_data, loop=False):
    
        # --Variable Setup--
        self.player_battler = PlayerBattler(
            statsdict = player_gl.stat,
            equipment = player_gl.equipment,
            battle_ref = self,
            equipped_moves = player_gl.equipped_moves
        )

        # enemy objects setup
        self.enemies_list = []

        for enemy_data in enemies_data:
            item = enemy_data(
                battle_ref= self
            )
            self.enemies_list.append(item)
        
        self.rename_enemy_duplicates()

        self.turn = 1
        self.exit_battle = False
        self.results = "undetermined"

        # Starts battle
        self.start_of_battle()
        if loop:
            self.battle_loop()


    def rename_enemy_duplicates(self):
        seen_names = []
        dupes = []

        for enemy in self.enemies_list:
            name = enemy.name
            if name in dupes:
                pass
            elif name in seen_names:
                pass
            else:
                seen_names.append(name)


    def rename_enemy_duplicates(self):
        # renames all duplicates in a list of enemy_objects
        # !do note that the function may have wonky naming if applied multiple times
        seen_names = []
        dupes = []

        for enemy in self.enemies_list:
            name = enemy.name
            if name in dupes:
                pass
            elif name in seen_names:
                dupes.append(name)
            else:
                seen_names.append(name)

        if len(dupes) > 0:
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            dupes_dic = {}
            for x in dupes:
                dupes_dic[x] = -1

            for enemy in self.enemies_list:
                name = enemy.name
                if name in dupes_dic:
                    dupes_dic[name] = dupes_dic[name] + 1
                    enemy.name = name + " " + alphabet[dupes_dic[name]]


    def battle_loop(self):

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

    def battle_turn(self, takeninput=None):
        # --Start of Turn--
        str_turn = str(self.turn)
        print(f"\n\n<--Turn {str_turn} -->")

        # --Player Turn--
        print("--Player's Turn--")
        self.player_battler.start_of_turn()
        pturn_active = True
        while pturn_active:
            pturn_active = self.player_turn(takeninput)

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


    def player_turn(self, takeninput=None):

        # <Status Check>
        print("")
        print_output = ""
        for enemy_battler in self.enemies_list:
            str_enemy = str(enemy_battler.name)
            str_eHP = str(enemy_battler.stat["Current HP"])
            print_output += f"{str_enemy} HP: {str_eHP}   "
        print(print_output)

        str_plCHP = str(self.player_battler.stat["Current HP"])
        str_plMHP = str(self.player_battler.stat["Max HP"])
        str_plAP = str(self.player_battler.stat["Current AP"])
        print(f"\nPlayer HP: {str_plCHP}/{str_plMHP}")
        print(f"Player AP: {str_plAP}")
        if not takeninput:
            print("\n--Choose move--")
            print("Attack (1*)| Moves | TurnPass | Exit")

        # creating a reference for the enemies
        short_name_list = []
        for enemy in self.enemies_list:
            short_name_list.append(''.join(letter for letter in enemy.name if letter.isupper()))

        if not takeninput:
            takeninput = input(">Input: ").lower()
        
        match takeninput.split(sep= ' ', maxsplit= 1):
            
            case ["exit" | "e"]:
                self.exit_battle = True
                return False

            case ["attack" | "a", *target]: 
                #target is a single string in a list
                if len(target) > 0:
                    target= target[0]
                else:
                    target= ""
                
                used_move = self.player_battler.basic_attack
                self.targeting_tool(
                    user_battler= self.player_battler,
                    enemies_list= self.enemies_list,
                    move_function= used_move,
                    target_input= target
                )
                if False:
                    self.targeting_tool(
                        user_battler= self.player_battler,
                        enemies_list= self.enemies_list,
                        move_function= move.attack,
                        target_input= target
                    )


            case ["moves" | "move" | "m", *rest_input]:

                # creates a new dict of the player_moves; 
                # but with lowercase characters and shortened characters
                dm_lower= {}
                dm_short= {}
                for cmove in self.player_battler.equipped_moves:
                    dm_lower[cmove.lower()]= self.player_battler.equipped_moves[cmove]
                    
                    key_short = ''.join(char.lower() for char in cmove if char.isupper())
                    dm_short[key_short]= self.player_battler.equipped_moves[cmove]

                if len(rest_input) == 0:    # if only "moves" is inputted
                    print('use "move {move name}"')
                    print("available moves: ")
                    for pmove in self.player_battler.equipped_moves:
                        print("> " + pmove)
                else:
                    # !consider changing this in the future
                    rinput = rest_input[0].split(maxsplit= 1)
                    input_move = rinput[0]
                    if len(rinput) < 2:
                        target = None
                    else:
                        target = rinput[-1]

                    move_dict = False
                    if input_move in self.player_battler.equipped_moves:
                        move_dict = self.player_battler.equipped_moves
                    elif input_move in dm_lower:
                        move_dict = dm_lower
                    elif input_move in dm_short:
                        move_dict = dm_short
                    else:
                        print("move not recognized")

                    if move_dict:
                        used_move = move_dict[input_move]
                        self.targeting_tool(
                            user_battler= self.player_battler,
                            enemies_list= self.enemies_list,
                            move_function= used_move,
                            target_input= target
                        )

            
            case ["turnpass" | "t" | "tp"]:
                print("turn passed")
                return False

            case _:
                print("Input not recognized")
        
        return True


    def enemy_turn(self, enemy_battler):
        # --Enemy Turn--
        enemy_battler.self_behaviour()
        

    def targeting_tool(self, user_battler, enemies_list, move_function, target_input = None):
        # targeting tool used by player battler, requires moves
        target_exists, target_battler = self.check_target(
            enemies_list = enemies_list,
            target = target_input
            )
        if target_exists == False:
            return
        
        move_function.use(user_battler, target_battler)


    def check_target(self, enemies_list, target):
        # returns true or false depending whether the target is legal
        # and also returns a reference of the legal target
        
        # target is a list with a single string

        if target == None or len(target) == 0:
        # returns the first target, if target is an empty list
            return True, enemies_list[0]
        
        # Creates 2 lists: full name and shortened name
        full_l = []
        short_l = []
        for enemy in enemies_list:
            full_l.append(enemy.name.lower())
            short_l.append(
                ''.join(char.lower() for char in enemy.name if char.isupper())
            )

        if target in short_l:
            nimdex = short_l.index(target)
            return True, enemies_list[nimdex]
        elif target in full_l:
            nimdex = full_l.index(target)
            return True, enemies_list[nimdex]
        else:
            print("Target not found, check your input")
            return False, None

