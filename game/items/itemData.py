weaponBases = {
    "rickety PSI glove": {
        "minimumItemLvl": 0,
        "baseWeight": 1,
        "name": "Power Glove",
        "attackCategory": "psi",
        "implicitMods": {}
    },
    "powerGlove": {
        "minimumItemLvl": 10,
        "baseWeight": 2,
        "name": "Power Glove",
        "attackCategory": "psi",
        "implicitMods": {}
    },
    "psiManipulator": {
        "minimumItemLvl": 20,
        "baseWeight": 2,
        "name": "PSI Manipulator",
        "attackCategory": "psi",
        "implicitMods": {}
    },

    "rustyShank": {
        "minimumItemLvl": 0,
        "baseWeight": 1,
        "name": "Rusty Shank",
        "attackCategory": "assault",
        "implicitMods": {}
    },
    "stunBaton": {
        "minimumItemLvl": 10,
        "baseWeight": 2,
        "name": "Stun Baton",
        "attackCategory": "assault",
        "implicitMods": {}
    },
    "plasmaPoker": {
        "minimumItemLvl": 20,
        "baseWeight": 2,
        "name": "Plasma Poker",
        "attackCategory": "assault",
        "implicitMods": {}
    }
}

bootsBases = {}

baseTypes = weaponBases | bootsBases

print(baseTypes)

itemMods = {
    "flatmaxHP": {
        "modWeight": 30,
        "minimumItemLvl": 0,
        "midPoint": 10,
        "midPointItemLevelScaling": 0.5,
        "baseRange": 5,
        "baseRangeInstablityScaling": 0.2
    },
    "flatRegenHP": {
        "modWeight": 30,
        "minimumItemLvl": 0,
        "midPoint": 10,
        "midPointItemLevelScaling": 0.5,
        "baseRange": 5,
        "baseRangeInstablityScaling": 0.2
    }
}
