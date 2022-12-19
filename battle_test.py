# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.enemies import enemy_list as enemy
from game.moves import move_list as move
from game.stats import stats

# --setup player/enemy stat--
# psi list should contain ready to use objects
# !entries should contain NO spaces
setup_moves = {
    "FireBall": move.FireBall(),
    "CatchMe": move.CatchMe()
}

pstatdict = {
}

player_gl = stats.Stats(
    equipped_moves = setup_moves,
    statdict= pstatdict
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

# ! 19-12-2022; 
#   bezig met damage ranges en equipment handling

# to do list
# verander attack aanpassend aan de assault, tactic en psi
    # maak een nieuwe attack voor assault en maak aanpassingen betreft dat
# voeg equipment toe en damage ranges
# voeg status handling
# voeg passive handling
# pas enemy strategy toe

# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af