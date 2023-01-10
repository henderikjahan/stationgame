#from . import move_list as move  # fix this
from game.stats.stat_data import item_mods


class CharacterStats:
    def __init__(self, character, stats_override={}):
        self.character = character

        self.basic_stats = {
            "HP_current": 50,  # Current HP
            "HP_max": 50,  # Maximum Hit points
            "HP_regen": 0,

            "AP_current": 0,
            "AP_max": 3,  # Maximum Action points, which can be banked
            "AP_regen": 3,  # Turn Action points, determines the amount of AP the battlers can gain per turn at start

            "generic": 0,
            "assault": 0,
            "tactics": 0,
            "psi": 0,

            "generic defense": 1,
            "assault defense": 1,
            "tactics defense": 1,
            "psi  defense": 1,

            "increased_generic_dmg": 0,
            "increased_assault_dmg": 0,
            "increased_tactics_dmg": 0,
            "increased_psi_dmg": 0,
            # "Base Attack": 5,  # Base attack stat
            # Damage reduction of receiving Physical attacks: damageReceived = 100/(100+defense)
            # "Physical Defense": 10,
            #  Damage reduction of receiving Psi attacks: damageReceived = 100/(100+defense)
            #  "Psi Defense": 10,
        } | stats_override

        self.status = {}

        # TODO: pluk mods van de equipmentlijst, self.character.equipment
        self.current_mods = self.calculate_current_mods()
        self.current_total_mods = self.calculate_current_mod_totals()
        self.current_stat = self.calculate_current_stats()


    def calculate_current_mods(self):
        # ga door de items en pak de mods
        current_mods = []
        for item in self.character.equipment:
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

    def go_through_item_mods(
        self, current_total_mods, relation,
        original_stats, callback
    ):
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
            current_total_mods, "flat_addition",
            self.basic_stats, lambda x, y: x + y)

        increased_stats = self.go_through_item_mods(
            current_total_mods, "percentage_increase",
            new_flat_stats, lambda x, y: round(x*(1+(y/100))))

        return increased_stats

    def update_current_stats(self):
        self.current_stats = self.calculate_current_stats()

    # Stat-specific methods start here
    def update_hp(self, amount=0):
        new_hp = self.current_stats["HP_current"] + amount
        new_hp = min(max(0, new_hp), self.current_stats["HP_max"])
        self.current_stats["HP_current"] = new_hp
        return self.current_stats["HP_current"]

    def update_ap(self, amount=0):
        new_ap = self.current_stats["AP_current"] + amount
        new_ap = min(max(0, new_ap), self.current_stats["AP_max"])
        self.current_stats["AP_current"] = new_ap
        return self.current_stats["AP_current"]