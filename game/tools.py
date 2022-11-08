import builtins
from panda3d.core import Vec2, Vec3
from panda3d.core import NodePath
from panda3d.core import CardMaker


def print(string):
    try:
        base.print(string)
    except NameError:
        builtins.print(string)

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

def roundvec(vec):
    rounded = Vec3()
    for v, value in enumerate(vec):
        rounded[v] = int(value)
    return rounded

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

def tile_texture(nodepath, texture, x, y, tiles_per_row):
    y = y+1 # Innocent hack. Something is off about this math.
    texture.set_minfilter(0)
    texture.set_magfilter(0)
    for texture_stage in nodepath.find_all_texture_stages():
        nodepath.set_texture(texture_stage, texture, 1)
        w = h = 1/tiles_per_row
        nodepath.set_tex_scale(texture_stage, w, h)
        nodepath.set_tex_offset(texture_stage, x*w, 1-(y*w))

def tile_animation(nodepath, texture, frames=[(0,0), (1,0)], tiles_per_row=8, framerate=24):
    sequenced = NodePath(nodepath.name)
    sequence = SequenceNode(nodepath.name)
    sequences.attach_new_node(sequence)
    for frame in frames:
        new = nodepath.copy_to(sequenced)
        tile_texture(new, texture, frame[0], frame[1], tiles_per_row)
        sequence.add_child(new.node()) # WARNING: this might not copy the texture offset
    sequence.set_frame_rate(framerate)
    sequence.loop(True)
    return sequenced

def flatten_sequence(sequences_nodepath):
    sequences =  sequences_nodepath.get_children()
    flattened_sequence = SequenceNode(sequence[0].name)
    for a, animation in enumerate(sequence[0].node().get_children()):
        for f, frame in enumerate(animation.get_child(0).get_children()):
            combined_frame = NodePath("frame " + str(f))
            for sequence in sequences:
                new_np = NodePath("frame")
                new_np.set_pos(sequence.get_pos())
                animation = sequence.node().get_child(a).get_child(0)
                new_np.attach_new_node(animation.get_child(f))
                new_np.reparent_to(combined_frame)
            combined_frame.flattenStrong()
            flattened_sequence.add_child(combined_frame.node())
    framerate = animation.get_frame_rate()
    flattened_sequence.set_frame_rate(framerate)
    flattened_sequence.loop(True)
    return NodePath(flattened_sequence)

def render_to_texture(root):
    # Render to texture
    cardmaker = CardMaker("card")
    cardmaker.set_frame(-1,1,-1,1)
    screen = base.render2d.attach_new_node(cardmaker.generate())
    buffer = base.win.makeTextureBuffer("Buffer", 256, 256)
    buffer.set_clear_color_active(True)
    buffer.set_clear_color((0,0,0,1))
    texture = buffer.get_texture()
    texture.set_minfilter(0)
    texture.set_magfilter(0)
    screen.set_texture(texture, 1)
    buffer.set_sort(-100)
    camera = base.make_camera(buffer)
    camera.reparent_to(root)
    return camera










