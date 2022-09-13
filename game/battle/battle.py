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
		self.attack_stat = 5
		self.ap = 1
		

	def attack(self, who):
		who.hp -= self.attack_stat
		

player = Battler()
enemy = Battler()

print("A monster appears")
while True:
	print("(a)ttack / (d)efend / (p)si / (i)tem")
	key = getch()
	keyc = key.decode()	# character
	keyu = ord(key)	# unicode, escape = 27

	if keyc == "a":
		print("You attack")
		player.attack(enemy)
	elif keyc == "d":
		print("You defend")
	elif keyc == "p":
		print("You psi")
	elif keyc == "i":
		print("You use an item")
	elif keyu == 27:	# when you press escape
		print("script ended")
		break
	else:
		print("invalid input: " + str(keyc))
		continue
	
	print("enemy does a thing")


# notes for getch() (getch() returns bytecode)
# ord(): byte -> unicode
# chr(): unicode -> character (like a, x, r)
# .decode(): byte -> character