import math
import keyboard
import time
import os

def clear():
	if(os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")	

class Player:
	def __init__(self):
		self.xpos = 5
		self.ypos = -10
		self.xvel = 0
		self.yvel = 0
		self.has_ball = False
		self.grounded = False
		self.move = False
	def get_pos(self):
		return (self.xpos, self.ypos)
	def get_vel(self):
		return (self.xvel, self.yvel)
	def update(self, ball, dt):
		if(not self.grounded):
			self.yvel -= .2 * (dt / .1)
		if(self.grounded and not self.move):
			self.xvel /= 2
		if(self.ypos <= -25):
			self.yvel = 0
			self.grounded = True
			self.ypos = -24
		if(self.xpos >= 100):
			self.xvel = -1
		if(self.xpos <= 0):
			self.xvel = 1
		if(((self.xpos - ball.xpos) ** 2 + (self.ypos - ball.ypos) ** 2) ** 0.5 < 2):
			self.has_ball = True
			ball.xpos = self.xpos
			ball.ypos = self.ypos
			ball.xvel = self.xvel
			ball.yvel = self.yvel
		else:
			self.has_ball = False
		self.move = False
		self.xpos += self.xvel * (dt / .1)
		self.ypos += self.yvel * (dt / .1)
class Ball:
	def __init__(self):
		self.xpos = 5
		self.ypos = -20
		self.xvel = 0
		self.yvel = 0
		self.in_hoop = False
	def get_pos(self):
		return (self.xpos, self.ypos)
	def get_vel(self):
		return (self.xvel, self.yvel)
	def check_in_hoop(self, hoop_pos):
		hx, hy = hoop_pos
		if(((self.xpos - hx) ** 2 + (self.ypos - hy) ** 2) ** .5 < 3):
			return True
		return False
	def update(self, dt):
		self.yvel -= .2 * (dt / .1)
		if(self.ypos > 0):
			self.yvel = -self.yvel
			self.xvel = 0
		if(self.ypos > -1):
			self.ypos = -1
		if(self.xpos > 99):
			self.xvel = -self.xvel
		if(self.xpos < 0):
			self.xvel = -self.xvel
		if(self.ypos < -25):
			self.yvel = -self.yvel / 2
			self.xvel /= 1.5
			self.ypos = -24
		self.xpos += self.xvel * (dt / .1)
		self.ypos += self.yvel * (dt / .1)
ball = Ball()
player = Player()
score = 0
ball.xvel = .5
def draw_border(height, width, ball, player, hoop_pos):
	print("                                                  ", end="")
	for x in range(width + 2):
		print("-", end="")
	print()
	for y in range(height):
		print("                                                  |", end="")
		for x in range(width):
			if(int(player.xpos) == x and int(-player.ypos) == y):
				if(int(time.time()) % 2 == 0):
					print("Y", end="")
				else:
					print(chr(165), end="")
			elif(int(ball.xpos) == x and int(-ball.ypos) == y):
				print("o", end="")
			elif(hoop_pos[0]-1 == x and hoop_pos[1] == y):
				print("_", end="")
			else:
				print(" ", end="")
		print("|")
	print("                                                  ",end="")
	for x in range(width+2):
		print("-", end="")
	print()

def mainloop(dt):
	global score
	clear()
	if(ball.check_in_hoop((99, -20))):
		ball.__init__()
		player.has_ball = False
		#player.__init__()
		score += 1
	if(keyboard.is_pressed("space") and player.grounded):
		player.grounded = False
		player.yvel = 1.5
	if(keyboard.is_pressed("right_arrow")):
		player.xvel += .1
		player.move = True
	if(keyboard.is_pressed("left_arrow")):
		player.xvel -= .1
		player.move = True
	if(keyboard.is_pressed("up_arrow") and player.has_ball):
		ball.xpos += 2
		ball.ypos += 2
		ball.xvel += .5
		ball.yvel += .5
	player.update(ball, dt)
	ball.update(dt)
	draw_border(25, 100, ball, player, (99, 20))
	print(score)
while 1:
	mainloop(0.05)
	time.sleep(0.05)
