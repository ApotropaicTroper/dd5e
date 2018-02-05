import Tkinter as tk

class dragManager(object):

	mouseX = 0
	mouseY = 0	#position at which the widget was grabbed. Updates as it gets dragged around
	dragWidget = None #grabbed widget
	dragFrame = None #container for widget

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

	#get widget, get type of widget. Return a copy of the widget
	#can't pass config() to dragWIdget.config(); error with too many of the parameters
	@classmethod
	def copyWidget(cls,widget):
		copyAttrib = {key:widget[key] for key in {'bd','bg','fg','font','height','width','text'}}
		print copyAttrib
		cls.dragWidget = tk.LabelFrame(cls.dragFrame)
		cls.dragWidget.config(copyAttrib)


#widget bound to <ButtonPress-1> event calls this method.
#create a window at cursor position, identical to grabbed widget.
#Bind this to <B1-Motion> event to call onDrag(), <ButtonRelease-1> event to call onDrop() 
#changing parent of a widget isn't possible, so make a copy of it
	@classmethod
	def onGrab(cls,event):
		'''Grab a widget to drag'''
		cls.dragFrame = tk.Toplevel()

		cls.copyWidget(event.widget)
#		print cls.dragCopy['text']
#		print 'DragFrame:',cls.dragFrame,'\nDragCopy:',cls.dragCopy
		cls.dragWidget.grid(in_=cls.dragFrame)
		cls.dragFrame.grid()
#		dragCopy.grid(in_=dragFrame)
#		print event.widget.config()
#		print 'Grabbed at',event.x,event.y

#method for setting a widget as draggable?
	@classmethod
	def canDrag(cls,widget):
		'''set a given widget to be grabbable'''
		widget.bind('<ButtonPress-1>',lambda e: dragManager.onGrab(e))


#print draggable.onGrab()