
from .movebase import MoveBase

# <-- Enemy Moves -->

# -- Status Moves --
class RottenEgg(MoveBase):
    def __init__(self):
        super().__init__()
        self.name = "RottenEgg"
        self.ap_cost = 3
        self.move_power = 0.1
        self.attack_type = "Tactics"
    
    def use(self, user_battler, target_battler):
        if not self.check_legality_target(target_battler= target_battler):
            return False
        
        continue_move = user_battler.reduce_self_ap(self.ap_cost)
        # continue move is True or False, depending whether the cost can be paid

        if continue_move:
            # message
            str_userbattler = str(user_battler.name)
            str_targetbattler = str(target_battler.name)
            print( f"{str_userbattler} used {self.name} on {str_targetbattler}!")

            # actual move
            raw_damage = user_battler.deal_damage_Base(
                attack_type= self.attack_type,
                move_power= self.move_power
                )

            target_battler.take_damage(
                raw_damage= raw_damage,
                attack_type= self.attack_type
            )

        else:
            # ap cost too low
            str_userbattler = str(user_battler.name)
            print( f"{str_userbattler}'s AP is too low!")