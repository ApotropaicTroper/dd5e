import Tkinter as tk

class dragManager(object):

	mouseX = 0 #position in window in which widget was grabbed
	mouseY = 0	
	dragWidget = None #grabbed widget
	dragFrame = None #container for widget

#Remove window, do something with the widget under it
	@classmethod
	def onDrop(cls,event):
		'''Release grabbed widget'''
		print 'Release'

#Move window to mouse position (or the same amount as the mouse moved)
	@classmethod
	def onDrag(cls,event):
		'''Move grabbed widget'''
		print cls.dragFrame.winfo_width(),cls.dragFrame.winfo_height(),cls.dragFrame.winfo_x(),cls.dragFrame.winfo_y()
		cls.dragFrame.geometry('%dx%d%+d%+d' % (cls.dragFrame.winfo_width(),cls.dragFrame.winfo_height(),
												event.x_root,event.y_root))
#												event.x_root-cls.mouseX,event.y_root-cls.mouseY))


	#get widget, get type of widget. Return a copy of the widget
	#can't pass config() to dragWIdget.config(); error with too many of the parameters
	@classmethod
	def copyWidget(cls,widget):

		copyAttrib = {key:widget[key] for key in {'bd','bg','fg','font','height','width','text'}}
		cls.dragWidget = tk.LabelFrame(cls.dragFrame)
		cls.dragWidget.config(copyAttrib)



#create a window at cursor position, identical to grabbed widget.
#Bind this to <B1-Motion> event to call onDrag(), <ButtonRelease-1> event to call onDrop() 
#changing parent of a widget isn't possible, so make a copy of it
	@classmethod
	def onGrab(cls,event):
		'''Grab a widget to drag'''
		cls.dragFrame = tk.Toplevel()
		pointerPos = (event.widget.winfo_pointerx(),event.widget.winfo_pointery())
		cls.copyWidget(event.widget)
		cls.dragWidget.grid(in_=cls.dragFrame)
		cls.dragFrame.geometry('%dx%d%+d%+d' % (cls.dragWidget.winfo_reqwidth(),cls.dragWidget.winfo_reqheight(),
													event.widget.winfo_pointerx(),event.widget.winfo_pointery()))
		cls.mouseX = event.x
		cls.mouseY = event.y
		cls.dragFrame.overrideredirect(1)
		cls.dragFrame.grid()
		cls.dragFrame.bind('<B1-Motion>', lambda e: cls.onDrag(e))
		cls.dragFrame.bind('<B1-Leave>', lambda e: cls.onDrag(e))
		cls.dragFrame.bind('<ButtonRelease-1>', lambda e: cls.onDrop(e))


#method for setting a widget as draggable?
	@classmethod
	def canDrag(cls,widget):
		'''set a given widget to be grabbable'''
		widget.bind('<ButtonPress-1>', lambda e: cls.onGrab(e))


#print draggable.onGrab()