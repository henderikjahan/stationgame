
from .moves_generic import *
from .moves_enemy import *
from .moves_player import *

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


# use 'get_info' to get more information of the move in a tuple
# !may need to be reworked
def get_info(movelist):
    list_moves = []
    for key in movelist:
        moveinfo= movelist[key]().move_info()
        moveinfo["key"]= key
        list_moves.append(moveinfo)
    
    return tuple(list_moves)