import math
import command_list as command
import status_list as status

# <-- general battler class -->
# For editing stats and mechanics which affects all battlers
class Battler:
    def __init__(self, statsdict = {}, weakness = [], status = {}, name = "Unnamed", battle_ref = None):
        
        self.name = name
        self.set_true_stat(statsdict)
        self.weakness = weakness
        self.status = status
        self.battle_ref = battle_ref

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
        # at start of battle passives


        pass
        

    def start_of_turn(self):
        # at start of turn passives/statuses


        # AP
        self.stat["Current AP"] += self.stat["Turn AP"]
        if self.stat["Current AP"] > self.stat["Max AP"]:
            self.stat["Current AP"] = self.stat["Max AP"]

    def end_of_turn(self):
        # at end of turn passives

        pass

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
        print(str(self.name) + " has taken " + str(end_damage) + " damage!")

        # checks whether it's felled
        if self.stat["Current HP"] <= 0.0:
            self.apply_felled_status()

        return end_damage   # Returns resulting damage

    def apply_felled_status(self):
        print(str(self.name) + " has been felled!")

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


    # to-do in battler:
    #   status handling
    #   passive handling
    #   


# <-- Player battler class -->
class Player_Battler(Battler):
    def __init__(self, statsdict = {}, weakness = [], status = {}, equipment = {}, psi = {}, battle_ref = None):

        Battler.__init__(self, 
        statsdict = statsdict, 
        weakness = weakness, 
        status = status,
        name = "Player",
        battle_ref= battle_ref
        )

        self.equipment = equipment
        self.psi = psi

    def low_ap_message(self):
        print(
            str(self.name) + " is too low!"
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
            item = Battler(
                name = enemy_data["Enemy Name"],
                statsdict = enemy_data["Enemy Stats"],
                weakness = enemy_data["Enemy Weakness"],
                battle_ref = self
            )
            self.enemies_list.append(item)
        
        self.turn = 1
        self.exit_battle = False

        # Starts battle
        self.battle_loop()

    def battle_loop(self):

        self.start_of_battle()
        
        while True:

            self.battle_turn()

            if self.exit_battle == True:
                print("battle exited")
                break
        
        # add results here


    def check_victory(self):
        # checks whether the battle can be ended when either party is fully felled
        player = self.player_battler
        enemies = self.enemies_list

        # checks player for felled status
        if "Felled" in player.status:
            self.exit_battle = True
            print("\nThe Player's been felled!")
            return

        # checks all enemies for felled status
        felled_count = 0
        for enemy in enemies:
            if "Felled" in enemy.status:
                felled_count += 1

        if felled_count == len(enemies):
            self.exit_battle = True
            print("\nAll enemies has been felled!")
            return


    def start_of_battle(self):
        print("\nStart Battle\n")
        # Start of battle handling per battler
        self.player_battler.start_of_battle()
        for enemy_battler in self.enemies_list:
            enemy_battler.start_of_battle()

    def battle_turn(self):
        # --Start of turn--
        self.player_battler.start_of_turn()
        for enemy_battler in self.enemies_list:
            enemy_battler.start_of_turn()

        print("\n\n<--Turn " + str(self.turn) + " -->")

        # --Player Turn--
        print("--Player's Turn--")
        pturn_active = True
        while pturn_active:
            pturn_active = self.player_turn()

            if self.exit_battle == True:
                # escape from battle
                return  # return is used, so that enemy doesn't get a turn
        

        # enemy actions
        for enemy_battler in self.enemies_list:
            self.enemy_turn(enemy_battler= enemy_battler)


        # --End of turn--
        self.turn += 1


    def player_turn(self):

        # <Status Check>
        print("")
        print_output = ""
        for enemy_battler in self.enemies_list:
            print_output += str(enemy_battler.name) + " HP:" + str(enemy_battler.stat["Current HP"]) + "   "
        print(print_output)

        print("\nPlayer HP: " + str(self.player_battler.stat["Current HP"]) + "/" + str(self.player_battler.stat["Max HP"]))
        print("Player AP: " + str(self.player_battler.stat["Current AP"]))

        print("\n--Choose command--")
        print("Attack (1*)| Psi | TurnPass | Exit")

        takeninput = input(">Input: ").lower()
        
        match takeninput.split():
            
            case ["exit" | "e"]:
                self.exit_battle = True
                return False

            case ["attack" | "a"]:
                command.attack(
                    user_battler= self.player_battler,
                    target_battler= self.enemies_list[0]
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

        command.attack(
            user_battler = enemy_battler,
            target_battler = self.player_battler)

        # >replace above with enemy strategy function, eventually





# <!> testing <!>
# remove everything under testing when importing this file


# --imports--
import player_stat

# --setup player stat--
player_gl = player_stat.playerstat()
enemies = [
    {
        "Enemy Name": "Borger Burger",
        "Enemy Stats": {},
        "Enemy Weakness": []
    }
    
]




# --starts battle--
random_battle = Battle_Gameplay(
    player_gl= player_gl,
    enemies_data= enemies
    )




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af

# at commands, mayhap
