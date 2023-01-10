
from .moves_generic import *
from .moves_enemy import *


# add () behind the dict to create the related object
#   example: 
#       some_variable= movecoll["BAA"]()
# !"the moves codes" or "movecoll.KEYS" may change in the future!

movecoll= {
    "BAA": BaseAttackAssault,
    "BAT": BaseAttackTactics,
    "BAP": BaseAttackPsi,
    "FB": FireBall,
    "CM": CatchMe,
    "RE": RottenEgg
}
