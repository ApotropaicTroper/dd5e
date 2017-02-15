import sys, glob
import PyPDF2
reload(sys)
sys.setdefaultencoding('utf-8')

char = 'Jebeddo the Green'
files = glob.glob('C:\\Users\\Jethro\\Desktop\\*.pdf')
charsheet = -1

for file in files:
	if char in file:
		charsheet = open(file, 'rb')
		fileReader = PyPDF2.PdfFileReader(charsheet)
		headers = fileReader.getFormTextFields()
		for head in headers:
			print head
		print '>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<'
		fields = fileReader.getFields()

		for key in fields.keys():
			print key
			print '    ', fields[key]

		charsheet.close()