import tkinter as tk

class draggable():

	mouseX = 0
	mouseY = 0	#position at which the widget was grabbed. Updates as it gets dragged around
	dragWidget = None #grabbed widget



#widget bound to <ButtonPress-1> event calls this method.
#create a window at cursor position identical to grabbed widget.
#Bind this to <B1-Motion> event to call onDrag(), <ButtonRelease-1> event to call onDrop() 
	def onGrab():
		'''Grab a widget to drag'''
		pass

#Move window to mouse position (or the same amount as the mouse moved)
	def onDrag():
		'''Move grabbed widget'''
		pass

#Remove window, do something with the widget under it
	def onDrop():
		'''Release grabbed widget'''
		pass
