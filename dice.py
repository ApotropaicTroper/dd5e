import numpy as np

_lastroll = []

#types is a list: [number of dice, sides per die]
def roll(types):
	global _lastroll
	_lastroll = [(np.random.randint(int(types[1]))+1) for _ in range(int(types[0]))]
	_lastroll.sort()
	return _lastroll

def results():
	return _lastroll
#lowest num items in lastroll
def min(num):
	return _lastroll[:num]
#highest num items in lastroll
def max(num):
	return _lastroll[-num:]
#add all values and a modifier
def total(num = 0):
	return sum(_lastroll) + num
