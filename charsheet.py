import sys, glob
import PyPDF2
class char:
	level = -999	#Character Level
	AC = -999999	#Armor Class
	Prof = -9999	#Proficiency Bonus
	Init = -9999	#Initiative Bonus
	Speed = -999	#Movement distance per round
	Str = -99999	#Strength
	StrMod = -99	# ^ Modifier
	Dex = -99999	#Dexterity
	DexMod = -99	# ^ Modifier
	Con = -99999	#Constitution
	ConMod = -99	# ^ Modifier
	Int = -99999	#Intelligence
	IntMod = -99	# ^ Modifier
	Wis = -99999	#Wisdom
	WisMod = -99	# ^ Modifier
	Chr = -99999	#Charisma
	ChrMod = -99	# ^ Modifier

	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		char = 'testsheet'
		files = glob.glob('C:\\Users\\Jethro\\Desktop\\*.pdf')
#		print files
		charsheet = -1
		for file in files:
			if char in file:
				charsheet = open(file, 'rb')
			else:
				continue
		if charsheet == -1:
			raise Exception('File not found!')
		fileReader = PyPDF2.PdfFileReader(charsheet)
		fields = fileReader.getFields()
#		print fields['ClassLevel']['/V'].split(' ')[1]
		for key in fields.keys():
			if 'Spells' in key:
				print key
				print fields[key]
				for key2 in fields[key].keys():
					print '    ', key
					print '        ', fields[key][key2]
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

		self.Speed = int(fields['Speed']['/V'])
		self.PassWis = 10+self.WisMod




		self.spell0 = [fields['Spells 1014']['/V'],fields['Spells 1016']['/V'],fields['Spells 1017']['/V'],fields['Spells 1018']['/V'],fields['Spells 1019']['/V'],fields['Spells 1020']['/V'],fields['Spells 1021']['/V'],fields['Spells 1022']['/V']]
						#Cantrip0					Cantrip1					Cantrip2					Cantrip3					Cantrip4					Cantrip5					Cantrip6					Cantrip7
		for x in range(0,len(self.spell0)):
			self.spell0[x] = self.spell0[x].strip()
		self.spell1 = []
		self.spell2 = []
		self.spell3 = []
		self.spell4 = []
		self.spell5 = []
		self.spell6 = []
		self.spell7 = []
		self.spell8 = []
		self.spell9 = []
		charsheet.close()

test = char()
print 'Level:', str(test.level)
print 'Proficiency Bonus:', str(test.Prof)
print 'Initiative:', str(test.DexMod)
print 'Armor Class:', str(test.AC)
print 'Strength:', str(test.Str), '(' + str(test.StrMod) + ')'
print 'Dexterity:', str(test.Dex), '(' + str(test.DexMod) + ')'
print 'Constitution:', str(test.Con), '(' + str(test.ConMod) + ')'
print 'Intelligence:', str(test.Int), '(' + str(test.IntMod) + ')'
print 'Wisdom:', str(test.Wis), '(' + str(test.WisMod) + ')'
print 'Charisma:', str(test.Chr), '(' + str(test.ChrMod) + ')'
print 'Speed:', str(test.Speed)
print 'Passive Perception:',test.PassWis
print 'Cantrips:'
for spell in test.spell0:
	print '',spell


