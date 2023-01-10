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
# psi list should contain ready to use objects
# !entries should contain NO spaces
# moves should be determined by Character equipment.
setup_moves = {
    "FireBall": move.FireBall(),
    "CatchMe": move.CatchMe()
}

player = Player()

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
