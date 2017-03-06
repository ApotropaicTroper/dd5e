import random as rand
import sys, re, glob
import charsheet
from bs4 import BeautifulSoup
import urllib, requests

compendium = 'https://roll20.net/compendium/dnd5e/Spells:'
#URL form: compendium + spell (space -> '%20') + '#h-' + spell (space -> '%20)
exit_cmd = {'quit','exit','halt','end','cease','desist','stop',''}
Ab_Scores = ['Str','Dex','Con','Int','Wis','Chr']

				#(number of dice)d(die type)
def roll(cmd):#returns -1 if error, 0 if exit, 1 if success
	if 'd' not in cmd:
		return -1
	cmd = re.sub(' *\+ *',' + ',cmd)
	cmd = re.sub(' *- *',' - ',cmd) #formatting for output

	out = ['(' + cmd + '): ['] #output string
	parse = re.split(' \+ | - ',cmd,1)
	dice = parse[0]

	if len(parse) > 1:
		if cmd.split(dice)[1][1] == '-': #if first modifier is a penalty, prefix with a minus sign
			parse[1] = ' - ' + parse[1]
		else:
			parse[1] = ' + ' + parse[1]

	dice = dice.split('d') #reduce function calls by casting these to ints once before loop
	if dice[0] == '':
		dice[0] = '1'
	dice[0] = int(dice[0]) #number of dice to roll
	dice[1] = int(dice[1]) #number of sides to the die (numbered 1 to n)

	total = 0		#Rolling sum
	for x in range(0,dice[0]):
		if x != 0:
			out += [' + ']
		roll = rand.randint(1,dice[1])
					#Conditions? to be added later, if at all.
		total += roll
		out += [str(roll)]
	if len(parse) > 1:
		total += eval(parse[1])
		out.extend([parse[1]])
	out += ['] = ' + str(total)]
	print ''.join(out),
	return 1

#Not all spells do damage, such as Comprehend Languages.
# These will not be implemented except to be described with "info".
def chromaticorb(mod):
	dmg = raw_input('Damage type? Fire/Cold/Lightning/Thunder/Acid/Poison\n')
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number!',

	roll('d20 + ' + str(char.Prof) + ' + ' + str(eval('char.' + mod + 'Mod')))
	if 'y' in raw_input('\nHit? ').lower():
		roll(str(slot+2) + 'd8')
		print dmg.capitalize() + ' damage.'
	else:
		print 'Too bad!'	

def eldritchblast(mod):
	hits = -1
	for x in range(0,(char.level+1)/6 + 1):
		roll('d20 + ' + str(char.Prof) + ' + ' + str(char.ChrMod))
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
	if hits == 0:
		print 'Too bad!'
		return -1
	for x in range(0, hits):
		roll('d10')
		print 'Force damage.'

def firebolt(mod):
	roll('d20 + ' + str(char.Prof) + ' + ' + str(eval('char.' + mod + 'Mod')))
	if 'y' in raw_input('\nHit? ').lower():
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
			print 'That must be a number, 3-9',
	roll(str(slot+5) + 'd6')
	print 'Lightning damage.'

def magearmor(mod):
	print 'AC becomes ' + str(13 + char.DexMod)

def magicmissile(mod):
	slot = 0
	while slot < 1 or slot > 9:
		try:
			slot = int(raw_input('Spell slot level? '))
		except:
			print 'That must be a number, 1-9',
	for x in range(0,slot+2):
		roll('d4+1')
		print 'Force damage.'

def rayoffrost(mod):
	roll('d20 + ' + str(char.Prof) + ' + ' + str(eval('char.' + mod + 'Mod')))
	if 'y' in raw_input('\nHit? ').lower():
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
			print 'That must be a number, 2-9',

	for x in range(0,slot+1):
		roll('d20 + ' + str(char.Prof) + ' + ' + str(eval('char.' + mod + 'Mod')))
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
	if hits == 0:
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
			print 'That must be a number, 1-9',
	roll('d20 + ' + str(char.Prof + char.IntMod))
	if 'y' in raw_input('\nHit? ').lower():
		roll(str(slot) + 'd12')
		print 'Lightning damage.'
	else:
		print 'Too bad!'
def info(cmd): #receive name of spell only
	spell = cmd.replace(' ','%20')
	url = compendium + spell + '#h-' + spell
	soup = BeautifulSoup(requests.get(url).text, 'lxml')
	title = str(soup.title)[7:].split(' | ')[0]
	info = soup.find('meta',{'name':'description'})['content']
	print '\n'.join((title,info))

char = charsheet.char(raw_input('Name? '))
while True:
	run = -1
	command = raw_input('> ')
	command = command.replace('\'','\\\'')
	if 'info' in command: 	#print spell description
		info(command[5:])
		continue
	mod = char.CastScore
	try:
		eval(command.replace(' ','') + '(\'' + mod + '\')')
	except:
		pass
	if command in exit_cmd:# and 'y' in raw_input('Are you sure? y/n\n').lower():
		break
	try:
		run = roll(command)
	except:
		print 'Malformed roll.\ne.g. 2d10+3-2'
	print ''
sys.exit()





