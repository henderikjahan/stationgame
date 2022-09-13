import math


# <-- general battler class -->
# For editing stats and mechanics which affects all battlers
class Battler:
    def __init__(self, statsdict = {}, weakness = [], status = {}, name = "Unnamed"):
        
        self.name = name
        self.stat_reset(statsdict)
        self.weakness = weakness
        self.status = status
        self.ap = self.stat["AP"]

    def stat_reset(self, statsdict):
        # reset stats to the inputed statsdict
        # here under are the base stats
        self.stat = {
            "Current HP": 10,
            "Max HP": 10,
            "Base Attack": 5,
            "Physical Defense": 0,
            "Psi Defense": 0,
            "AP": 1
            }

        for entry in statsdict:
            self.stat[entry] = statsdict[entry]
    

    def deal_damage(self, command_power):

        raw_damage = self.stat["Base Attack"] * command_power

        return raw_damage
    

    def take_damage(self, raw_damage):
        
        end_damagepre = raw_damage * 100 / (100 + self.stat["Physical Defense"])
        end_damage = math.ceil(end_damagepre)

        self.stat["Current HP"] -= end_damage

        return end_damage   # the return is for the printing messages


    def check_self_hp(self):
        # checks whether the battler died
        if self.stat["Current HP"] <= 0.0:
            print(str(self.name) + " has died!")
            # lacks removing self

    def check_self_ap(self, cost = 1):
        if self.stat["AP"] < cost:
            return False
        else:
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


# <-- battle functions -->
# -main battle function-
def battle(player_gl, enemies):
    
    print("\nStart Battle\n")

    # --Variable Setup--
    player_battler = Player_Battler(
        statsdict = player_gl.stat,
        equipment = player_gl.equipment,
        psi = player_gl.psi
    )

    # Change everything enemy related later, due to there being only one enemy
    enemy_battler = Battler(
        name = enemies["Enemy Name"],
        statsdict = enemies["Enemy Stats"],
        weakness = enemies["Enemy Weakness"]
    )
    
    turn = 1

    while True:
        # --Start of turn--
        print("\n\n<--Turn " + str(turn) + " -->")

        # --Player Turn--
        print("--Player's Turn--")
        while True: #loop is for the "case _"
            # <Status Check>
            print("\nPlayer HP: " + str(player_battler.stat["Current HP"]) + "/" + str(player_battler.stat["Max HP"]))
            print("Player AP: " + str(player_battler.stat["AP"]))

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
                        target_battler= enemy_battler
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

        # >replace above with enemy strategy function, eventually

        # --End of turn--

        turn += 1


# -smaller battle functions-



# function for checking every battler's hp for hitting 0 or less


# -command function-
def command_attack(user_battler, target_battler):
    apcost = 1

    if user_battler.ap < apcost:
        print("user doesn't have enough AP")
        # change message
    else:
        user_battler.stat

        command_power = 1.0
        
        raw_damage = user_battler.deal_damage(command_power= command_power)
        
        taken_damage = target_battler.take_damage(raw_damage= raw_damage)

        print(str(target_battler.name) + " has taken " + str(taken_damage) + " damage!")





# <!> testing <!>
# remove everything under testing when importing this file


# --imports--
import player_stat

# --setup player stat--
player_gl = player_stat.playerstat()
enemies = {
        "Enemy Name": "Borger Burger",
        "Enemy Stats": {},
        "Enemy Weakness": []
    }




        

# --starts battle--
battle(
    player_gl = player_gl,
    enemies = enemies
)




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af

# at commands, mayhap
