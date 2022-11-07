# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.battle import player_stat
from game.battle import enemy_list as enemy
from game.battle import move_list as move

# --setup player/enemy stat--
# psi list should contain ready to use objects
setup_psi = {
    "Fire": move.Fire()
}

player_gl = player_stat.PlayerStat(
    psi= setup_psi
    )
    # player_gl expects a "playerstat object"

# ! 24-10, was bezig met psi implementeren in het spel

enemies = [
    enemy.BorgerBurger,
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

# to do list
# rename moves -> moves
# verander stat bij player battler en global betreft discord post

# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af