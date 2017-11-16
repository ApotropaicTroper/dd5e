import sys, glob
import PyPDF2
import codecs
import pandas as pd


Scores_Abbr = ['Str','Dex','Con','Int','Wis','Cha']
#pg1header = {'CharacterName','ClassLevel','Background','PlayerName','Race','Alignment','XP'}
#stats = {'STR','DEX','CON','INT','WIS','CHA','STRmod','DEXmod','CONmod','INTmod','WISmod','CHamod',
#			'Inspiration','ProfBonus',
Scores_Full = ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma']
skills = ['Acrobatics','Animal','Arcana','Athletics','Deception','History',
		  'Insight','Intimidation','Investigation','Medicine','Nature','Perception',
		  'Performance','Persuasion','Religion','Sleight of Hand','Stealth','Survival','Passive']
#pg1col1 = stats | set(skills) | {'ProficienciesLang'}
#HPstats = {'HPMax','HPCurrent','HPTemp','HDTotal','HD'}
#wpns = {'AttacksSpellcasting','Wpn Name','Wpn Name 2','Wpn Name 3',
#		 'Wpn1 AtkBonus','Wpn2 AtkBonus','Wpn3 AtkBonus','Wpn1 Damage','Wpn2 Damage','Wpn3 Damage'}
#pg1col2 = {'AC','Initiative','Speed'} | HPstats | wpns | {'GP','EP','SP','CP','PP','Equipment'}
#pg1col3 = {'PersonalityTraits','Ideals','Bonds','Flaws','Features and Traits'}
#pg1 = pg1header | pg1col1 | pg1col2 | pg1col3

#pg2header = {'CharacterName 2','Age','Height','Weight','Eyes','Skin','Hair'}
#pg2 = pg2header | {'Allies','FactionName','Backstory','Feat+Traits','Treasure'}
#IMG = {'CHARACTER IMAGE','Faction Symbol Image'} #Do not have key '/V'

#spellstats = {'Spellcasting Class 2','SpellcastingAbility 2','SpellSaveDC 2','SpellAtkBonus 2'}
#negated = pg1 | pg2 | IMG | spellstats 
#test = range(0,20)
#print test[0:10]


class char:
	XP = 0
	level = 0		#Character Level
	race = ''
	classes = {}	#Key: class name. Value: class level. Multiclassing is possible, so dictionary
	Scores = {}		#Key: abbreviated score. Value: tuple of stat and its modifier
	Saves = {}		#						 Value: tuple of proficiency and modifier
	Skills = {}		#						 Value: tuple of proficiency and modifier
	AC = 0			#Armor Class
	Prof = 0		#Proficiency Bonus
	Init = 0		#Initiative Bonus
	Speed = 0		#Movement distance per round (measured in ft)
	HP = ()			#Tuple of maximum, current, and temporary HP
	HD = ()			#Tuple of maximum and current hit dice
	AC = 10

	spellList = [set(),set(),set(),set(),set(),set(),set(),set(),set(),set()]	#tuple of check box and corresponding line
	spellScore = None	#Which ability score do you use to cast spells, if able?
	spellBonus = 0		#Spell attack rolls get this as a bonus to hit
	spellDC = 0			#Difficulty class for opponents' saving throws against your magic

	def __init__(self, name):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		files = glob.glob('..\\*.pdf')
		charsheet = -1
		for file in files:
#			print file, name
			if name in file:
				charsheet = open(file, 'rb')
			else:
				continue
		if charsheet == -1:
			raise Exception('File not found!')
		fileReader = PyPDF2.PdfFileReader(charsheet)
		fields = fileReader.getFields()
		forms = dict((' '.join(k.split()),v.value) for k,v in fields.iteritems())
		for k in forms.keys():
			if 'Spells' in k:
				if len(k) == 12:
					forms[k[:8] + k[9:]] = forms.pop(k)
				if len(k) == 13:
					forms[k[:8] + k[9] + k[11:]] = forms.pop(k)
		forms['CHAmod'] = forms.pop('CHamod')
