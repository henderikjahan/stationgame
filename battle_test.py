# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.enemies import enemy_list as enemy
from game.moves import move_list as move
from game.stats import stats

# --setup player/enemy stat--
# psi list should contain ready to use objects
setup_moves = {
    "Fire": move.Fire(),
    "Attack": move.Attack()
}

player_gl = stats.Stats(
    equipped_moves = setup_moves
    )
    # player_gl expects a "playerstat object"


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
# verander attack aanpassend aan de assault, tactic en psi
    # maak een nieuwe attack voor assault en maak aanpassingen betreft dat
# maak vorderingen in move van (player) battle_gameplay
    # !hiermee bezig

# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af