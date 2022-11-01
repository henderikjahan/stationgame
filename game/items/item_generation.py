# TODO deal with negative mod values - need special descriptions for those
# Maybe prevent only negative mods spawning on an item

import random
from math import floor
from itemBasesData import baseTypes
from modData import itemMods


def generateItem(
    itemLevel: int = 0,
    inStability: int = 0,
):
    def selectBaseType():
        eligibleBaseTypes = {k: v for (k, v) in baseTypes.items() if (
            ("minimumItemLvl" not in v or v["minimumItemLvl"] <= itemLevel)
            and ("minimumInstabilityLvl" not in v or v["minimumInstabilityLvl"] <= inStability)
        )}
        orderedEligibleBaseTypesNames = list(eligibleBaseTypes)
        orderedEligibleBaseTypesWeights = [baseTypes[x]["baseWeight"]
                                           for x in orderedEligibleBaseTypesNames]
        selectedBaseType = random.choices(
            orderedEligibleBaseTypesNames, weights=orderedEligibleBaseTypesWeights, k=1)[0]

        return baseTypes[selectedBaseType]

    def rollMod(
        mod: any,
        itemLevel: int,
        instability: int,
        baseType: any,
    ):
        if "instabilityMultiplier" in baseType:
            instability = instability * baseType["instabilityMultiplier"]

        range = mod["baseRange"] + \
            (mod["baseRangeInstablityScaling"] * instability)
        lowpoint = mod["midPoint"] - range
        highpoint = mod["midPoint"] + range + \
            (mod["highPointItemLevelScaling"] * itemLevel)

        modRoll = floor(random.uniform(lowpoint, highpoint))
        for magnitudeModifierTag in mod["baseTagMagnitudeModifiers"]:
            if magnitudeModifierTag in baseType["baseTags"]:
                modRoll = modRoll * \
                    mod["baseTagMagnitudeModifiers"][magnitudeModifierTag]

        if "modMultiplier" in baseType:
            modRoll = modRoll * baseType["modMultiplier"]

        modText = mod["description"].replace("$$", str(int(modRoll)))

        return modText

    def generateMods(
        baseType: any,
        modAmount: int
    ):
        eligibleMods = {k: v for (k, v) in itemMods.items() if (
            ("minimumItemLvl" not in v or v["minimumItemLvl"] <= itemLevel)
            and ("minimumInstabilityLvl" not in v or v["minimumInstabilityLvl"] <= inStability)
        )}
        orderedEligibleModNames = list(eligibleMods)
        orderedEligibleModWeights = []

        baseTags = baseType["baseTags"]
        for modName in orderedEligibleModNames:
            itemMod = itemMods[modName]
            modWeight = itemMod["modWeight"]

            if "baseTagWeigthModifiers" in itemMod:
                for baseTag in baseTags:
                    if baseTag in itemMod["baseTagWeigthModifiers"]:
                        amountToModifyTag = itemMod["baseTagWeigthModifiers"][baseTag]
                        modWeight = modWeight * amountToModifyTag
            orderedEligibleModWeights.append(modWeight)

        selectedMods = []

        while (len(selectedMods) < modAmount):
            # check if no mods are left over, if so, exit while loop
            if (max(orderedEligibleModWeights) == 0):
                break

            # select a mod, append it and set its weight to zero
            selectedMod = random.choices(
                orderedEligibleModNames, weights=orderedEligibleModWeights, k=1)[0]
            selectedMods.append(selectedMod)
            orderedEligibleModWeights[orderedEligibleModNames.index(
                selectedMod)] = 0

        # for each selected mod, decide mod roll
        rolledMods = []
        for modName in selectedMods:
            rolledMod = rollMod(itemMods[modName],
                                itemLevel, inStability, baseType)
            # TODO prevent zero value mods from being appended here
            rolledMods.append(rolledMod)

        return rolledMods

    def decideModAmount(itemLevel):
        # TODO accept base type as argument - some base types should have less mods
        # minimum mod amount 1 - max 5, but very rare.
        return random.choices([1, 2, 3, 4, 5], weights=[80, 60 + itemLevel, 20 + itemLevel, 3 + itemLevel, 0 + itemLevel])[0]

    # select is unique item?
    # select special mod template? Maybe give special items generated red background

    baseType = selectBaseType()
    itemName = random.choice(
        baseType["names"]) if "names" in baseType else "Item"

    modAmount = decideModAmount(itemLevel)

    selectedItemMods = generateMods(baseType, modAmount)

    # print(itemName)
    # print(itemMods)
    return {"itemName": itemName, "itemMods": selectedItemMods}
    # returned itemMods should be associated with player mods file


print(generateItem(itemLevel=25, inStability=20))
