

class status:
    def __init__(self, name= "Unnamed", turn= None, strength= 0, afflicted_object = None):
        self.name = name
        self.turn = turn
        self.strength = strength
        self.afflicted_object = afflicted_object

    def turn_reduction(self, minus_turns= 1):
        if isinstance(self.turn, int):
            self.turn -= minus_turns
            if self.turn <= 0:
                self.afflicted_object.status.pop(self.name)

    def effect(self):
        pass


class felled(status):
    def effect(self):
        pass

class poison(status):
    def effect(self):
        self.user_class.stat["Current HP"] -= self.strength



# status example
user_status_list = {
    "Felled": "Felled_Status object",
    "Poison": "Poison_Status object"
}