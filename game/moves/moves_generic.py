from setuptools import Command
from game.tools import print
from .movebase import MoveBase


# <--- Moves --->

# -- Basic attacks --
class BaseAttackAssault(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "assault"
        self.affinity = None


class BaseAttackTactics(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "assault"
        self.affinity = None

        
class BaseAttackPsi(MoveBase):
    def __init__(self):
        super().__init__()

        self.name = "BaseAttackAssault"
        self.ap_cost = 1
        self.move_power = 1.0
        self.attack_type = "assault"
        self.affinity = None
