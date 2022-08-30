try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
			

class Battler:
	def __init__(self):
		self.hp = 10
		self.attack = 5

	def attack(self, who):
		who.hp -= self.attack
		

player = Battler()
enemy = Battler()
print("A monster appears")
while True:
	print("(a)ttack / (d)efend / (p)si / (i)tem")
	key = getch()
	if key == "a":
		print("You attack")
		player.attack(enemy)
	elif key == "d":
		print("You defend")
	elif key == "p":
		print("You psi")
	elif key == "i":
		print("You use an item")
	else:
		print("invalid input")
		continue
	
	print("enemy does a thing")