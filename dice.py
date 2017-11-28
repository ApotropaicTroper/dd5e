import numpy as np


#dice group:
# <N>d<S>, where <N> is the number of dice and <S> is the number of sides
#class dice:

lastroll = []

#input: NdS, where N and S are integers
#	def __init__(self,word,mod = 0):
#		params = word.split('d')
#		if params[0] == '':
#			params[0] = '1'
#		try:
#			assert int(params[0]) > 0 and int(params[1]) > 0
#			self.count = int(params[0])
#			self.sides = int(params[1])
#			self.roll(mod)
#		except AssertionError:
#			print 'No dice. (Must be positive)'
#		except ValueError:
#			print 'No dice. (<int>d<int>)'


#types is a list: [number of dice, sides per die]
def roll(types):
	lastroll = [(np.random.randint(int(types[1]))+1) for _ in range(int(types[0]))]
	lastroll.sort()
	return lastroll

#	def roll(self, count, sides):

#def dietype(self):
#	return str(self.count) + 'd' + str(self.sides)


def results():
	return lastroll
#lowest num items in lastroll
def min(num):
	return lastroll[:num]
#highest num items in lastroll
def max(num):
	return lastroll[-num:]

'''
	def __add__(self,num):
		self.roll()
		return self.sum() + num
#Dice + Dice = total + total
	def __radd__(self,arg):# die + die + die = int + die. Must be right-associative
		self.roll()
		try:
			return self.sum() + arg.sum()
		except:
			return self.sum() + arg
#Dice * int = total * int
	def __mul__(self,num):
		self.roll()
		return self.sum()*num
#int * Dice = Roll dice int times, return the full list of rolls. Use last per-die modifier
	def __rmul__(self,num):
		try:
			assert num > 0
		except:
			print 'That must be positive'
			return
		rolls = []
		for _ in range(num):
			rolls.append(self.roll(self.lastmod))
		self.lastroll = []
		self.lastroll = rolls
		return self.lastroll

#Dice / int = sum / int
	def __div__(self,num):
		self.roll()
		try:
			assert num > 0
		except:
			print 'Divide by zero error'
			return self.sum()
		return self.sum()/num
'''