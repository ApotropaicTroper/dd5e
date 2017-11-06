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
	def __add__(self,die2):
		return self.sum() + die2.sum()
#Dice + int = total + modifier
	def __add__(self,mod):
		return self.sum() + mod

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

'''
Dice notation:
+- mean perform that operation on the results
<dice>*/<number> mean perform that operation on the results
  does not mean reroll
       2d6*5 = [2:12]*5 = [10:60]
   (2d6+4)*5 = [6:16]*5 = [30:80]
<number>*<dice> means perform that operation on the number of dice. i.e. 4*3d6 = 12d6
  indicates a reroll
       3*2d6 =    6d6 =  [6:36]
   3*2d6 + 4 =  6d6+4 = [10:40]
   3*(2d6+4) = 6d6+12 = [18:48]

'''

#die = dice('2d6')
#print die.dietype()
#print die.roll()
#print die.min(10)
#print die.max(10)
#print die.sum()