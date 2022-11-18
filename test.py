from game.stats.stats import add_item_mods

print(add_item_mods([
    {"modName": "flat_to_max_hp", "value": 140,
        "source": "item", "source_item_ID": 5},
    {"modName": "flat_to_max_hp", "value": 120,
        "source": "item", "source_item_ID": 6}]))
