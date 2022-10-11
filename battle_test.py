# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.battle import player_stat
from game.battle import enemy_list as enemy

# --setup player/enemy stat--
player_gl = player_stat.PlayerStat()
    # player_gl expects a "playerstat object"

enemies = [
    enemy.BorgerBurger,
    enemy.MagicalMayonaise
]
    # enemies expects a list of enemy classes, which are NOT objects (yet)!


# --starts battle--
random_battle = bgp.BattleGameplay(
    player_gl= player_gl,
    enemies_data= enemies,
    loop= True
)




# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af