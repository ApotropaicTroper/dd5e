import glob
import PyPDF2
char = 'Jebeddo the Green'
files = glob.glob('C:\\Users\\Jethro\\Desktop\\*.pdf')
charsheet = -1
for file in files:
	if char in file:
		charsheet = PyPDF2.PdfFileReader(open(file,'rb')).getPage(2)
		print charsheet.extractText()
#		charsheet.close()
