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
			if 'Check Box' in key or 'Spells' in key or 'ST ' in key:
				continue
			print key
			print fields[key]
			for key2 in fields[key].keys():
				print '    ', key
				print '        ', fields[key][key2]
		self.level = int(fields['ClassLevel']['/V'].split(' ')[-1])

		self.Prof = (self.level-1)/4 + 2
#		print fields['CHamod']['/V']
	
		charsheet.close()
#		print 'Initialized'

test = char()
print 'Level: ' + str(test.level)
print 'Proficiency Bonus: ' + str(test.Prof)