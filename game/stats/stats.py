current_mods = [
    {"modName": "flat_to_max_hp", "value": 40,
        "source": "item", "source_item": "itemID"},
    {"modName": "flat_to_max_hp", "value": 20,
        "source": "item", "source_item": "itemID"},
    {"modName": "increased_max_hp", "value": 10,
        "source": "item", "source_item": "itemID"},
]


basic_stats = {"max_HP": 50, "max_AP": 3,
               "AP_regen": 3, "HP_Regen": 0, "more_generic_dmg": 0,
               "increased_assault_dmg": 0, "increased_tactics_dmg": 0,
               "increased_psi_dmg": 0, }

# Should current hp and current ap be stored here?
current_stats = {
    "total_HP": {"value": 110, "statText": "110 Hit Points"}
}


def caclculate_current_stats():
    print("calculate stats from currentmods and basicstats")


def remove_item_mods(id):
    print("removes all mods added by an item with a certain id")
