# --imports Gameplay--
import battle_gameplay as bgp

# --imports--
import player_stat
import enemy_list as enemy

# --setup player/enemy stat--
player_gl = player_stat.playerstat()
    # player_gl expects a "playerstat object"

enemies = [
    enemy.Borger_Burger,
    enemy.Magical_Mayonaise
]
    # enemies expects a list of enemy classes, which are NOT objects (yet)!


# --starts battle--
random_battle = bgp.Battle_Gameplay(
    player_gl= player_gl,
    enemies_data= enemies
    )




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af