

from tkinter import *
root = Tk()


root.mainloop()

"""
#Create lines and boxes 
root = Tk()

canvas = Canvas(root, width=200, height=100)
canvas.pack()

blackLine = canvas.create_line(0, 0, 200, 50) #Starting points at 0,0, ending point at 200,50
greenLine = canvas.create_rectangle(25, 25, 130, 60, fill="green") #first parameter is a point, top left. the next two parameters are the bottom right corner.

canvas.delete(ALL) #Removes all the lines again. 

root.mainloop()
"""



"""
#Statusbar
root = Tk()

status = Label(root, text="Statusbar", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
root.mainloop()
"""

"""
#Toolbar
root = Tk()
toolbar = Frame(root, bg="blue")
insertButt = Button(toolbar, text="insert image")
insertButt.pack(side=LEFT, padx=2, pady=2)
printButt = Button(toolbar, text="print")
printButt.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X) #fills in the X direction.

root.mainloop()
"""

"""
#Menu's
def doNothing():
    print("saved")

root = Tk()
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu) #Creates a file button, dropdown functionallity, menu is the submenu that is in the dropdown
subMenu.add_command(label="Save", command=doNothing) # name in the dropdown, and the command to go with it.
subMenu.add_command(label="Save1", command=doNothing) # name in the dropdown, and the command to go with it.
subMenu.add_separator()
subMenu.add_command(label="exit", command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label="file2", menu=editMenu)

root.mainloop()
"""


"""
#QUIT button to terminate the screen. 
class classname:

    def __init__(self, master):
        frame = Frame(master) #master = main window instead of root
        frame.pack()

        self.printButton = Button(frame, text="print something", command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=master.destroy) #Command that quits, breaks, the main loop. closing the window.
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("printsomethingontheleftside")


root = Tk()
b = classname(root)
root.mainloop()
"""

"""
#prints right, left, or middle depending on the mouse click.
root = Tk()

def printName():
    print("Hello my name is Fabio")

def leftClick(event):
    print("left")
def rightClick(event):
    print("right")
def middleClick(event):
    print("middle")

frame = Frame(root, width=1000, height=1000)
frame.bind("<Button-1>", leftClick) #leftclick on the mouse
frame.bind("<Button-2>", middleClick) #scrollwheel on your mouse
frame.bind("<Button-3>", rightClick) #rightclick on the mouse

frame.pack()


#button_1 = Button(root, text="print my name", command = printName)
#button_1.pack()


root.mainloop()
"""

'''
#password
root = Tk()

label_1 = Label(root, text="Username")
label_2 = Label(root, text="Password")
entry_1 = Entry(root) #gives a blank field
entry_2 = Entry(root)

label_1.grid(row=0, column=0, sticky=E)  #sticky moves the location, E = east. Right align.
label_2.grid(row=1, column=0, sticky=E)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

c = Checkbutton(root, text="keepmeloggedin")

c.grid(columnspan=2)


root.mainloop()
'''

"""
#root = Tk() #blank window
#label = Label(root, text="this is too easy")
#label.pack()
#root.mainloop() #loops the window, so it stays open.

#Default pack() is on top. you can specify a location: side=left e.g.

root = Tk() #blank window
topFrame = Frame(root)
topFrame.pack(side=TOP) #Pack displays it in the window
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)


button1 = Button(topFrame, text="click me, button 1", fg="red")
button2 = Button(topFrame, text="click me, button 2", fg="blue")
button3 = Button(topFrame, text="click me, button 3", fg="green")
button4 = Button(bottomFrame, text="click me, button 4", fg="yellow")

button1.pack(side="left")
button2.pack(side="left")
button3.pack(side="left")
button4.pack()

label = Label(root, text="Hi Noortje", bg="yellow", fg="red")
label.pack(fill=X)


root.mainloop() #loops the window, so it stays open.
"""
