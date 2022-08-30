from panda3d.core import Vec2


def load_as_dict(filename):
    child_dict = {}
    models = loader.load_model(filename)
    for child in models.get_children():
        child.clear_transform()
        child.detach_node()
        child.set_render_mode_thickness(2)
        child_dict[child.name] = child
    return child_dict

def clamp(mini, maxi, n):
    return max(mini, min(n, maxi))

def multvec2(a, b):
    n = Vec2()
    for index, value in enumerate(a):
        n[index] = a[index]*b[index]
    return n

def evenvec2(a, n=2):
    for index, value in enumerate(a):
        if value%2 == 1:
            a[index] = value-1
    return a

def is_in(x, y, size):
    if x <= size and x >= 0 and y <= size and y >= 0:
        return True

def rotate_mat3(sub):
    return list(zip(*sub[::-1]))
