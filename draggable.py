import Tkinter as tk

class dragManager(object):

	mouseX = 0
	mouseY = 0	#position at which the widget was grabbed. Updates as it gets dragged around
	dragWidget = None #grabbed widget



#Remove window, do something with the widget under it
	@staticmethod
	def onDrop(event):
		'''Release grabbed widget'''
		pass

#Move window to mouse position (or the same amount as the mouse moved)
	@staticmethod
	def onDrag(event):
		'''Move grabbed widget'''
		pass

#widget bound to <ButtonPress-1> event calls this method.
#create a window at cursor position, identical to grabbed widget.
#Bind this to <B1-Motion> event to call onDrag(), <ButtonRelease-1> event to call onDrop() 
	@staticmethod
	def onGrab(event):
		'''Grab a widget to drag'''
		widgetConfig = event.widget.config()
		dragFrame = tk.Frame(tk.Tk())
		dragFrame.grid()
		event.widget.grid(in_=dragFrame)
		print 'Grabbed at',event.x,event.y

#method for setting a widget as draggable?
	@staticmethod
	def canDrag(widget):
		'''set a given widget to be grabbable'''
		widget.bind('<ButtonPress-1>',lambda e: dragManager.onGrab(e))


#print draggable.onGrab()