
'''
Support for drag & drop?
'''

'''
ff0000 0
ff7f00 1
ffff00 2
00ff00 3
00ff7f 4
00ffff 5
0000ff 6
7f00ff 7
ff00ff 8
'''


import Tkinter as tk

class Menu(tk.Frame):

	slots = []
	listing = 0

	def boop(self):
		'''Placeholder, so the buttons do something'''
		print 'boop'

#	def doSomething(self):
#		print self.listing.curselection()

	def color(self,num):
		return '#00bf00'

	def fidgetWidget(self):
		self.CardSpace = tk.Frame(self)
		self.DropOptions = tk.Frame(self)
		self.BottomOptions = tk.Frame(self)
		self.CardSpace.grid(row=1,column=1)
		self.DropOptions.grid(row=1,column=0)
		self.BottomOptions.grid(row=2,columnspan=2)

		cardsWidth=125
		cardsHeight=75
		self.Cards = tk.Canvas(self,height=7*cardsHeight,width=5*cardsWidth,bg='#ffffff')
		self.Cards.create_text((5,5),text='Drag stuff from this area. Things are 7 high by 5 wide.',anchor=tk.NW)
		self.Cards.grid(in_=self.CardSpace,rowspan=19,column=4)

		dropWidgetHeight=50
		dropWidgetWidth=50
		for level in range(0,10):
			self.slots.append(tk.Canvas(self,height=dropWidgetHeight,width=dropWidgetWidth,bg=self.color(level)))
			self.slots[level].create_text((25,25),text=str(level+1),anchor=tk.CENTER,fill='#000000')
			self.slots[level].grid(in_=self.DropOptions,row=level)
		self.Compendium = tk.Button(self, text='Compendium',height=2,width=12)
		self.loadList = tk.Button(self, text='Load',command=self.boop,height=2, width=5)
		self.quit = tk.Button(self, text='quit',command=self.quit,height=2,width=5)
		self.Compendium.grid(in_=self.BottomOptions,row=0,column=0)
		self.loadList.grid(in_=self.BottomOptions,row=0,column=1)
		self.quit.grid(in_=self.BottomOptions,row=0,column=2)

		listing = tk.Listbox(self)
		listing.insert(tk.END,'testing')
		listing.insert(tk.END,'testing')
		listing.insert(1,'1')
		listing.insert(2,'2')
		listing.insert(3,'3')
		listing.delete(0)
		listing.grid(row=0)



	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.fidgetWidget()


root = tk.Tk()
#frame = tk.Frame(root)
#frame.pack()
#bottomframe = tk.Frame(root)
#bottomframe.pack(side='bottom')
menu = Menu(master=root)
menu.mainloop()

