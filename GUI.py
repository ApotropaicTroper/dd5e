
'''
Support for drag & drop?
Track left button down, button hold/motion, button release
<Button-1> (or <ButtonPress-1> or <1>
 remove object from its section?
<B1-Motion>
 set coordinates to that of mouse
<ButtonRelease-1>
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
from draggable import dragManager as drag

#class Menu(tk.Frame):

root = tk.Tk()
slots = []
listing = 0

def boop(self):
	'''Placeholder, so the buttons do something'''
	print 'boop'

def react(event):
	print event.x, event.y
#def doSomething(self):
#	print self.listing.curselection()

def color(num):
	return '#00bf00'

#drag.onGrab()


def fidgetWidget(master=None):

	obj1 = tk.LabelFrame(text='left',height=100,width=100,bg='#df0000')
	drag.canDrag(obj1)
	obj1.grid(row=0,column=0)

	obj2 = tk.LabelFrame(text='right',height=100,width=100,bg='#0000df')
	drag.canDrag(obj2)
	obj2.grid(row=0,column=1)

#	print obj1.winfo_class()
#	test = tk.LabelFrame(text='test',height=50,width=50)
#	drag.canDrag(test)
#	test.grid(in_=obj1)
#	test.grid(in_=obj2)


	'''
	dropWidgetHeight=50
	dropWidgetWidth=50

	for level in range(0,10):
		slots.append(tk.LabelFrame(text=str(level),height=dropWidgetHeight,width=dropWidgetWidth))
		slots[level].grid(row=level)
		slots[level].bind('<ButtonPress-1>',onGrab)

	listing = tk.Listbox(self)
	listing.insert(tk.END,'testing')
	listing.insert(tk.END,'testing')
	listing.insert(1,'1')
	listing.insert(2,'2')
	listing.insert(3,'3')
	listing.delete(0)
	listing.grid(row=20,columnspan=2)

	self.CardSpace = tk.Frame(self)
	self.DropOptions = tk.Frame(self)
	self.BottomOptions = tk.Frame(self)
	self.CardSpace.grid(row=1,column=1)
	self.DropOptions.grid(row=1,column=0)
	self.BottomOptions.grid(row=2,columnspan=2)

	cardsWidth=125
	cardsHeight=75
 	self.Card = tk.Canvas(self,height=7*cardsHeight,width=5*cardsWidth,bg='#ffffff')
 	self.Card.create_text((5,5),text='Drag stuff from this area. Things are 7 high by 5 wide.',anchor=tk.NW)

	self.Card.bind('<Button-1>',self.react)
	self.Card.grid(in_=self.CardSpace,rowspan=19,column=4)

	self.Compendium = tk.Button(self, text='Compendium',height=2,width=12)
	self.loadList = tk.Button(self, text='Load',command=self.boop,height=2, width=5)
	self.Compendium.grid(in_=self.BottomOptions,row=0,column=0)
	self.loadList.grid(in_=self.BottomOptions,row=0,column=1)
	'''
	QUIT = tk.Button(text='quit',command=quit,height=2,width=5)
	QUIT.grid(row=0,column=2)



#	def __init__(self, master=None):
#		main = tk.Frame.__init__(self,master)
#		tk.Frame.__init__(self,master)
#		self.overridedirect(1)
#		self.grid()
#		self.fidgetWidget()


masterFrame = tk.Frame(root)
#root.overrideredirect(1)
fidgetWidget(root)
masterFrame.mainloop()
#frame = tk.Frame(root)
#frame.pack()
#bottomframe = tk.Frame(root)
#bottomframe.pack(side='bottom')
#menu = Menu(master=root)
#menu.mainloop()

