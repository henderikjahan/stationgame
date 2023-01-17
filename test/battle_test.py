# --sys.path.append --
import sys
sys.path.append(".")


# --imports Gameplay--
from game.battle import battle_gameplay as bgp

# --imports--
from game.character import enemies as enemy
from game.character.character import Player
from game.moves import move_list as move
from game.stats.stats import CharacterStats

# --setup player/enemy stat--
# moves should be determined by Character equipment.
setup_moves = {
    "FireBall": move.FireBall(),
    "CatchMe": move.CatchMe()
}
playerstat2 = {
    "HP_current": 100,  # Current HP
    "HP_max": 100,  # Maximum Hit points
    "HP_regen": 0,

    "AP_current": 0,
    "AP_max": 3,  # Maximum Action points, which can be banked
    "AP_regen": 3,  # Turn Action points, determines the amount of AP the battlers can gain per turn at start

    "generic": 0,
    "assault": 10,
    "tactics": 10,
    "psi": 10,

    "generic defense": 1,
    "assault defense": 1,
    "tactics defense": 1,
    "psi defense": 1,
}

player = Player()

player.moves |= setup_moves
player.stats.current_stat |= playerstat2


enemies = [
    enemy.SpoiledEggBoy,
    enemy.BorgerBurger,
]
    # enemies expects a list of Enemy character classes, which are NOT instantiated (yet)!
    # consider changing this, for variable changing the objects


# --starts battle--
random_battle = bgp.BattleGameplay(
    player = player,
    enemies = enemies,
    loop = True
)

# ! 19-12-2022;
#   bezig met damage ranges en equipment handling

# 2-1-2022
    # Bezig met statuses en passives
        # bekijk of je de felled status met de generic battler.apply_status kan gebruiken


# to do list
# verander attack aanpassend aan de assault, tactic en psi
    # maak een nieuwe attack voor assault en maak aanpassingen betreft dat
# voeg equipment toe en damage ranges
# voeg status handling
# voeg passive handling

# <-- Notes -->

# gebruik math.ceil( x ), rond omhoog af en is een int
# math.floor( x ), rond omlaag af
