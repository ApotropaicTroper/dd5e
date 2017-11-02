import random as rand
import re, glob
#from string import capwords
from inflect import engine	#inflecting numbers (i.e. 1 -> 1st)
import pandas as pd
import numpy as np
#import charsheet


'''
To do:
  Replace "info" function with pulling from excel spreadsheet instead of compendium site
  package: pandas
Might want to do:
  Command GUI: visual of chosen dice when roll command used
  (TkInter?)
problem spells:
light
'''

exit_cmd = {'quit','exit','halt','end','cease','desist','stop',''}
Ab_Scores = ['Str','Dex','Con','Int','Wis','Chr']
#classes = {0:'Barbarian',1:'Bard',2:'Cleric',3:'Druid',4:'Fighter',5:'Monk',6:'Paladin',7:'Ranger',8:'Rogue',9:'Sorcerer',10:'Warlock',11:'Wizard'}
				#(number of dice)d(die type)
def roll(cmd):#returns -1 if exit, 1 if normal operation
	if 'd' not in cmd:
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
	print '(' + cmd + '): [' + rolls + '] = ' + str(eval(rolls)),
	return 1

#Not all spells do damage, such as Comprehend Languages.
# These will not be implemented except to be described with "info".
def chromaticorb(mod):
	dmg = raw_input('Damage type? \n')
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 1-9'

	roll('d20+' + str(char.CastBonus))
	response = raw_input('\nHit? ')
	if 'a' in response or 'd' in response:
		roll('d20+' + str(char.CastBonus))
	elif 'n' in response:
		print 'Too Bad!'
		return -1
	if 'y' in response or 'y' in raw_input('\nHit? ').lower():
		roll(str(slot+2) + 'd8')
		print ' Fire/Cold/Lightning/Thunder/Acid/Poison + damage.'
	else:
		print 'Too bad!'	

def eldritchblast(mod):
	hits = -1
	for x in range(0,(char.level+1)/6 + 1):
		roll('d20+' + str(char.CastBonus))
		print ''
	while hits < 0:
		try:
			hits = int(raw_input('How many hits? '))
			if hits > (char.level+1)/6 + 1:
				print 'Not enough beams!'
				hits = -1
				continue
		except:
			print 'That\'s not a number!'
	if not hits:
		print 'Too bad!'
		return -1
	for x in range(0, hits):
		roll('d10')
		print 'Force damage.'

def falselife(mod):
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 1-9'
	roll('d4+1 + ' + str((slot-1)*5))
	print ' Temporary hit points.'

def firebolt(mod):#'a' for advantage, 'd' for disadvantage
	roll('d20+' + str(char.CastBonus))
	response = raw_input('\nHit? ')
	if 'a' in response or 'd' in response:
		roll('d20+' + str(char.CastBonus))
	elif 'n' in response:
		print 'Too Bad!'
		return -1
	if 'y' in response or 'y' in raw_input('\nHit? ').lower():
		roll(str((char.level+1)/6 + 1) + 'd10')
		print 'Fire damage.'
	else:
		print 'Too bad!'

def lightningbolt(mod):
	slot = 0
	while slot < 3 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 3-9'
	roll(str(slot+5) + 'd6')
	print 'Lightning damage.'

def magicmissile(mod):
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 1-9'
	for x in range(0,slot+2):
		roll('d4+1')
		print 'Force damage.'

def rayoffrost(mod):
	roll('d20+' + str(char.CastBonus))
	response = raw_input('\nHit? ')
	if 'a' in response or 'd' in response:
		roll('d20+' + str(char.CastBonus))
	elif 'n' in response:
		print 'Too Bad!'
		return -1
	if 'y' in response or 'y' in raw_input('\nHit? ').lower():
		roll(str((char.level+1)/6 + 1) + 'd8')
		print 'Cold damage.'
	else:
		print 'Too bad!'

def scorchingray(mod):
	slot = 0
	while slot < 2 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 2-9'

	for x in range(0,slot+1):
		roll('d20+' + str(char.CastBonus))
		print ''
	hits = -1
	while hits < 0:
		try:
			hits = int(raw_input('How many hits? '))
			if hits > slot+1:
				print 'Not enough beams!'
				hits = -1
		except:
			print 'That\'s not a number!'
	if not hits:
		print 'Too bad!'
		return -1
	for x in range(0,hits):
		roll('2d6')
		print 'Fire damage.'	

def witchbolt(mod):
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 1-9'
	roll('d20+' + str(char.CastBonus))
	response = raw_input('\nHit? ')
	if 'a' in response or 'd' in response:
		roll('d20+' + str(char.CastBonus))
	elif 'n' in response:
		print 'Too Bad!'
		return -1
	if 'y' in response or 'y' in raw_input('\nHit? ').lower():
		roll(str(slot) + 'd12')
		print 'Lightning damage.'
	else:
		print 'Too bad!'

#Problematic Spells: Dispel Magic
#df['label'] yields Series: column with that label and indexes
#df.loc[index] yields Series: row with that index
#df.loc[row,col]
def info(spell): #receive name of spell only
	fpath = glob.glob('.\\spells.xlsx')[0]
#	print fpath
	compendium = pd.read_excel(fpath)
#	print compendium['name']
#	print compendium.loc[0,'name']
	names = compendium['name']
	index = -1
	for item in range(names.size):
		if spell == compendium.loc[item,'name']:
			index = item
			break
	if index == -1:
		print 'Spell not found'
		return -1
	spell = compendium.loc[index]
	print spell
	out = spell['name'] + '\n'
	if not spell['level']:
		out += spell['school'] + 'cantrip'
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
	out += '\n' + spell['source_book'] + ', Page ' + str(spell['source_page']) + '\n'
	print out
'''
properties:
name	level	school	is_ritual	casting_time	spell_range
comp_verb	comp_som	comp_mat	materials
duration	concentration
description		at_higher_levels
source_book		source_page
casting_classes
 can_barbarian	can_bard	can_cleric	can_druid		can_fighter		can_monk,
 can_paladin	can_ranger	can_rogue	can_sorcerer	can_warlock		can_wizard
'''
#	for row in compendium.iterrows():	#row is a tuple: index, Series
info('Fire Bolt')
info('Magic Missile')
info('Spider Climb')
info('Fireball')

'''
char = charsheet.char(raw_input('Name? '))
while True:
	run = -1
	command = raw_input('> ')
	if 'info' in command: 	#print spell description
		try:
			info(command[5:])
		except:
			char.toString()
		continue
	if command in exit_cmd:# and 'y' in raw_input('Are you sure? y/n\n').lower():
		break
#is the command a spell in the spell list? If so, run spell command
#otherwise attempt to roll dice
	files = glob.glob('.\\Spells\\' + command.replace(' ','') + '.txt')
	if len(files):
		try:
			mod = char.CastScore
			eval(command.replace(' ','') + '(\'' + mod + '\')')
		except:
			info(command)
		continue
	try:
		run = roll(command)
	except:
		print 'Malformed roll.\ne.g. 2d10+3-2'
	print ''
'''




