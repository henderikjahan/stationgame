from typing import Union
import random

weaponBases = {
    "tier1PSIWeapon": {
        "baseName": "tier1PSIWeapon",
        "minimumItemLvl": 0,
        "minimumInstabilityLvl": 0,
        "baseWeight": 1,
        "names": ["Rickety PSI glove", "Rusted PSI glove"],
        "attackCategory": "psi",
        "implicitMods": [],
        "images": [],
    },
    "tier2PSIWeapon": {
        "baseName": "tier2PSIWeapon",
        "minimumItemLvl": 10,
        "minimumInstabilityLvl": 0,
        "baseWeight": 2,
        "names": ["Power Glove", "PSI glove"],
        "attackCategory": "psi",
        "implicitMods": [],
        "images": [],
    },
    "tier3PSIWeapon": {
        "baseName": "tier3PSIWeapon",
        "minimumItemLvl": 20,
        "minimumInstabilityLvl": 0,
        "baseWeight": 2,
        "names": ["PSI Manipulator"],
        "attackCategory": "psi",
        "implicitMods": [],
        "images": [],
    },

    "tier1AssaultWeapon": {
        "baseName": "tier1AssaultWeapon",
        "minimumItemLvl": 0,
        "minimumInstabilityLvl": 0,
        "baseWeight": 1,
        "names": ["Rusty Shank", "Baseball Bat", "Broken Baton"],
        "attackCategory": "assault",
        "implicitMods": [],
        "images": [],
    },
    "tier2AssaultWeapon": {
        "baseName": "tier2AssaultWeapon",
        "minimumItemLvl": 10,
        "minimumInstabilityLvl": 0,
        "baseWeight": 2,
        "names": ["Stun Baton"],
        "attackCategory": "assault",
        "implicitMods": [],
        "images": [],
    },
    "tier3AssaultWeapon": {
        "baseName": "tier3AssaultWeapon",
        "minimumItemLvl": 20,
        "minimumInstabilityLvl": 0,
        "baseWeight": 2,
        "names": ["Plasma Poker"],
        "attackCategory": "assault",
        "implicitMods": [],
        "images": [],
    },

    "tier1InsanityWeapon": {
        "baseName": "tier1InsanityWeapon",
        "minimumItemLvl": 0,
        "minimumInstabilityLvl": 10,
        "baseWeight": 1,
        "names": ["Dart Gun"],
        "attackCategory": "tactics",
        "implicitMods": [],
        "images": [],
        "modMultiplier": 1.2,
        "insanityMultiplier": 1.3,
    },
    "tier2InsanityWeapon": {
        "baseName": "tier2InsanityWeapon",
        "minimumItemLvl": 10,
        "minimumInstabilityLvl": 20,
        "baseWeight": 1,
        "names": ["Rubber Chicken"],
        "attackCategory": "assault",
        "implicitMods": [],
        "images": [],
        "modMultiplier": 1.4,
        "insanityMultiplier": 1.4,
    },
    "tier3InsanityWeapon": {
        "baseName": "tier3InsanityWeapon",
        "minimumItemLvl": 10,
        "minimumInstabilityLvl": 30,
        "baseWeight": 2,
        "names": ["Mysterious Orb"],
        "attackCategory": "psi",
        "implicitMods": [],
        "images": [],
        "modMultiplier": 1.5,
        "insanityMultiplier": 1.5,
    },
}

bootsBases = {
    "tier1Boots": {
        "baseName": "tier1Boots",
        "minimumItemLvl": 0,
        "minimumInstabilityLvl": 0,
        "baseWeight": 1,
        "names": ["Leather Boots"],
        "implicitMods": [],
        "images": [],
    },
}

baseTypes = weaponBases | bootsBases

# print(baseTypes)

itemMods = {
    "flatMaxHP": {
        "description": "$$ to maximum HP",
        "modWeight": 30,
        "minimumItemLvl": 0,
        "midPoint": 10,
        "midPointItemLevelScaling": 3,
        "baseRange": 5,
        "baseRangeInstablityScaling": 0.2
    },
    "increasedMaxHP": {
        "description": "$$% increased maximum HP",
        "modWeight": 10,
        "minimumItemLvl": 10,
        "midPoint": 3,
        "midPointItemLevelScaling": 0.2,
        "baseRange": 2,
        "baseRangeInstablityScaling": 0.2
    },
    "flatRegenHP": {
        "description": "$$ HP restored per step",
        "modWeight": 10,
        "minimumItemLvl": 0,
        "midPoint": 2,
        "midPointItemLevelScaling": 0.4,
        "baseRange": 1,
        "baseRangeInstablityScaling": 0.2
    },
    "increasedHPRegen": {
        "description": "$$% increased HP restored per step",
        "modWeight": 5,
        "minimumItemLvl": 20,
        "midPoint": 15,
        "midPointItemLevelScaling": 1,
        "baseRange": 10,
        "baseRangeInstablityScaling": 1
    },
    "increasedGenericDamage": {
        "description": "Deal $$% increased damage",
        "modWeight": 5,
        "minimumItemLvl": 0,
        "midPoint": 5,
        "midPointItemLevelScaling": 1,
        "baseRange": 3,
        "baseRangeInstablityScaling": 0.4
    },
}


def selectBaseType(
    itemLevel: int,
    inStability: int
):
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


def selectMods(
    itemLevel: int,
    inStability: int,
    modAmount: int
):
    eligibleMods = {k: v for (k, v) in itemMods.items() if (
        ("minimumItemLvl" not in v or v["minimumItemLvl"] <= itemLevel)
        and ("minimumInstabilityLvl" not in v or v["minimumInstabilityLvl"] <= inStability)
    )}
    orderedEligibleModNames = list(eligibleMods)
    orderedEligibleModWeights = [itemMods[x]["modWeight"]
                                 for x in orderedEligibleModNames]
    # selectedBaseType = random.choices(
    #     orderedEligibleModNames, weights=orderedEligibleModWeights, k=1)[0]

    # Select mod from eligiblemodNames using choices() in while loop. Then remove the mods
    # from eligible mod name and weight lists. Add to selectedmods and continue until amount of selected mods is reached

    selectedMods = []

    # prune zero and below zero mod rolls from list.

    return selectedMods


def decideModAmount(itemLevel):
    # TODO accept base type as argument - some base types should have less mods
    # minimum mod amount 1 - max 5, but very rare.
    return random.choices([1, 2, 3, 4, 5], weights=[80, 60 + itemLevel, 20 + itemLevel, 3 + itemLevel, 0 + itemLevel])[0]


def generateItem(
    itemLevel: int,
    inStability: Union[int, bool] = False,
):
    # select is unique item?

    # select baseType

    baseType = selectBaseType(itemLevel, inStability if inStability else 0)
    itemName = random.choice(
        baseType["names"]) if "names" in baseType else "Item"

    modAmount = decideModAmount(itemLevel)
    print(modAmount)

    # select is special mod template? Maybe give special items generated red background

    # choose mods
    # choose mod roll
    print("generating item")


generateItem(itemLevel=5, inStability=15)
