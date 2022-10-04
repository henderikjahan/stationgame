from panda3d.core import NodePath, CardMaker
from panda3d.core import TextNode, TextProperties, TextPropertiesManager
from game.gui.menus import TextMenu


class ItemGui:
    def __init__(self):
        self.root = aspect2d.attach_new_node("Item Gui")
        aug = draw_box(0.8, -0.2, -1, -0.1, loader.load_texture("assets/images/augtest.png"))
        aug.reparent_to(self.root)
        aug.set_transparency(True)

        self.textmenu = TextMenu([
            MenuItem("Shoe", "A very beautiful shoe"),
            MenuItem("Cigarette", "A very beautiful cigarette"),
            MenuItem("Sleeping bag", "A very beautiful sleeping bag"),
            MenuItem("Coin", "A very beautiful coin"),
        ], y=0.8)
        self.textmenu.root.reparent_to(self.root)
        base.task_mgr.add(self.update)

    def update(self, task):
        context = base.device_listener.read_context("menu")
        if context["up"]:
            self.textmenu.move_selection(-1)
        if context["down"]:
            self.textmenu.move_selection(1)
        return task.cont