#XP thresholds:
#     0    300    900   2700   6500  14000  23000  34000  48000  64000
# 85000 100000 120000 140000 165000 195000 225000 265000 305000 355000
		self.XP = int(''.join(forms.pop('XP').split(' | ')[-1].split(',')))
		if   self.XP <    300: self.level = 1
		elif self.XP <    900: self.level = 2
		elif self.XP <   2700: self.level = 3
		elif self.XP <   6500: self.level = 4
		elif self.XP <  14000: self.level = 5
		elif self.XP <  23000: self.level = 6
		elif self.XP <  34000: self.level = 7
		elif self.XP <  48000: self.level = 8
		elif self.XP <  64000: self.level = 9
		elif self.XP <  85000: self.level = 10
		elif self.XP < 100000: self.level = 11
		elif self.XP < 120000: self.level = 12
		elif self.XP < 140000: self.level = 13
		elif self.XP < 165000: self.level = 14
		elif self.XP < 195000: self.level = 15
		elif self.XP < 225000: self.level = 16
		elif self.XP < 265000: self.level = 17
		elif self.XP < 305000: self.level = 18
		elif self.XP < 355000: self.level = 19
		else: self.level = 20
		self.Prof = (self.level-1)/4 + 2
		self.race = forms.pop('Race')
		self.classes = {str(cls.split()[0]) : int(cls.split()[1]) for cls in forms.pop('ClassLevel').split(' | ')[:-1]}
		self.Scores = {stat: (int(forms.pop(stat.upper())),int(forms.pop(stat.upper()+'mod'))) for stat in Scores_Abbr}
		self.Saves['Str'] = (forms.pop('Check Box 11')=='/Yes',int(forms.pop('ST Strength')))
		for x in range(18,23):
			self.Saves[Scores_Abbr[x-17]] = (forms.pop('Check Box '+str(x))=='/Yes',int(forms.pop('ST '+Scores_Full[x-17])))
		for x in range(23,41):
			self.Skills[skills[x-23]] = (forms.pop('Check Box '+str(x))=='/Yes',int(forms.pop(''.join(skills[x-23].split(' ')))))
			if skills[x-23] == 'Animal':
				self.Skills['Animal Handling'] = self.Skills.pop('Animal')
		self.Skills['Passive Perception'] =(None,int(forms.pop('Passive')))
		self.AC = int(forms.pop('AC'))
		self.Init = [int(x) for x in forms.pop('Initiative').split('|')]
		self.speed = int(forms.pop('Speed'))

		HPMax = forms.pop('HPMax')
		HPCurrent = forms.pop('HPCurrent')
		if HPCurrent == None:
			HPCurrent = HPMap
		HPTemp = forms.pop('HPTemp')
		if HPTemp == None:
			HPTemp = 0
		self.HP = (int(HPMax),int(HPCurrent),int(HPTemp))
		self.HD = (int(forms.pop('HDTotal')),forms.pop('HD'))
		assert self.HD[0] == self.level

		spellcheck = {'1014':None,'1015':'251','1046':'313','1034':'310','1048':'315','1047':'314',
					'1061':'317','1060':'316','1074':'319','1073':'318','1083':'321','1082':'320',
					'1092':'323','1091':'322','1101':'325','1100':'324','1108':'327','1107':'326'}
		spellcheck.update(dict(('10'+str(k),None) for k in range(16,23)))# 0
		spellcheck.update(dict(('10'+str(k+14),'30'+str(k)) for k in range(9,20)))# 1
		spellcheck.update(dict(('10'+str(k+15),'30'+str(k)) for k in range(20,31)))# 2
		spellcheck.update(dict(('10'+str(k+18),'30'+str(k)) for k in range(31,42)))# 3
		spellcheck.update(dict(('10'+str(k+20),'30'+str(k)) for k in range(42,53)))# 4
		spellcheck.update(dict(('10'+str(k+22),'30'+str(k)) for k in range(53,60)))# 5
		spellcheck.update(dict(('10'+str(k+24),'30'+str(k)) for k in range(60,67)))# 6
		spellcheck.update(dict(('10'+str(k+26),'30'+str(k)) for k in range(67,74)))# 7
		spellcheck.update(dict(('1' +str(k+28),'30'+str(k)) for k in range(74,79)))# 8
		spellcheck.update(dict(('1' +str(k+30),'30'+str(k)) for k in range(79,84)))# 9

		for k,v in spellcheck.iteritems():
			if v == None or 1016 <= int(k) <= 1022:	
				self.spellList[0] |= {(None, forms.pop('Spells '+k))}
			elif 1023 <= int(k) <= 1033 or k == '1015':
				self.spellList[1] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1034 <= int(k) <= 1046:
				self.spellList[2] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1047 <= int(k) <= 1059:
				self.spellList[3] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1060 <= int(k) <= 1072:
				self.spellList[4] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1073 <= int(k) <= 1081:
				self.spellList[5] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1082 <= int(k) <= 1090:
				self.spellList[6] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1091 <= int(k) <= 1099:
				self.spellList[7] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1100 <= int(k) <= 1106:
				self.spellList[8] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
			elif 1107 <= int(k) <= 1113:
				self.spellList[9] |= {(forms.pop('Check Box '+v)=='/Yes' , forms.pop('Spells '+k))}
		self.spellScore = forms.pop('SpellcastingAbility 2')
		self.spellBonus = self.Prof + self.Scores[self.spellScore][1]
		self.spellDC = 8 + self.spellBonus


