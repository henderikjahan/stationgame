from . import move_list as move  # fix this
from game.stats.stat_data import item_mods


class PlayerStat:
    def __init__(self, player):
        self.player = player

        self.basic_stats = {
            "max_HP": 50,  # Maximum Hit points
            "current_HP": 50,  # Current HP
            "max_AP": 3,  # Maximum Action points, which can be banked
            "AP_regen": 3,  # Turn Action points, determines the amount of AP the battlers can gain per turn at start
            "HP_Regen": 0,
            "more_generic_dmg": 0,
            "increased_assault_dmg": 0,
            "increased_tactics_dmg": 0,
            "increased_psi_dmg": 0,
            # "Base Attack": 5,  # Base attack stat
            # Damage reduction of receiving Physical attacks: damageReceived = 100/(100+defense)
            # "Physical Defense": 10,
            #  Damage reduction of receiving Psi attacks: damageReceived = 100/(100+defense)
            #  "Psi Defense": 10,
        }

        # pluk deze van de equipmentlijst
        self.current_mods = self.calculate_current_mods()

        self.current_total_mods = self.calculate_current_mod_totals()

        self.stat = self.calculate_current_stats()

        # pluk deze ook uit de equipment - misschien als er geen wapen is, kick of slap toevoegen
        self.moves = ["test"]

        # basic attack moet gewoon een move worden die aan elk weapon type hangt (?)
        self.basic_attack = "test"  # pluk dit uit equipment

    def calculate_current_mods(self):
        # ga door de items en pak de mods
        current_mods = []
        for item in self.player.equipped_items:
            for mod in item["mods"]:
                current_mods.append(mod)
        return current_mods

    def update_current_mods(self):
        self.current_mods = self.calculate_current_mods()

    def calculate_current_mod_totals(self):
        # make list of unique names in current_mods
        current_unique_mod_names = []
        for mod in self.current_mods:
            if (mod["modName"] not in current_unique_mod_names):
                current_unique_mod_names.append(mod["modName"])

        # go through current_mods and add all mods of the same type together
        current_total_mods = []
        for mod_name in current_unique_mod_names:
            current_total_mod = {"modName": mod_name, "value": 0}
            for mod in self.current_mods:
                if mod["modName"] == mod_name:
                    current_total_mod["value"] += mod["value"]
            current_total_mods.append(current_total_mod)

        return current_total_mods

    def update_current_mod_totals(self):
        self.current_total_mods

    def go_through_item_mods(self, current_total_mods, relation, original_stats, callback):
        result = original_stats

        for mod in current_total_mods:
            mod_info = item_mods[mod["modName"]]

            if "relation" not in mod_info or "related_basic_stat" not in mod_info:
                continue
            if mod_info["relation"] != relation:
                continue
            if mod_info["related_basic_stat"] not in self.basic_stats:
                continue

            result[mod_info["related_basic_stat"]] = callback(
                original_stats[mod_info["related_basic_stat"]], mod["value"])

        return result

    def calculate_current_stats(self):
        current_total_mods = self.calculate_current_mod_totals()

        new_flat_stats = self.go_through_item_mods(
            current_total_mods, "flat_addition", self.basic_stats, lambda x, y: x + y)

        increased_stats = self.go_through_item_mods(
            current_total_mods, "percentage_increase", new_flat_stats, lambda x, y: round(x*(1+(y/100))))

        return increased_stats

    def update_current_stats(self):
        self.stat = self.calculate_current_stats()

    def update_hp(self, amount=0):
        new_hp = self.stat["current_HP"] + amount
        new_hp = min(max(0, new_hp), self.stat["max_HP"])
        self.stat["current_HP"] = new_hp
        return self.stat["current_HP"]
