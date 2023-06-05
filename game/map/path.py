from math import sqrt, pow


def distance(a, b):
    return sqrt(pow(a.pos[0]-b.pos[0], 2)+pow(a.pos[0]-b.pos[1], 2))

def h_score(start, end):
    dist = end.pos[0] - start.pos[0], end.pos[1] - start.pos[1]
    diag_steps = min(abs(dist[0]), abs(dist[1]))
    straight_steps = abs(dist[0]) + abs(dist[1]) - 2 * diag_steps
    return diag_steps * sqrt(2) + straight_steps

def lowest_f_score(open_set):
    final = None
    for tile in open_set:
        if not final or tile.f_score < final.f_score:
            final = tile
    return final

def reconstruct_path(grid, came_from, current):
    path = [current]
    current_key = current.pos[0], current.pos[1]
    while current_key in came_from:
        current = came_from[current_key]
        current_key = current.pos[0], current.pos[1]
        path.insert(0, current)
    return path

def a_star(grid, start, end):
    print(start.pos, end.pos)
    open_set = []
    closed_set = []
    came_from = {}
    start.g_score = 0
    start.f_Score = h_score(start, end)
    open_set.append(start)
    while len(open_set) > 0:
        current = lowest_f_score(open_set)
        open_set.remove(current)
        closed_set.append(current)
        if current == end:
            print("found path yay!, reconstructing")
            return reconstruct_path(grid, came_from, current)
        for neighbor in current.neighbors:
            if neighbor in closed_set or neighbor.solid:
                continue

            if grid[neighbor.pos[0], current.pos[1]].solid and grid[current.pos[0], neighbor.pos[1]].solid:
                continue

            tent_g_score = current.g_score + distance(current, neighbor)
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tent_g_score > neighbor.g_score:
                continue

            came_from[neighbor.pos[0], neighbor.pos[1]] = current
            neighbor.g_score = tent_g_score
            neighbor.f_score = neighbor.g_score + h_score(neighbor, end)