#		for k,v in forms.iteritems():
#			print k,v
#		print '\n'*5







	def toString(self):
		out = ''
		out += self.race + ' ' + str(self.level) + ' ('
		first = True
		for cls,lvl in self.classes.iteritems():
			if not first:
				out += ' | '
			out += cls + ' ' + str(lvl)
			first = False
		out += ')\n'

		out += ' HP: '
		if self.HP[2] != 0:
			out += '(' + str(self.HP[2]) + ')  '
		out += str(self.HP[1]) + ' / ' + str(self.HP[0])

		out += '\n HD: ' + self.HD[1] + ' / ' + str(self.HD[0])

		for x in range(6):
			tup = self.Scores[Scores_Abbr[x]]
			out += '\n  ' + Scores_Abbr[x] + ': ' + str(tup[0]) + ' ('
			if tup[1] > 0:
				out += '+'
			out += str(tup[1]) + ')'

		out += '\nSaves:'
		for k,v in self.Saves.iteritems():
			out += '\n  ' + k + ': (' + str(v[0]) + ')\t'
			if v[1] > 0:
				out += '+'
			out += str(v[1])

		out += '\nSkills:'
		for k,v in self.Skills.iteritems():
			out += '\n  ' + k + ': ' + '\t'*((23-len(k))/4)
			if v[0] == None:
				out += '\t\t'
			else:
				out += '(' + str(v[0]) + ')\t'
			if v[1] > 0:
				out += '+'
			out += str(v[1]) 

		out += '\nProficiency Bonus: +' + str(self.Prof) + '\nArmor Class: ' + str(self.AC) + '\nInitiative Bonus: '
		first = True
		for x in self.Init:
			if not first:
				out += '/'
			out += '+' + str(x)
			first = False

			
		return out


