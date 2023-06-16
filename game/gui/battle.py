from game.gui.menus import TextScroller, TextMenu, MenuItem


class BattleGui:
    def __init__(self, player, enemies):
        self.root = aspect2d.attach_new_node("Battle Gui")
        self.battle = BattleGameplay(player_gl=player, enemies_data=enemies)
        self.describe = TextScroller(-1,-0.5, 28, 5)
        self.describe.set_text("\nBattle begins!")
        self.describe.root.reparent_to(self.root)
        self.buffer = base.printer.buffer = []

        # Abstract this.
        base.cardmaker.set_frame(-0.5,0.5,-0.5,0.5)
        self.enemy = self.root.attach_new_node(base.cardmaker.generate())
        texture = loader.load_texture("assets/images/enemies/boze_smurf.png")
        texture.set_minfilter(0); texture.set_magfilter(0)
        self.enemy.set_texture(texture)
        self.enemy.set_transparency(True)
        self.enemy.set_scale(1.5,1.5,1.5)


        self.main_menu = TextMenu([
            MenuItem(
                "Attack", "Attack enemy.", 
                function=[self.attack_menu]
            ),
            MenuItem(
                "Psi", "Use psi ability.",
                function=[self.attack_menu]
            ),
            MenuItem(
                "TurnPass", "Use psi ability.",
                function=[self.attack_menu]
            ),
            MenuItem(
                "Item", "Use an item.",
                function=[self.attack_menu]
            ),
        ], x=0.5, y=0.8)

        self.menu = self.main_menu
        self.menu.root.reparent_to(self.root)

    def send_command(self, command):
        self.battle.battle_turn(command)
        self.switch_to(self.main_menu)

    def attack_menu(self):
        # read enemies and see who's alive
        self.attack_menu = TextMenu([
            MenuItem(
                "Magical mayonaise", 
                "A very magical mayonaise, oh no!",
                function=[self.send_command, "attack magical mayonaise"]
            ),
            MenuItem(
                "Attack borger burger", 
                "A furious borger borger, aaaaah!",
                function=[self.send_command, "attack borger burger"]
            ),
            MenuItem(
                "cancel", 
                "don't attack", 
                function=[self.switch_to, self.main_menu],
            ),
        ], x=0.5, y=0.8)
        self.menu.root.detach_node()
        self.menu = self.attack_menu
        self.menu.root.reparent_to(self.root)


    def switch_to(self, menu):
        self.menu.root.detach_node()
        self.menu = menu
        self.menu.root.reparent_to(self.root)

    def update(self):
        while len(self.buffer) > 0:            
            self.describe.add_text(self.buffer.pop(0)+"\n")
            self.describe.done = False

        if not self.describe.done:
            self.describe.update()
        else:
            self.menu.interact()
            if not self.menu.alive:
                return True