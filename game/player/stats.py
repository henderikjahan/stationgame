# TODO move this info to mod_data.py
available_mods = {
    "flat_to_max_hp": {"related_basic_stat": "max_HP", "relation": "flat_addition"},
    "increased_max_hp": {"related_basic_stat": "max_HP", "relation": "percentage_increase"}
}

current_mods = [
    {"modName": "flat_to_max_hp", "value": 40,
        "source": "item", "source_item": "itemID"},
    {"modName": "flat_to_max_hp", "value": 20,
        "source": "item", "source_item": "itemID"},
    {"modName": "increased_max_hp", "value": 10,
        "source": "item", "source_item": "itemID"},
]


basic_stats = {"max_HP": 50, "max_AP": 3, "AP_regen": 3}

# Should current hp and current ap be stored here?
current_stats = {
    "total_HP": {"value": 110, "statText": "110 Hit Points"}
}


def caclculate_current_stats():
    print("calculate stats from currentmods and basicstats")


def remove_item_mods(id):
    print("removes all mods added by an item with a certain id")