test = char('Jebeddo the Green')
print test.toString()
'''
Spells
Spells <>
Cantrip:	1014, 1016-1022 (in order)
1st-level: 1015, 1023-1033
			251 -> 1015
  '30' + [9-19] -> '10' + [23-33]
2nd-level:	1034-1046
			313 -> 1046
			310 -> 1034
 '30' + [20-30] -> '10' + [35-45]
3rd-level:	1047-1059
   '31' + [5,4] -> '10' + [48,47]
 '30' + [31-41] -> '10' + [49-59]
4th-level:	1060-1072
   '31' + [7,6] -> '10' + [61,60]
 '30' + [42-52] -> '10' + [62-72]
5th-level:	1073-1081
   '31' + [9,8] -> '10' + [74,73]
 '30' + [53-59] -> '10' + [75-81]
6th-level:	1082-1090
   '32' + [1,0] -> '10' [83,82]
 '30' + [60-66] -> '10' + [84-90]
7th-level:	1091-1099
   '32' + [3,2] -> '10' + [92,91]
 '30' + [67-73] -> '10' + [93-99]
8th-level:	'1010' + [0-6]
   '32' + [5,4] -> '11' + [01,00]
 '30' + [74-78] -> '11' + [02-06]
9th-level:	'1010' + [7-13]
   '32' + [7,6] -> '11' + [08,07]
 '30' + [79-83] -> '11' + [09-13]
Total: SlotsTotal <19-27>
Expended: SlotsRemaining <19-27>
 18 + level
'''
'''
Check Boxes:
 Saving throws: ('/V':'/Yes')
 11: Str	 18: Dex	 19: Con	 20: Int	 21: Wis	 22: Cha
 Death saves:
 12:14 Success	15:17 Failure
 Skills:
 23: Acrobatics		 24: Animal Handling	 25: Arcana		 26: Athletics
'''
'''		for k in spReplace.keys():
			forms[spReplace[k]] = forms.pop('Spells 1' + k)
		for k in cbReplace.keys():
			forms[cbReplace[k]] = forms.pop('Check Box ' + k)
		for k in forms.keys():
			if 'SlotsRemaining ' in k:
				forms[k[:15] + str(int(k[15:])-18)] = forms.pop(k)
			if 'SlotsTotal ' in k:
				forms[k[:11] + str(int(k[11:])-18)] = forms.pop(k)
'''
'''
 27: Deception		 28: History			 29: Insight	 30: Intimidation
 31: Investigation	 32: Medicine			 33: Nature		 34: Perception
 35: Performance	 36: Persuasion			 37: Religion	 38: Sleight of Hand
 39: Stealth		 40: Survival
'''
'''
Spells 1014 	{'/V': u'Cantrip0', '/T': u'Spells 1014', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1016 	{'/V': u'Cantrip1', '/T': u'Spells 1016', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1017 	{'/V': u'Cantrip2', '/T': u'Spells 1017', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1018 	{'/V': u'Cantrip3', '/T': u'Spells 1018', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1019 	{'/V': u'Cantrip4', '/T': u'Spells 1019', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1020 	{'/V': u'Cantrip5', '/T': u'Spells 1020', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1021 	{'/V': u'Cantrip6', '/T': u'Spells 1021', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1022 	{'/V': u'Cantrip7', '/T': u'Spells 1022', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

SlotsTotal 19 	{'/V': u'Slots1', '/T': u'SlotsTotal 19', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 20 	{'/V': u'Slots2', '/T': u'SlotsTotal 20', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 21 	{'/V': u'Slots3', '/T': u'SlotsTotal 21', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 22 	{'/V': u'Slots4', '/T': u'SlotsTotal 22', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 23 	{'/V': u'Slots5', '/T': u'SlotsTotal 23', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 24 	{'/V': u'Slots6', '/T': u'SlotsTotal 24', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 25 	{'/V': u'Slots7', '/T': u'SlotsTotal 25', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 26 	{'/V': u'Slots8', '/T': u'SlotsTotal 26', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsTotal 27 	{'/V': u'Slots9', '/T': u'SlotsTotal 27', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 19 	{'/V': u'SlotsExpended1', '/T': u'SlotsRemaining 19', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 20 	{'/V': u'SlotsExpended2', '/T': u'SlotsRemaining 20', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 21 	{'/V': u'SlotsExpended3', '/T': u'SlotsRemaining 21', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 22 	{'/V': u'SlotsExpended4', '/T': u'SlotsRemaining 22', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 23 	{'/V': u'SlotsExpended5', '/T': u'SlotsRemaining 23', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 24 	{'/V': u'SlotsExpended6', '/T': u'SlotsRemaining 24', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 25 	{'/V': u'SlotsExpended7', '/T': u'SlotsRemaining 25', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 26 	{'/V': u'SlotsExpended8', '/T': u'SlotsRemaining 26', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}
SlotsRemaining 27 	{'/V': u'SlotsExpended9', '/T': u'SlotsRemaining 27', '/Ff': 12582912, '/DV': u'', '/FT': '/Tx'}

Spells 1015 	{'/V': u'Slot1a', '/T': u'Spells 1015', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1023 	{'/V': u'Slot1b', '/T': u'Spells 1023', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1024 	{'/V': u'Slot1c', '/T': u'Spells 1024', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1025 	{'/V': u'Slot1d', '/T': u'Spells 1025', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1026 	{'/V': u'Slot1e', '/T': u'Spells 1026', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1027 	{'/V': u'Slot1f', '/T': u'Spells 1027', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1028 	{'/V': u'Slot1g', '/T': u'Spells 1028', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1029 	{'/V': u'Slot1h', '/T': u'Spells 1029', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1030 	{'/V': u'Slot1i', '/T': u'Spells 1030', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1031 	{'/V': u'Slot1j', '/T': u'Spells 1031', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1032 	{'/V': u'Slot1k', '/T': u'Spells 1032', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1033 	{'/V': u'Slot1l', '/T': u'Spells 1033', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1046 	{'/V': u'Slot2a', '/T': u'Spells 1046', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1034 	{'/V': u'Slot2b', '/T': u'Spells 1034', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1035 	{'/V': u'Slot2c', '/T': u'Spells 1035', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1036 	{'/V': u'Slot2d', '/T': u'Spells 1036', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1037 	{'/V': u'Slot2e', '/T': u'Spells 1037', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1038 	{'/V': u'Slot2f', '/T': u'Spells 1038', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1039 	{'/V': u'Slot2g', '/T': u'Spells 1039', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1040 	{'/V': u'Slot2h', '/T': u'Spells 1040', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1041 	{'/V': u'Slot2i', '/T': u'Spells 1041', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1042 	{'/V': u'Slot2j', '/T': u'Spells 1042', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1043 	{'/V': u'Slot2k', '/T': u'Spells 1043', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1044 	{'/V': u'Slot2l', '/T': u'Spells 1044', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1045 	{'/V': u'Slot2m', '/T': u'Spells 1045', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1048 	{'/V': u'Slot3a', '/T': u'Spells 1048', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1047 	{'/V': u'Slot3b', '/T': u'Spells 1047', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1049 	{'/V': u'Slot3c', '/T': u'Spells 1049', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1050 	{'/V': u'Slot3d', '/T': u'Spells 1050', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1051 	{'/V': u'Slot3e', '/T': u'Spells 1051', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1052 	{'/V': u'Slot3f', '/T': u'Spells 1052', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1053 	{'/V': u'Slot3g', '/T': u'Spells 1053', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1054 	{'/V': u'Slot3h', '/T': u'Spells 1054', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1055 	{'/V': u'Slot3i', '/T': u'Spells 1055', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1056 	{'/V': u'Slot3j', '/T': u'Spells 1056', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1057 	{'/V': u'Slot3k', '/T': u'Spells 1057', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1058 	{'/V': u'Slot3l', '/T': u'Spells 1058', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1059 	{'/V': u'Slot3m', '/T': u'Spells 1059', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1061 	{'/V': u'Slot4a', '/T': u'Spells 1061', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1060 	{'/V': u'Slot4b', '/T': u'Spells 1060', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1062 	{'/V': u'Slot4c', '/T': u'Spells 1062', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1063 	{'/V': u'Slot4d', '/T': u'Spells 1063', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1064 	{'/V': u'Slot4e', '/T': u'Spells 1064', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1065 	{'/V': u'Slot4f', '/T': u'Spells 1065', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1066 	{'/V': u'Slot4g', '/T': u'Spells 1066', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1067 	{'/V': u'Slot4h', '/T': u'Spells 1067', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1068 	{'/V': u'Slot4i', '/T': u'Spells 1068', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1069 	{'/V': u'Slot4j', '/T': u'Spells 1069', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1070 	{'/V': u'Slot4k', '/T': u'Spells 1070', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1071 	{'/V': u'Slot4l', '/T': u'Spells 1071', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1072 	{'/V': u'Slot4m', '/T': u'Spells 1072', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1074 	{'/V': u'Slot5a', '/T': u'Spells 1074', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1073 	{'/V': u'Slot5b', '/T': u'Spells 1073', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1075 	{'/V': u'Slot5c', '/T': u'Spells 1075', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1076 	{'/V': u'Slot5d', '/T': u'Spells 1076', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1077 	{'/V': u'Slot5e', '/T': u'Spells 1077', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1078 	{'/V': u'Slot5f', '/T': u'Spells 1078', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1079 	{'/V': u'Slot5g', '/T': u'Spells 1079', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1080 	{'/V': u'Slot5h', '/T': u'Spells 1080', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1081 	{'/V': u'Slot5i', '/T': u'Spells 1081', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1083 	{'/V': u'Slot6a', '/T': u'Spells 1083', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1082 	{'/V': u'Slot6b', '/T': u'Spells 1082', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1084 	{'/V': u'Slot6c', '/T': u'Spells 1084', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1085 	{'/V': u'Slot6d', '/T': u'Spells 1085', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1086 	{'/V': u'Slot6e', '/T': u'Spells 1086', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1087 	{'/V': u'Slot6f', '/T': u'Spells 1087', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1088 	{'/V': u'Slot6g', '/T': u'Spells 1088', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1089 	{'/V': u'Slot6h', '/T': u'Spells 1089', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1090 	{'/V': u'Slot6i', '/T': u'Spells 1090', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 1092 	{'/V': u'Slot7a', '/T': u'Spells 1092', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1091 	{'/V': u'Slot7b', '/T': u'Spells 1091', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1093 	{'/V': u'Slot7c', '/T': u'Spells 1093', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1094 	{'/V': u'Slot7d', '/T': u'Spells 1094', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1095 	{'/V': u'Slot7e', '/T': u'Spells 1095', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1096 	{'/V': u'Slot7f', '/T': u'Spells 1096', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1097 	{'/V': u'Slot7g', '/T': u'Spells 1097', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1098 	{'/V': u'Slot7h', '/T': u'Spells 1098', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 1099 	{'/V': u'Slot7i', '/T': u'Spells 1099', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 10101 	{'/V': u'Slot8a', '/T': u'Spells 10101', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10100 	{'/V': u'Slot8b', '/T': u'Spells 10100', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10102 	{'/V': u'Slot8c', '/T': u'Spells 10102', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10103 	{'/V': u'Slot8d', '/T': u'Spells 10103', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10104 	{'/V': u'Slot8e', '/T': u'Spells 10104', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10105 	{'/V': u'Slot8f', '/T': u'Spells 10105', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10106 	{'/V': u'Slot8g', '/T': u'Spells 10106', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

Spells 10108 	{'/V': u'Slot9a', '/T': u'Spells 10108', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10107 	{'/V': u'Slot9b', '/T': u'Spells 10107', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 10109 	{'/V': u'Slot9c', '/T': u'Spells 10109', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 101010 	{'/V': u'Slot9d', '/T': u'Spells 101010', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 101011 	{'/V': u'Slot9e', '/T': u'Spells 101011', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 101012 	{'/V': u'Slot9f', '/T': u'Spells 101012', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}
Spells 101013 	{'/V': u'Slot9g', '/T': u'Spells 101013', '/Ff': 8388608, '/DV': u'', '/FT': '/Tx'}

'''
'''
#		print fields['ClassLevel']['/V'].split(' ')[1]
#		for key in fields.keys():
#			if 'Check Box ' in key and len(key) < 13:
#				for key2 in fields[key].keys():
#					try:
#						if fields[key]['/V'] == '/Yes':
#							print key
#							print '    ', key2
#							print '        ', fields[key][key2]
#					except:
#						continue
		self.level = int(fields['ClassLevel']['/V'].split(' ')[-1])
		self.Prof = (self.level-1)/4 + 2
		self.AC = int(fields['AC']['/V'])

		self.Str = int(fields['STR']['/V'])
		self.Dex = int(fields['DEX']['/V'])
		self.Con = int(fields['CON']['/V'])
		self.Int = int(fields['INT']['/V'])
		self.Wis = int(fields['WIS']['/V'])
		self.Chr = int(fields['CHA']['/V'])
		self.StrMod = (self.Str-10)/2
		self.DexMod = (self.Dex-10)/2
		self.ConMod = (self.Con-10)/2
		self.IntMod = (self.Int-10)/2
		self.WisMod = (self.Wis-10)/2
		self.ChrMod = (self.Chr-10)/2
#Skill Proficiencies keys:	fields[key]['/V'] == '/Yes'

		self.CastScore = fields['SpellcastingAbility 2']['/V']
		self.CastBonus = self.Prof + eval('self.' + self.CastScore + 'Mod')
		self.CastDC = 8 + self.CastBonus 


		self.Speed = int(fields['Speed']['/V'])
		self.PassWis = 10+self.WisMod

#		self.spell0 = [fields['Spells 1014']['/V'],fields['Spells 1016']['/V'],fields['Spells 1017']['/V'],fields['Spells 1018']['/V'],fields['Spells 1019']['/V'],fields['Spells 1020']['/V'],fields['Spells 1021']['/V'],fields['Spells 1022']['/V']]
						#Cantrip0					Cantrip1					Cantrip2					Cantrip3					Cantrip4					Cantrip5					Cantrip6					Cantrip7
#		for x in range(0,len(self.spell0)):
#			self.spell0[x] = self.spell0[x].strip()
#		self.spell1 = []
#		self.spell2 = []
#		self.spell3 = []
#		self.spell4 = []
#		self.spell5 = []
#		self.spell6 = []
#		self.spell7 = []
#		self.spell8 = []
#		self.spell9 = []
#		print fields['Acrobatics']['/V']
		charsheet.close()

	def toString(self):
		print 'Level:', str(self.level)
		print 'Proficiency Bonus:', str(self.Prof)
		print 'Initiative Bonus:', str(self.DexMod)
		print 'Armor Class:', str(self.AC)
		print 'Strength:', str(self.Str), '(' + str(self.StrMod) + ')'
		print 'Dexterity:', str(self.Dex), '(' + str(self.DexMod) + ')'
		print 'Constitution:', str(self.Con), '(' + str(self.ConMod) + ')'
		print 'Intelligence:', str(self.Int), '(' + str(self.IntMod) + ')'
		print 'Wisdom:', str(self.Wis), '(' + str(self.WisMod) + ')'
		print 'Charisma:', str(self.Chr), '(' + str(self.ChrMod) + ')'
		print 'Spellcasting Ability Modifier:', self.CastScore
		print ' Spell Save DC:', self.CastDC
		print ' Spell Attack Bonus:', self.CastBonus
		print 'Speed:', str(self.Speed)
		print 'Passive Perception:',self.PassWis
'''
