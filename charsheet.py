import sys, glob
import PyPDF2
import codecs

class char:
	level = -99		#Character Level
	AC = -99		#Armor Class
	Prof = -99		#Proficiency Bonus
	Init = -99		#Initiative Bonus
	Speed = -99		#Movement distance per round (ft)
	Str = -99		#Strength
	StrMod = -99	# ^ Modifier
	Dex = -99		#Dexterity
	DexMod = -99	# ^ Modifier
	Con = -99		#Constitution
	ConMod = -99	# ^ Modifier
	Int = -99		#Intelligence
	IntMod = -99	# ^ Modifier
	Wis = -99		#Wisdom
	WisMod = -99	# ^ Modifier
	Chr = -99		#Charisma
	ChrMod = -99	# ^ Modifier
	CastScore = ''	#Which ability score do you use to cast spells?
	CastBonus = -99	#Spell attack rolls get this as a bonus to hit
	CastDC = -99	#Difficulty class for opponents' saving throws against your spells

	def __init__(self, name):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		files = glob.glob('..\\*.pdf')
#		print files
		charsheet = -1
		for file in files:
			if name in file:
				charsheet = open(file, 'rb')
			else:
				continue
		if charsheet == -1:
			raise Exception('File not found!')
		fileReader = PyPDF2.PdfFileReader(charsheet)
		fields = fileReader.getFields()
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
#(Dex) Acrobatics: 		Check Box 23
#(Wis) Animal Handling: Check Box 24
#(Int) Arcana: 			Check Box 25
#(Str) Athletics: 		Check Box 26
#(Cha) Deception: 		Check Box 27
#(Int) History: 		Check Box 28
#(Wis) Insight: 		Check Box 29
#(Cha) Intimidation: 	Check Box 30
#(Int) Investigation: 	Check Box 31
#(Wis) Medicine:		Check Box 32
#(Int) Nature: 			Check Box 33
#(Wis) Perception: 		Check Box 34
#(Cha) Performance: 	Check Box 35
#(Cha) Persuasion: 		Check Box 36
#(Int) Religion:		Check Box 37
#(Dex) Sleight of Hand:	Check Box 38
#(Dex) Stealth:			Check Box 39
#(Wis) Survival:		Check Box 40

		self.CastScore = fields['SpellcastingAbility 2']['/V']
		self.CastBonus = self.Prof + eval('self.' + self.CastScore + 'Mod')
		self.CastDC = 8 + self.CastBonus 


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


#test = char('Jebeddo the Green')
#test.toString()