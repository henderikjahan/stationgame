

class Status:
    def __init__(self, name= None, turn= None, strength= None, afflicted_object = None):
        
        if name == None:
            name = "Unnamed"
        if turn == None:
            turn= None
        if strength == None:
            strength= 0

        self.name = name
        self.turn = turn
        self.strength = strength
        self.afflicted = afflicted_object   # add something when handling afflicted_object= None
        
        # messaging
        self.message_hit = "{afflicted_name} has been afflicted by {status_name}!"


    def print_message_hit(self):
        message= self.message_hit.format(
            afflicted_name= self.afflicted.name,
            status_name= self.name
            )
        
        if True:
            print(message)

        return message

    def clear_self(self):
        self.afflicted.status.pop(self.name)

    def turn_reduction(self, minus_turns= 1, pop_status= True):
        if isinstance(self.turn, int):
            self.turn -= minus_turns
            
            if pop_status == False and self.turn <= 0:
                # happens when pop_status == False; useful for specific healing effects
                self.turn = 1

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



class Break(Status):    #old and unused
    def __init__(self, name=None, turn=None, strength=0, afflicted_object=None):
        super().__init__(name, turn, strength, afflicted_object)

    def start_turn_effect(self):
        self.clear_self()

class Felled(Status):
    def __init__(self, name=None, turn=None, strength=None, afflicted_object=None):
        super().__init__(name, turn, strength, afflicted_object)
        self.message_hit= "{afflicted_name} has been felled!"

    def immediate_effect(self):
        self.afflicted.stat["AP_current"] = 0

        if self.afflicted.battle_ref != None:
            self.afflicted.battle_ref.check_victory()


class Poison(Status):
    def end_turn_effect(self):
        # message
        name = str(self.afflicted.name)
        damage = self.strength
        print(f"{name} has taken {damage} poison damage")

        # action
        self.afflicted.stat["HP_current"] -= self.strength
        




# status example
user_status_list = {
    "Felled": "FelledStatus object",
    "Poison": "PoisonStatus object"
}