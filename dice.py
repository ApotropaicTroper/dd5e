import numpy as np


#dice group:
# <N>d<S>, where <N> is the number of dice and <S> is the number of sides
class dice:

	count = 0
	sides = 0
	lastroll = []
	lastmod = 0

#input: NdS, where N and S are integers
	def __init__(self,cmd_word) :
		params = cmd_word.split('d')
		if params[0] == '':
			params[0] = '1'
		try:
			assert str.isdigit(params[0]) and str.isdigit(params[1])
		except:
			print 'Malformed dice group. Must be <int>d<int>'
			return
		self.count = int(params[0])
		self.sides = int(params[1])
		self.roll()

#mod is a per-die modifier
	def roll(self, mod = 0):
		self.lastroll = []
		for int in range(self.count):
			self.lastroll.append(np.random.randint(self.sides)+1 + mod)
		self.lastroll.sort()
		self.lastmod = mod
		return self.lastroll

	def dietype(self):
		return str(self.count) + 'd' + str(self.sides)
	def lastroll(self):
		return self.lastroll

#lowest num items in lastroll
	def min(self,num):
		return self.lastroll[:num]
#highest num items in lastroll
	def max(self,num):
		return self.lastroll[-num:]
	def sum(self):
		return sum(self.lastroll)
#Dice + Dice = total + total
	def __radd__(self,arg):# die + die + die = int + die. Must be right-associative
		try:
			return self.sum() + arg.sum()
		except:
			return self.sum() + arg
#Dice * int = total * int
	def __mul__(self,num):
		print 'left multiply'
		return self.sum()*num
#int * Dice = Roll dice int times, return the full list of rolls. Use last per-die modifier
	def __rmul__(self,num):
		print 'right multiply'
		self.lastroll = []
		for int in range(num):
			self.lastroll += self.roll(self.lastmod)
		return self.lastroll

