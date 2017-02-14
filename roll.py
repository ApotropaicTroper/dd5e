import random as rand
import sys


exit_com = {'quit','exit','halt','end','cease','desist','stop',''}




			#(number of dice)d(die type)
def roll(cmd):#returns -1 if error, 0 if exit, 1 if success
	bonus = 0
	if cmd in exit_com:
		return 0
	if 'd' not in cmd:
		return -1
	out = ['(' + cmd + '): [']
	cmd = cmd.split('d')
	if '+' in cmd[1]:
		bonus = int(cmd[1].split('+')[1])
		cmd[1] = cmd[1].split('+')[0]
	if '-' in cmd[1]:
		bonus = -int(cmd[1].split('-')[1])
		cmd[1] = cmd[1].split('-')[0]
	if cmd[0] == '':
		cmd[0] = '1'
	cmd[0] = int(cmd[0]) #reduce function calls by casting these to ints once before loop
	cmd[1] = int(cmd[1])
	total = 0		#Rolling sum
	for x in range(0,cmd[0]):
		if x != 0:
			out += ' + '
		roll = rand.randint(1,cmd[1])
					#Conditions? to be added later, if at all.
		total += roll
		out += [str(roll)]
	if bonus > 0:
		out += ' + ' + str(bonus)
	elif bonus < 0:
		out += ' - ' + str(abs(bonus))
	out += '] = '
	print ''.join(out), (total + bonus)
	return 1





while True:
	run = -1
	try:
		run = roll(raw_input('> '))
	except:
		pass
	if run == 0:
		break
sys.exit()





