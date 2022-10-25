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
        
    def update(self, task):
        self.textmenu.interact()
        if self.alive:
            return task.cont
        else:
            return task.finish
