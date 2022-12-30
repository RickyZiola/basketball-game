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
	def get_pos(self):
		return (self.xpos, self.ypos)
	def get_vel(self):
		return (self.xvel, self.yvel)
	def update(self, ball):
		if(not self.grounded):
			self.yvel -= .1
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

		self.xpos += self.xvel
		self.ypos += self.yvel
class Ball:
	def __init__(self):
		self.xpos = 0
		self.ypos = 0
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
	def update(self):
		self.yvel -= .1
		if(self.xpos > 99):
			self.xvel = -self.xvel
		if(self.xpos < 0):
			self.xvel = -self.xvel
		if(self.ypos < -25):
			self.yvel = -self.yvel / 1.1
		self.xpos += self.xvel
		self.ypos += self.yvel
ball = Ball()
player = Player()
ball.xvel = .5
def draw_border(height, width, ball, player, hoop_pos):
	for y in range(height):
		for x in range(width):
			if(int(ball.xpos) == x and int(-ball.ypos) == y):
				print("o", end="")
			elif(int(player.xpos) == x and int(-player.ypos) == y):
				print(chr(165), end="")
			elif(hoop_pos[0] == x and hoop_pos[1] == y):
				print("_", end="")
			else:
				print(" ", end="")
		print("|")
	for x in range(width):
		print("-", end="")
	print()

def mainloop():
	clear()
	if(keyboard.is_pressed("w")):
		print("JUMP")
	if(keyboard.is_pressed("space") and player.is_grounded):
		player.is_grounded = False
		player.yvel = 2
	if(keyboard.is_pressed("right_arrow")):
		player.xvel += .1
	if(keyboard.is_pressed("left_arrow")):
		player.xvel -= .1
	player.update(ball)
	ball.update()
	draw_border(25, 100, ball, player, (99, 10))
	print(keyboard.is_pressed("w"))
while 1:
	mainloop()
	time.sleep(0.1)
