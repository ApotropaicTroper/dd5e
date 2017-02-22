import random as rand
import sys, re, glob


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
	print ''.join(out)
	return 1



while True:
	run = -1
	command = raw_input('> ')
	files = glob.glob('.\\Spells\\' + command + '.txt')
	if len(files) > 0:
		file = open(files[0])
		for line in file:
			print line,
		file.close()
		break
	if command in exit_cmd:
		break
	try:
		run = roll(command)
	except:
		print 'Malformed roll.\ne.g. 2d10+3-2'
	if run == 0:
		break
sys.exit()





