# TODO move data and functions to separate file - gotta figure out relative importing
# TODO deal with negative mod values - need special descriptions for those

import random
from math import floor

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
        "baseTags": ["weapon", "psi"],
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
        "baseTags": ["weapon", "psi"],
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
        "baseTags": ["weapon", "psi"],
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
        "baseTags": ["weapon", "assault"],
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
        "baseTags": ["weapon", "assault"],
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
        "baseTags": ["weapon", "assault"],
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
        "instabilityMultiplier": 1.3,
        "baseTags": ["weapon", "tactics"],
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
        "instabilityMultiplier": 1.4,
        "baseTags": ["weapon", "assault"],
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
        "instabilityMultiplier": 1.5,
        "baseTags": ["weapon", "psi"],
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
        "baseTags": ["armor", "boots"],
    },
}

baseTypes = weaponBases | bootsBases

# baseRange is allowed mod values around the range beween midPoint and highPoint
# by default, highpoint is the same as midPoint
itemMods = {
    "flatMaxHP": {
        "description": "$$ to maximum HP",
        "modWeight": 20,
        "minimumItemLvl": 0,
        "midPoint": 10,
        "highPointItemLevelScaling": 3,
        "baseRange": 5,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {},
        "baseTagWeigthModifiers": {"weapon": 0}
    },
    "increasedMaxHP": {
        "description": "$$% increased maximum HP",
        "modWeight": 10,
        "minimumItemLvl": 10,
        "midPoint": 3,
        "highPointItemLevelScaling": 0.2,
        "baseRange": 2,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {},
        "baseTagWeigthModifiers": {"weapon": 0}
    },
    "flatRegenHP": {
        "description": "$$ HP restored per step",
        "modWeight": 10,
        "minimumItemLvl": 0,
        "midPoint": 2,
        "highPointItemLevelScaling": 0.4,
        "baseRange": 1,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {},
        "baseTagWeigthModifiers": {"weapon": 0}
    },
    "increasedHPRegen": {
        "description": "$$% increased HP restored per step",
        "modWeight": 5,
        "minimumItemLvl": 20,
        "midPoint": 15,
        "highPointItemLevelScaling": 1,
        "baseRange": 10,
        "baseRangeInstablityScaling": 1,
        "baseTagMagnitudeModifiers": {},
        "baseTagWeigthModifiers": {"weapon": 0}
    },
    "increasedGenericDamage": {
        "description": "Deal $$% increased damage",
        "modWeight": 5,
        "minimumItemLvl": 0,
        "midPoint": 5,
        "highPointItemLevelScaling": 1,
        "baseRange": 3,
        "baseRangeInstablityScaling": 0.4,
        "baseTagMagnitudeModifiers": {"weapon": 2},
        "baseTagWeigthModifiers": {}
    },
    "APRegen": {
        "description": "Restore $$ more Action Points each turn in combat",
        "modWeight": 1,
        "minimumItemLvl": 10,
        "midPoint": 1,
        "highPointItemLevelScaling": 0.03,
        "baseRange": 0.01,
        "baseRangeInstablityScaling": 0.02,
        "baseTagMagnitudeModifiers": {"weapon": 2},
        "baseTagWeigthModifiers": {},
        "maximumValue": 2
    },
    "flatToAP": {
        "description": "+$$ maximum Action Points in combat",
        "modWeight": 2,
        "minimumItemLvl": 10,
        "midPoint": 1,
        "highPointItemLevelScaling": 0.05,
        "baseRange": 0.01,
        "baseRangeInstablityScaling": 0.02,
        "baseTagMagnitudeModifiers": {"weapon": 2},
        "baseTagWeigthModifiers": {},
        "maximumValue": 2
    },
    "flatToAssault": {
        "description": "+$$ to Assault Skill",
        "modWeight": 5,
        "minimumItemLvl": 0,
        "midPoint": 2,
        "highPointItemLevelScaling": 0.5,
        "baseRange": 1,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {"assault": 2, "psi": 0.5, "tactics": 0.5},
        "baseTagWeigthModifiers": {"assault": 2, "psi": 0.2, "tactics": 0.2},
    },
    "flatToPSI": {
        "description": "+$$ to PSI Skill",
        "modWeight": 5,
        "minimumItemLvl": 0,
        "midPoint": 2,
        "highPointItemLevelScaling": 0.5,
        "baseRange": 1,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {"assault": 0.5, "psi": 2, "tactics": 0.5},
        "baseTagWeigthModifiers": {"assault": 0.2, "psi": 2, "tactics": 0.2},
    },
    "flatToTactics": {
        "description": "+$$ to Tactics Skill",
        "modWeight": 5,
        "minimumItemLvl": 0,
        "midPoint": 2,
        "highPointItemLevelScaling": 0.5,
        "baseRange": 1,
        "baseRangeInstablityScaling": 0.2,
        "baseTagMagnitudeModifiers": {"assault": 0.5, "psi": 0.5, "tactics": 2},
        "baseTagWeigthModifiers": {"assault": 0.2, "psi": 0.2, "tactics": 2},
    }
}

# TODO turn these loose functions into one big function/class


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


def rollMod(
    mod: any,
    itemLevel: int,
    instability: int,
    baseType,
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
    itemLevel: int,
    inStability: int,
    baseType,
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
        rolledMods.append(rolledMod)

    return rolledMods


def decideModAmount(itemLevel):
    # TODO accept base type as argument - some base types should have less mods
    # minimum mod amount 1 - max 5, but very rare.
    return random.choices([1, 2, 3, 4, 5], weights=[80, 60 + itemLevel, 20 + itemLevel, 3 + itemLevel, 0 + itemLevel])[0]


def generateItem(
    itemLevel: int = 0,
    inStability: int = 0,
):
    # select is unique item?
    # select special mod template? Maybe give special items generated red background

    baseType = selectBaseType(itemLevel, inStability)
    itemName = random.choice(
        baseType["names"]) if "names" in baseType else "Item"

    modAmount = decideModAmount(itemLevel)

    itemMods = generateMods(itemLevel, inStability, baseType, modAmount)

    print(itemName)
    print(itemMods)

    # generate mod text and data to pass. Needs specifics of how to share data
    # {itemName: "", "itemText": "", itemMods: {}}


generateItem(itemLevel=5, inStability=25)
