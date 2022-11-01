# TODO deal with negative mod values - need special descriptions for those
# Maybe prevent only negative mods spawning on an item

import random
from math import floor
from itemBasesData import base_types
from modData import item_mods


def generate_item(
    item_level: int = 0,
    instability: int = 0,
):
    def selectBaseType():
        eligible_base_types = {k: v for (k, v) in base_types.items() if (
            ("minimumItemLvl" not in v or v["minimumItemLvl"] <= item_level)
            and ("minimumInstabilityLvl" not in v or v["minimumInstabilityLvl"] <= instability)
        )}
        ordered_eligible_base_types_names = list(eligible_base_types)
        ordered_eligible_base_types_weights = [base_types[x]["baseWeight"]
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

    def generateMods(
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

        baseTags = base_type["baseTags"]
        for modName in ordered_eligible_mod_names:
            itemMod = item_mods[modName]
            modWeight = itemMod["modWeight"]

            if "base_tag_weigth_modifiers" in itemMod:
                for baseTag in baseTags:
                    if baseTag in itemMod["base_tag_weigth_modifiers"]:
                        amountToModifyTag = itemMod["base_tag_weigth_modifiers"][baseTag]
                        modWeight = modWeight * amountToModifyTag
            ordered_eligible_mod_weights.append(modWeight)

        selectedMods = []

        while (len(selectedMods) < mod_amount):
            # check if no mods are left over, if so, exit while loop
            if (max(ordered_eligible_mod_weights) == 0):
                break

            # select a mod, append it and set its weight to zero
            selectedMod = random.choices(
                ordered_eligible_mod_names, weights=ordered_eligible_mod_weights, k=1)[0]
            selectedMods.append(selectedMod)
            ordered_eligible_mod_weights[ordered_eligible_mod_names.index(
                selectedMod)] = 0

        # for each selected mod, decide mod roll
        rolledMods = []
        for modName in selectedMods:
            rolledMod = roll_mod(item_mods[modName],
                                 item_level, instability, base_type)
            # TODO prevent zero value mods from being appended here
            rolledMods.append(rolledMod)

        return rolledMods

    def decideModAmount(item_level):
        # TODO accept base type as argument - some base types should have less mods
        # minimum mod amount 1 - max 5, but very rare.
        return random.choices([1, 2, 3, 4, 5], weights=[80, 60 + item_level, 20 + item_level, 3 + item_level, 0 + item_level])[0]

    # select is unique item?
    # select special mod template? Maybe give special items generated red background

    baseType = selectBaseType()
    itemName = random.choice(
        baseType["names"]) if "names" in baseType else "Item"

    modAmount = decideModAmount(item_level)

    selectedItemMods = generateMods(baseType, modAmount)

    # print(itemName)
    # print(itemMods)
    return {"itemName": itemName, "itemMods": selectedItemMods}
    # returned itemMods should be associated with player mods file


print(generate_item(item_level=25, instability=20))
