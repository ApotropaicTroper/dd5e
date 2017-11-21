import glob
from inflect import engine	#inflecting numbers (i.e. 1 -> 1st)
import re
import pandas as pd
import numpy as np
import dice
#from string import capwords
#import charsheet


'''
To do:

Might want to do:
  Command GUI: visual of chosen dice when roll command used
  (TkInter?)
'''

exit_cmd = {'quit','exit','halt','end','cease','desist','stop',''}
Ab_Scores = ['Str','Dex','Con','Int','Wis','Chr']
compendium = pd.read_excel(glob.glob('.\\spells.xlsx')[0])
names = compendium['name']
#df['label'] yields Series: column with that label and indexes
#df.loc[index] yields Series: row with that index
#df.loc[row,col]

def info(index):
	spell = compendium.loc[index]
	out = spell['name'] + '\n'
	if not spell['level']:
		out += spell['school'] + ' cantrip'
	else:
		out += engine().ordinal(spell['level']) + '-level ' + spell['school']
	out += '\nCasting Time: ' + spell['casting_time'] + '\nRange: ' + spell['spell_range']
	out += '\nComponents: '
	if spell['comp_verb']:
		out += 'V '
	if spell['comp_som']:
		out += 'S '
	if spell['comp_mat']:
		out += 'M (' + spell['materials'] + ')'
	out += '\nDuration: '
	if spell['concentration']:
		out += 'Concentration, '
	out += spell['duration'] + '\n\n' + spell['description']
	if spell['at_higher_levels'] != 'None':
		out += '\n\nAt Higher Levels:\n\t' + spell['at_higher_levels']
	out += '\n\nClasses: ' + spell['casting_classes']
	out += '\n\t' + spell['source_book'] + ', Page ' + str(spell['source_page']) + '\n'
	print out
#print names
#properties:
#name		level	school	is_ritual	casting_time	spell_range
#comp_verb	comp_som	comp_mat	materials
#duration	concentration
#description	at_higher_levels
#source_book	source_page
#casting_classes
# can_barbarian	can_bard	can_cleric	can_druid		can_fighter		can_monk,
# can_paladin	can_ranger	can_rogue	can_sorcerer	can_warlock		can_wizard

#print compendium.loc[0]
def isSpell(spell):
	spellFound = False
	for x in range(names.size):
		if spell.lower() == names[x].lower():
			spellFound = x
			break
	return spellFound




def dparse(word):#returns list of terms




	temp = word.split('+')
	word = []
	for term in temp:
		term = term.split('-')
		word.append(term[0].strip())
		if len(term) == 1:
			continue
		word.extend('-'+str(sub).strip() for sub in term[1:])

	out = []
	for index in range(len(word)):
		if 'd' in word[index] and '*' not in word[index]:
			die = dice.dice(word[index])
			out.append(die.lastroll)
		else:
			out.append(int(word[index]))
	return out




'''
Split based on +/-. Anything within parentheses should be its own term (nested list?), including * attached to it
For each term:
	If 'd' in the term, that's a die object. Roll
	If '*' in term, then consider the operands
		if die * num, replace with sum*int
		if num * die, roll die num times

'''





while True:
	entry = raw_input('> ')
	if entry in exit_cmd:
		break
	index = isSpell(entry)
	if index:
		info(index)
	elif 'd' in entry:
		print dparse(entry)
#parse command: Every <int>d<int> becomes a dice object. Roll each dice object. Print list of rolls and their sum










'''
+
 die + die = sum + sum
 die + int = sum + int

-
 die - int = sum - int
 Equivalent to '+' with int < 0
*
 die * int = sum * int
 int * die = roll die <int> times. Returns list of all rolls
  int must be positive
/
 die / int = sum / int
()
 (die + int) = same as die + int
 int * (die + int) = list of <int 1> rolls of die with <int2> as modifier
  Examples:
   3 * (1d4 + 1) -> [1d4+1, 1d4+1, 1d4+1]
   3 * (d20 + 8) -> [d20+8, d20+8, d20+8]

3 (d20+8) *

'''




'''	if 'd' not in cmd:
		print 'That\'s no roll at all!'
		return -1
	cmd = re.sub(' *\+ *',' +',cmd)
	cmd = re.sub(' *- *',' -',cmd)
	parse = cmd.split(' ')

	cmd = re.sub('\+','+ ',cmd)
	cmd = re.sub('-','- ',cmd)

	rolls = []
	for term in parse:
		if 'd' in term:
			dice = term.replace('+','').split('d')
			if not len(dice[0]):
				dice[0] = '1'
			temp = []
			for x in range(0,int(dice[0])):
				temp += ['+',str(rand.randint(1,int(dice[1])))]
			rolls += [' '.join(temp)]
		else:
			rolls += [term[0] + ' ' + term[1:]]

	rolls = ' '.join(rolls)[2:]
	result = eval(rolls)
	print '(' + cmd + '): [' + rolls + '] = ' + str(result),
	return result'''






