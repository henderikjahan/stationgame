# TODO deal with negative mod values - need special descriptions for those
# Maybe prevent only negative mods spawning on an item

import random
from math import floor
from item_bases_data import base_types
from mod_data import item_mods


def generate_item(
    item_level: int = 0,
    instability: int = 0,
):
    def select_base_type():
        eligible_base_types = {k: v for (k, v) in base_types.items() if (
            ("minimumItemLvl" not in v or v["minimumItemLvl"] <= item_level)
            and ("minimumInstabilityLvl" not in v or v["minimumInstabilityLvl"] <= instability)
        )}
        ordered_eligible_base_types_names = list(eligible_base_types)
        ordered_eligible_base_types_weights = [base_types[x]["base_weight"]
                                               for x in ordered_eligible_base_types_names]
        selectedBaseType = random.choices(
            ordered_eligible_base_types_names, weights=ordered_eligible_base_types_weights, k=1)[0]

        return base_types[selectedBaseType]

    def roll_mod(
        mod: any,
        item_level: int,
        instability: int,
        base_type: any,
    ):
        if "instability_multiplier" in base_type:
            instability = instability * base_type["instability_multiplier"]

        range = mod["base_range"] + \
            (mod["base_range_instablity_scaling"] * instability)
        lowpoint = mod["mid_point"] - range
        highpoint = mod["mid_point"] + range + \
            (mod["high_point_item_level_scaling"] * item_level)

        mod_roll = floor(random.uniform(lowpoint, highpoint))
        for magnitude_modifier_tag in mod["base_tag_magnitude_modifiers"]:
            if magnitude_modifier_tag in base_type["base_tags"]:
                mod_roll = mod_roll * \
                    mod["base_tag_magnitude_modifiers"][magnitude_modifier_tag]

        if "mod_multiplier" in base_type:
            mod_roll = mod_roll * base_type["mod_multiplier"]

        mod_text = mod["description"].replace("$$", str(int(mod_roll)))

        return mod_text

    def generate_mods(
        base_type: any,
        mod_amount: int
    ):
        eligible_mods = {k: v for (k, v) in item_mods.items() if (
            ("minimum_item_lvl" not in v or v["minimum_item_lvl"]
             <= item_level)
            and ("minimum_instability_lvl" not in v or v["minimum_instability_lvl"] <= instability)
        )}
        ordered_eligible_mod_names = list(eligible_mods)
        ordered_eligible_mod_weights = []

        base_tags = base_type["base_tags"]
        for mod_name in ordered_eligible_mod_names:
            item_mod = item_mods[mod_name]
            mod_weight = item_mod["mod_weight"]

            if "base_tag_weigth_modifiers" in item_mod:
                for base_tag in base_tags:
                    if base_tag in item_mod["base_tag_weigth_modifiers"]:
                        amount_to_modify_tag = item_mod["base_tag_weigth_modifiers"][base_tag]
                        mod_weight = mod_weight * amount_to_modify_tag
            ordered_eligible_mod_weights.append(mod_weight)

        selected_mods = []

        while (len(selected_mods) < mod_amount):
            # check if no mods are left over, if so, exit while loop
            if (max(ordered_eligible_mod_weights) == 0):
                break

            # select a mod, append it and set its weight to zero
            selected_mod = random.choices(
                ordered_eligible_mod_names, weights=ordered_eligible_mod_weights, k=1)[0]
            selected_mods.append(selected_mod)
            ordered_eligible_mod_weights[ordered_eligible_mod_names.index(
                selected_mod)] = 0

        # for each selected mod, decide mod roll
        rolled_mods = []
        for mod_name in selected_mods:
            rolled_mod = roll_mod(item_mods[mod_name],
                                  item_level, instability, base_type)
            # TODO prevent zero value mods from being appended here
            rolled_mods.append(rolled_mod)

        return rolled_mods

    def decide_mod_amount(item_level):
        # TODO accept base type as argument - some base types should have less mods
        # minimum mod amount 1 - max 5, but very rare.
        return random.choices([1, 2, 3, 4, 5], weights=[80, 60 + item_level, 20 + item_level, 3 + item_level, 0 + item_level])[0]

    # select is unique item?
    # select special mod template? Maybe give special items generated red background

    base_type = select_base_type()
    item_name = random.choice(
        base_type["names"]) if "names" in base_type else "Item"

    mod_amount = decide_mod_amount(item_level)

    selected_item_mods = generate_mods(base_type, mod_amount)

    # print(itemName)
    # print(itemMods)
    return {"item_name": item_name, "item_mods": selected_item_mods}
    # returned itemMods should be associated with player mods file


print(generate_item(item_level=25, instability=20))
