

import Tkinter as tk

class Menu(tk.Frame):
	def boop(self):
		print 'boop'

	def fidgetWidget(self):
		self.menu = tk.Canvas(self,height=256+128,width=256+128,bg='#ffffff')
		self.menu.create_text(5,5,text='Text',anchor=tk.NW)
		self.menu.grid(rowspan=19,column=4)
#		self.Cantrip = tk.Button(self, text='Cantrip', command=self.boop, height='2',width='32',bg='#ffffff',fg='#000000')
		self.Level1 = tk.Button(self, text='1', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level2 = tk.Button(self, text='2', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level3 = tk.Button(self, text='3', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level4 = tk.Button(self, text='4', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level5 = tk.Button(self, text='5', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level6 = tk.Button(self, text='6', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level7 = tk.Button(self, text='7', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level8 = tk.Button(self, text='8', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.Level9 = tk.Button(self, text='9', command=self.boop, height='2',width='10',bg='#ffffff',fg='#000000')
		self.QUIT = tk.Button(self, text='QUIT', fg='blue', command=self.quit,height='2',width='20')

#		self.Cantrip.grid(row=0,columnspan=3,ipadx=7,pady=2)
		self.Level1.grid(row=1,rowspan=2,column=0,pady=2,padx=2)
		self.Level2.grid(row=3,rowspan=2,column=0,pady=2,padx=2)
		self.Level3.grid(row=5,rowspan=2,column=0,pady=2,padx=2)
		self.Level4.grid(row=7,rowspan=2,column=0,pady=2,padx=2)
		self.Level5.grid(row=9,rowspan=2,column=0,pady=2,padx=2)
		self.Level6.grid(row=11,rowspan=2,column=0,pady=2,padx=2)
		self.Level7.grid(row=13,rowspan=2,column=0,pady=2,padx=2)
		self.Level8.grid(row=15,rowspan=2,column=0,pady=2,padx=2)
		self.Level9.grid(row=17,rowspan=2,column=0,pady=2,padx=2)
		self.QUIT.grid(row=19,ipadx=7)



	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.fidgetWidget()

root = tk.Tk()
menu = Menu(master=root)
menu.mainloop()
root.destroy()