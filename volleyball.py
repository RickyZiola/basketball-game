import keyboard
import os
import time
import random
def clear():
	if(os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")

class Player:
	def __init__(self, control, startpos = [40, -24]):
		self.control = control
		self.pos = startpos
		self.vel = [0, 0]
		self.char = chr(165)
	def xpos(self):
		return self.pos[0]
	def ypos(self):
		return self.pos[1]
	def xvel(self):
		return self.vel[0]
	def yvel(self):
		return self.vel[1]

	def update(self, dt):
		self.vel[1] -= .1 * (dt / .05)	
		control = False
		grounded = False
		if(self.pos[0] < 0):
			self.pos[0] = 0
			self.vel[0] = .5
		if(self.pos[0] > 100):
			self.pos[0] = 100
			self.vel[0] = -.5
		if(self.pos[1] <= -24):
			grounded = True
			self.pos[1] = -24
			self.vel[1] = 0
		if(keyboard.is_pressed(self.control[1]) and grounded):
			self.vel[1] = 1
		if(keyboard.is_pressed(self.control[0])):
			control = True
			self.vel[0] -= .1 * (dt / .1)
		if(keyboard.is_pressed(self.control[2])):
			control = True
			self.vel[0] += .1 * (dt / .1)
		if(not control):
			self.vel[0] /= 2 * (dt / .1)
		if(self.pos[0] > 49 and self.pos[0] < 51):
			self.pos[0] -= self.vel[0] * 2
			self.vel[0] = 0
		if(self.vel[0] > 1):
			self.vel[0] = 1
		if(self.vel[0] < -1):
			self.vel[0] = -1
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
score = [0, 0]
class Ball:
	def __init__(self):
		self.pos = [50, -10]
		self.vel = random.choice([[1, 0], [-1, 0]])
		self.char = "o"
	def xpos(self):
		return self.pos[0]
	def ypos(self):
		return self.pos[1]
	def xvel(self):
		return self.vel[0]
	def yvel(self):
		return self.vel[1]
	def update(self, dt):
		self.vel[1] -= .1 * (dt / .05)
		if(self.pos[1] > 1):
			self.pos[1] = 1
			self.vel[0] = 0
			self.vel[1] = -self.vel[1]
		if(self.pos[0] < 0):
			score[1] += 1
			self.__init__()
		if(self.pos[0] > 100):
			score[0] += 1
			self.__init__()
		if(self.pos[1] <= -24):
			if(self.pos[0] > 50):
				score[0] += 1
			else:
				score[1] += 1
			self.__init__()
		if(((self.pos[0] - player1.pos[0]) ** 2 + (self.pos[1] - player1.pos[1]) ** 2) ** 0.5 < 2):
			self.vel[0] = -self.vel[0]
			self.vel[1] = -self.vel[1]
			self.vel[0] += player1.vel[0]
			self.vel[1] += player1.vel[1]
		if(((self.pos[0] - player2.pos[0]) ** 2 + (self.pos[1] - player2.pos[1]) ** 2) ** 0.5 < 2):
			self.vel[0] = -self.vel[0]
			self.vel[1] = -self.vel[1]
			self.vel[0] += player2.vel[0]
			self.vel[1] += player2.vel[1]
		self.pos[0] += self.vel[0] * (dt / .1)
		self.pos[1] += self.vel[1] * (dt / .1)
	
class Border:
	def __init__(self, pos):
		self.pos = pos
		self.char = "|"
	def xpos(self):
		return self.pos[0]
	def ypos(self):
		return self.pos[1]

	def __str__(self):
		return f"Border({str(self.pos)})"
scene = [Border((50, y)) for y in range(-25, -20)]
player1 = Player(("a", "w", "d"))
player2 = Player(("left_arrow", "up_arrow", "right_arrow"), [60, -24])
ball = Ball()
scene.append(player1)
scene.append(player2)
scene.append(ball)
prnt_stdout = print
reg = ""
def print(text="", end="\n"):
	global reg
	reg += str(text) + str(end)
def update_stdout():
	global reg
	prnt_stdout(reg)
	reg = ""
def draw(scene, size):
	clear()
	for y in range(15):
		print()
	for x in range(50):
		print(" ", end="")
	for x in range(size[0]+2):
		print("-", end="")
	print()
	for y in range(size[1]):
		for x in range(50):
			print(" ", end="")
		print("|", end="")
		for x in range(size[0]):
			obj = False
			for o in scene:
				if(int(o.xpos()) == x and int(-o.ypos()) == y):
					print(o.char, end="")
					obj = True
			if(not obj):
				print(" ", end="")
		print("|")
	for x in range(50):
		print(" ", end="")
	for x in range(size[0] + 2):
		print("-", end="")
	print()
	for x in range(47 + int(size[0] / 2)):
		print(" ", end="")
	print(score[0], end="")
	for x in range(5):
		print(" ", end="")
	print(score[1])
	update_stdout()
while 1:
	t0 = time.time()
	draw(scene, (100, 25))
	update_stdout()
	time.sleep(0.05)
	dt = time.time() - t0
	player1.update(dt)
	player2.update(dt)
	ball.update(dt)
