# from game.items.item_generation import generate_item

from game.stats.stats import calculate_current_stats, remove_item_mods

print(calculate_current_stats())

remove_item_mods(3)
