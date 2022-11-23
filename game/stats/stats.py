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
current_stats = basic_stats


def calculate_current_mod_totals():
    # make list of unique names in current_mods
    current_unique_mod_names = []
    for mod in current_mods:
        if (mod["modName"] not in current_unique_mod_names):
            current_unique_mod_names.append(mod["modName"])

    # go through current_mods and add all mods of the same type together
    current_total_mods = []
    for mod_name in current_unique_mod_names:
        current_total_mod = {"modName": mod_name, "value": 0}
        for mod in current_mods:
            if mod["modName"] == mod_name:
                current_total_mod["value"] += mod["value"]
        current_total_mods.append(current_total_mod)

    return current_total_mods


def go_through_item_mods(current_total_mods, relation, original_stats, callback):
    result = original_stats

    for mod in current_total_mods:
        mod_info = item_mods[mod["modName"]]

        if "relation" not in mod_info or "related_basic_stat" not in mod_info:
            continue
        if mod_info["relation"] != relation:
            continue
        if mod_info["related_basic_stat"] not in basic_stats:
            continue

        result[mod_info["related_basic_stat"]] = callback(
            original_stats[mod_info["related_basic_stat"]], mod["value"])

    return result


def calculate_current_stats():
    current_total_mods = calculate_current_mod_totals()

    new_flat_stats = go_through_item_mods(
        current_total_mods, "flat_addition", basic_stats, lambda x, y: x + y)

    increased_stats = go_through_item_mods(
        current_total_mods, "percentage_increase", new_flat_stats, lambda x, y: round(x*(1+(y/100))))

    return increased_stats


def remove_item_mods(id):
    global current_mods
    new_mods = list(filter(lambda x: x["source_item_ID"] != id, current_mods))
    current_mods = new_mods
    return current_mods


def add_item_mods(new_mods):
    global current_mods
    current_mods = current_mods + new_mods
    return current_mods
