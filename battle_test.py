# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.battle import player_stat
from game.battle import enemy_list as enemy
from game.battle import move_list as move
from game.stats import stats

# --setup player/enemy stat--
# psi list should contain ready to use objects
setup_psi = {
    "Fire": move.Fire()
}

player_gl = stats.Stats(
    psi= setup_psi
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
# verander battler stat in gelijkenis van "stats"
# verander attack aanpassend aan de assault, tactic en psi
    # maak een nieuwe attack voor assault en maak aanpassingen betreft dat
# verander psi -> "nog onbepaald", dit "moves" noemen kan verwarrend zijn voor coderen
# maak vorderingen in move van (player) battle_gameplay

# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af