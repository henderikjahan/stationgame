import math


# <-- general battler class -->
# For editing stats and mechanics which affects all battlers
class Battler:
    def __init__(self, statsdict = {}, weakness = [], status = {}, name = "Unnamed"):
        
        self.name = name
        self.stat_reset(statsdict)
        self.weakness = weakness
        self.status = status

    def stat_reset(self, statsdict):
        # reset stats to the inputed statsdict
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


    def deal_damage_Base(self, command_power):
        # deal damage with base attack in mind
        raw_damage = self.stat["Base Attack"] * command_power

        return raw_damage
    
    def take_damage(self, raw_damage):
        # Take damage based on physical defense
        end_damagepre = raw_damage * 100 / (100 + self.stat["Physical Defense"])
        end_damage = math.ceil(end_damagepre)

        self.stat["Current HP"] -= end_damage

        return end_damage   # the return is for the printing messages

    def check_self_hp(self):
        # checks whether the battler died
        if self.stat["Current HP"] <= 0.0:
            print(str(self.name) + " has died!")
            # lacks removing self or messaging a control function

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
    def __init__(self, statsdict = {}, weakness = [], status = {}, equipment = {}, psi = {}):

        Battler.__init__(self, 
        statsdict = statsdict, 
        weakness = weakness, 
        status = status,
        name = "Player"
        )

        self.equipment = equipment
        self.psi = psi

    def low_ap_message(self):
        print(
            str(self.name) + " is too low!"
        )

# <-- battle functions -->
# -main battle function-
def battle(player_gl, enemies_data):
    
    print("\nStart Battle\n")

    # --Variable Setup--
    player_battler = Player_Battler(
        statsdict = player_gl.stat,
        equipment = player_gl.equipment,
        psi = player_gl.psi
    )

    # Change everything enemy related later, due to there being only one enemy
    enemies_list = []
    for enemy_data in enemies_data:
        item = Battler(
            name = enemy_data["Enemy Name"],
            statsdict = enemy_data["Enemy Stats"],
            weakness = enemy_data["Enemy Weakness"]
        )
        enemies_list.append(item)
    
    # Start of battle handling
    player_battler.start_of_battle()
    for enemy_battler in enemies_list:
        enemy_battler.start_of_battle()

    turn = 1

    while True:
        # --Start of turn--
        player_battler.start_of_turn()
        for enemy_battler in enemies_list:
            enemy_battler.start_of_turn()

        print("\n\n<--Turn " + str(turn) + " -->")

        # --Player Turn--
        print("--Player's Turn--")
        while True: #loop is for the "case _"
            # <Status Check>
            print("")
            print_output = ""
            for enemy_battler in enemies_list:
                print_output += str(enemy_battler.name) + " HP:" + str(enemy_battler.stat["Current HP"]) + "   "
            print(print_output)

            print("\nPlayer HP: " + str(player_battler.stat["Current HP"]) + "/" + str(player_battler.stat["Max HP"]))
            print("Player AP: " + str(player_battler.stat["Current AP"]))

            print("\n--Choose command--")
            print("Attack (1*)| Psi | TurnPass | Exit")

            takeninput = input(">Input: ").lower()
            
            match takeninput.split():
                
                case ["exit" | "e"]:
                    print("battle exited")
                    return
                    # exit from this function and breaks the loop
                    # Caution! Has Return!

                case ["attack" | "a"]:
                    command_attack(
                        user_battler= player_battler,
                        target_battler= enemies_list[0]
                    )
                    

                case ["psi" | "p"]:
                    print("choose psi")
                    # Doesn't work at the moment
                    while False:
                        takeninput = input("Input: ")
                
                case ["turnpass" | "t" | "tp"]:
                    print("turn passed")
                    break

                case _:
                    print("Input not recognized")
        

        # --Enemy Turn--
        for enemy_battler in enemies_list:
            command_attack(
                user_battler = enemy_battler, 
                target_battler = player_battler)

        # >replace above with enemy strategy function, eventually

        # --End of turn--

        turn += 1


# -smaller battle functions-
def fell_battler(battler):
    del battler


# function for checking every battler's hp for hitting 0 or less


# -command function-
def command_attack(user_battler, target_battler):
    
    ap_cost = 1
    continue_command = user_battler.reduce_self_ap(ap_cost)
    # continue command is True or False, depending whether the cost can be paid

    if continue_command:

        command_power = 1.0
        
        raw_damage = user_battler.deal_damage_Base(command_power= command_power)
        
        taken_damage = target_battler.take_damage(raw_damage= raw_damage)
        print(str(user_battler.name) + " attacked " + str(target_battler.name) + "!")
        print(str(target_battler.name) + " has taken " + str(taken_damage) + " damage!")

    else:
        # ap cost too low
        print(str(user_battler.name) + "'s AP is too low!")



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
if True:
    battle(
        player_gl = player_gl,
        enemies_data = enemies
    )




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af

# at commands, mayhap
