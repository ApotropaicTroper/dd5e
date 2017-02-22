import random as rand
import sys, re, glob
import charsheet

exit_cmd = {'quit','exit','halt','end','cease','desist','stop',''}



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

#not all spells do damage, such as Comprehend Languages. These will not be implemented.
def chromatic_orb():
	dmg = raw_input('Damage type? Fire/Cold/Lightning/Thunder/Acid/Poison\n')
	slot = raw_input('Spell slot level? ')
	roll('d20 + ' + str(char.Prof) + ' + ' + str(char.IntMod))
	if 'y' in raw_input('\nHit? ').lower():
		roll(str(int(slot)+2) + 'd8')
		print dmg + ' damage.'
	else:
		print 'Too bad!'	

def eldritch_blast():
	hits = -1
	for x in range(0,(char.level+1)/6 + 1):
		roll('d20 + ' + str(char.Prof) + ' + ' + str(char.ChrMod))
		print ''
	while hits < 0:
		try:
			hits = int(raw_input('How many hits? '))
			if hits > (char.level+1)/6 + 1:
				print 'That\'s too many!'
				hits = -1
				continue
		except:
			print 'That\'s not a number!'
	if hits == 0:
		print 'Too bad!'
		return -1
	for x in range(0, hits):
		roll('d10')
		print ' force damage.'

def witchbolt():
	slot = raw_input('Spell slot level? ')
	roll('d20 + ' + str(char.Prof) + ' + ' + str(char.IntMod))
	if 'y' in raw_input('\nHit? ').lower():
		roll(slot + 'd12')
		print ' lightning damage.'
	else:
		print 'Too bad!'




char = charsheet.char(raw_input('Name? '))

print str(char.Prof+char.IntMod)

while True:
	run = -1
	command = raw_input('> ')
#	if 'info' in command:
	#print spell description
	files = glob.glob('.\\Spells\\' + command + '.txt')
	if len(files) > 0:
		file = open(files[0])
#		for line in file:
#			print line,
		eval(command.lower().replace(' ','_') + '()')
		file.close()
		continue
	if command in exit_cmd and 'y' in raw_input('Are you sure? y/n\n').lower():
		break
	try:
		run = roll(command)
	except:
		print 'Malformed roll.\ne.g. 2d10+3-2'
	print ''
sys.exit()





