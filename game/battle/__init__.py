# --imports Gameplay--
import battle_gameplay as bgp

# <!> testing <!>
# remove everything under testing when importing this file


# --imports--
import player_stat

# --setup player stat--
player_gl = player_stat.playerstat()
enemies = [
    {
        "Enemy Name": "Borger Burger",
        "Enemy Stats": {
            "Current HP": 15,
            "Max HP": 15,

            "Base Attack": 5,
            "Physical Defense": 0,
            "Psi Defense": 0,

            "Current AP": 0,
            "Turn AP": 1,
            "Max AP": 5
            },
        "Enemy Weakness": []
    },
    {
        "Enemy Name": "Magical Mayonaise",
        "Enemy Stats": {
            "Current HP": 8,
            "Max HP": 8,

            "Base Attack": 8,
            "Physical Defense": 0,
            "Psi Defense": 0,

            "Current AP": 0,
            "Turn AP": 1,
            "Max AP": 5
            },
        "Enemy Weakness": []
    }
]

# stat note
if False:
    stat = {
        "Current HP": 10,
        "Max HP": 10,

        "Base Attack": 5,
        "Physical Defense": 0,
        "Psi Defense": 0,

        "Current AP": 0,
        "Turn AP": 1,
        "Max AP": 5
        }



# --starts battle--
random_battle = bgp.Battle_Gameplay(
    player_gl= player_gl,
    enemies_data= enemies
    )




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af

# at commands, mayhap