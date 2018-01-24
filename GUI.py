
'''
End goal: D&D spell manager
'''



import Tkinter as tk

class Menu(tk.Frame):
	def boop(self):
		'''Placeholder, so the buttons do something'''
		print 'boop'

	def fidgetWidget(self):
		self.CardSpace = tk.Frame(self)
		self.DropOptions = tk.Frame(self)
		self.BottomOptions = tk.Frame(self)
		self.CardSpace.grid(row=0,column=1)
		self.DropOptions.grid(row=0,column=0)
		self.BottomOptions.grid(row=1,columnspan=2)
		
		self.Cards = tk.Canvas(self,height=384,width=384,bg='#ffffff')
		self.Cards.create_text(5,5,text='Text',anchor=tk.NW)
		self.Cards.grid(in_=self.CardSpace,rowspan=19,column=4)

		self.Level1 = tk.Button(self,text='1', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level2 = tk.Button(self,text='2', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level3 = tk.Button(self,text='3', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level4 = tk.Button(self,text='4', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level5 = tk.Button(self,text='5', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level6 = tk.Button(self,text='6', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level7 = tk.Button(self,text='7', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level8 = tk.Button(self,text='8', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level9 = tk.Button(self,text='9', command=self.boop, height=2,width=15,bg='#ffffff',fg='#000000')
		self.Level1.grid(in_=self.DropOptions,row=1,rowspan=2,column=0,columnspan=2,pady=2,padx=8)
		self.Level2.grid(in_=self.DropOptions,row=3,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level3.grid(in_=self.DropOptions,row=5,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level4.grid(in_=self.DropOptions,row=7,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level5.grid(in_=self.DropOptions,row=9,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level6.grid(in_=self.DropOptions,row=11,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level7.grid(in_=self.DropOptions,row=13,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level8.grid(in_=self.DropOptions,row=15,rowspan=2,column=0,columnspan=2,pady=2,padx=2)
		self.Level9.grid(in_=self.DropOptions,row=17,rowspan=2,column=0,columnspan=2,pady=2,padx=2)

		self.Compendium = tk.Button(self, text='Compendium',command=self.boop,height=2,width=12)
		self.loadList = tk.Button(self, text='Load',command=self.boop,height=2, width=5)
		self.quit = tk.Button(self, text='quit',command=self.quit,height=2,width=5)
		self.Compendium.grid(in_=self.BottomOptions,row=0,column=0)
		self.loadList.grid(in_=self.BottomOptions,row=0,column=1)
		self.quit.grid(in_=self.BottomOptions,row=0,column=2)



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
