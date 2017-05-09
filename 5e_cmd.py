import random as rand
import re, glob, codecs
import charsheet
from bs4 import BeautifulSoup
from string import capwords
from inflect import engine
import urllib, requests

compendium = 'https://www.dnd-spells.com/spells/'
#Problematic spells thus far:
#None that I know of.
 
exit_cmd = {'quit','exit','halt','end','cease','desist','stop',''}
Ab_Scores = ['Str','Dex','Con','Int','Wis','Chr']
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
	print '(' + cmd + '): [' + rolls + '] = ' + str(eval(rolls))
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
		print dmg.capitalize() + ' damage.'
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

def info(spell): #receive name of spell only
	if not spell:
		raise Exception
#look for the spell in files; if not there, get from internet
	for file in glob.glob('.\\Spells\\*.txt'):
		if spell.replace(' ','') in file.lower():
			fr = codecs.open('.\\Spells\\' + spell.replace(' ','') + '.txt','r','utf-8')
			for line in fr:
				print line,
			print ''
			fr.close()
			return 1

	spellIn = spell	
	spell = spell.replace('\'',u'\u2019')
	soup = BeautifulSoup(requests.get(compendium).text,'lxml')
	for tr in soup.tbody.findAll('tr'):
		td = tr.findAll('td')
		if td[1].a.string.lower().split(' (')[0] == spell:
			alphSoup = BeautifulSoup(requests.get(td[1].a.get('href')).text,'lxml')	#"spell"ing with alphabet soup
			info = alphSoup.find('div',{'class':'col-md-12'})
			out = ['', info.h1.span.string]
			p = info.findAll('p')[:-1]

			school = p[0].string
			stats = p[1].findAll('strong')
			level = stats[0].string.strip()
			if level == 'Cantrip':
				out += [' ' + school + ' ' + level,'']
			else:
				out += [' ' + engine().ordinal(level) + '-level ' + school,'']
			out += ['Casting Time: ' + stats[1].string,
					'Range: ' + stats[2].string,
					'Components: ' + stats[3].string,
					'Duration: ' + stats[4].string]

#if casting time is a reaction, then don't print an extra newline; print it after reaction
			reaction = 'Reaction' in str(p[2])
			for par in str(p[2]).split('<br/>'):
				par = re.sub('<[^<]+?>','',par)		#strip other html codes
				if reaction:
					out += [' '*4 + par.strip()]
					reaction = False
					continue
				if ' '*6 not in out:
					out += [' '*6]
				if par.strip() != '':
					out += [' '*8 + par.strip()]

#If spell scales with spell slot level, separate this line from rest of description
			if len(p) - 6:
				out += ['']
				for par in re.sub('</?p>','',str(p[3])).split('<br/>'):
					out += [' '*8 + par.strip()]
			out += ['\nClasses:', ' ' + ', '.join([a.string for a in p[-1].findAll('a')]),'']
			out = '\n'.join(out)
			print out
			fw = codecs.open('.\\Spells\\' + ''.join(capwords(spellIn).split()) + '.txt','w','utf-8')
			fw.write(out)
			fw.close()
#Write the spell to a text file
			return 1
	print 'Spell not found. Did you mistype it?'


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





