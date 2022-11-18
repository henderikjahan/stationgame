from game.stats.stat_data import item_mods

current_mods = [
    {"modName": "flat_to_max_hp", "value": 40,
        "source": "item", "source_item_ID": 1},
    {"modName": "flat_to_max_hp", "value": 20,
        "source": "item", "source_item_ID": 2},
    {"modName": "increased_max_hp", "value": 10,
        "source": "item", "source_item_ID": 3},
]


basic_stats = {"max_HP": 50, "max_AP": 3,
               "AP_regen": 3, "HP_Regen": 0, "more_generic_dmg": 0,
               "increased_assault_dmg": 0, "increased_tactics_dmg": 0,
               "increased_psi_dmg": 0, }

# Should current hp and current ap be stored here?
current_stats = {
    "total_HP": {"value": 110, "statText": "110 Hit Points"}
}


def calculate_current_mod_totals():
    # make list of unique names in current_mods
    current_mod_names = []
    for mod in current_mods:
        if (mod["modName"] not in current_mod_names):
            current_mod_names.append(mod["modName"])

    # go through current_mods and add all mods of the same type together
    current_total_mods = []
    for mod_name in current_mod_names:
        # find and total all mods in current_mods
        current_stat = {"modName": mod_name, "value": 0}
        for mod in current_mods:
            if mod["modName"] == mod_name:
                current_stat["value"] += mod["value"]
        current_total_mods.append(current_stat)

    return current_total_mods


def calculate_current_stats():
    current_total_mods = calculate_current_mod_totals()

    # for each current_total_mod, look for the related stat, if additive, add to base stats
    new_flat_stats = basic_stats
    for mod in current_total_mods:
        mod_info = item_mods[mod["modName"]]
        if mod_info["relation"] == "flat_addition":
            if mod_info["related_basic_stat"] in basic_stats:
                new_flat_stats[mod_info["related_basic_stat"]] += mod["value"]

    # for each current_total_mod, look for the related stat, if increase, increase base amount by it
    increased_stats = new_flat_stats
    for mod in current_total_mods:
        mod_info = item_mods[mod["modName"]]
        if mod_info["relation"] == "percentage_increase":
            if mod_info["related_basic_stat"] in basic_stats:
                new_flat_stats[mod_info["related_basic_stat"]
                               ] = round(new_flat_stats[mod_info["related_basic_stat"]] * (1+(mod["value"]/100)))

    return (increased_stats)


def remove_item_mods(id):
    global current_mods
    new_mods = list(filter(lambda x: x["source_item_ID"] != id, current_mods))
    current_mods = new_mods
    return current_mods
