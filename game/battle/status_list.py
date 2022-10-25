

class Status:
    def __init__(self, name= None, turn= None, strength= 0, afflicted_object = None):
        
        if name == None:
            name = "Unnamed"
        if strength == None:
            strength = 0

        self.name = name
        self.turn = turn
        self.strength = strength
        self.afflicted = afflicted_object

        self.immediate_effect()

    def clear_self(self):
        self.afflicted.status.pop(self.name)

    def turn_reduction(self, minus_turns= 1, pop_status= True):
        if isinstance(self.turn, int):
            self.turn -= minus_turns
            if pop_status == True and self.turn <= 0:
                self.clear_self()

    def immediate_effect(self):
        pass

    def start_turn_effect(self):
        pass

    def end_turn_effect(self):
        pass

    def buff(self, stat_name):
        target_stat = None

        if stat_name == target_stat:
            return self.strength
        else:
            return 0



class Break(Status):
    def start_turn_effect(self):
        self.clear_self()


class Felled(Status):
    def immediate_effect(self):
        self.afflicted.stat["Current AP"] = 0


class Poison(Status):
    def end_turn_effect(self):
        self.user_class.stat["Current HP"] -= self.strength



# status example
user_status_list = {
    "Felled": "FelledStatus object",
    "Poison": "PoisonStatus object"
}