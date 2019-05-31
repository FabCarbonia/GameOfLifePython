import sys, pygame
import random
import time

grid_size = width, height = 700, 400
cell_size = 10
color_dead = 0, 0, 0 #Background
color_alive = 0, 255, 255 #alive cell, can be any color.

class GameOfLife:

    def __init__(self):
        #The screen
        pygame.init()
        self.screen = pygame.display.set_mode(grid_size)
        self.clear_screen()  # you clear the screen before it starts running
        pygame.display.flip()

        self.init_grids()

    def init_grids(self):
        self.num_cols = int(width / cell_size)
        self.num_rows = int(height / cell_size)
        #self.grids = [[[0] * self.num_rows]*self.num_cols,
        #             [[0] * self.num_rows]*self.num_cols]

        self.grids = []

        rows = []
        for row_num in range(self.num_rows):
            list_of_columns = [0] * self.num_cols
            rows.append(list_of_columns)


        print(rows)
        print(type(rows))
        self.grids.append(rows)

        self.active_grid = 0

        self.set_grid()
        print(self.grids[0])



#set_grid(0)  = all dead
    #set_grid(1) = all alive
    #set_grid() = random
    #set_grid(None) = random
    def set_grid(self, value=None):
       for r in range(self.num_rows):
           for c in range(self.num_cols):
               self.grids[self.active_grid][r][c] = random.choice([0,1])
  #              if value is None:
  #                  cell_value = random.choice([0,1])
  #              else:
  #                  cell_value = value
  #              self.grids[self.active_grid][c][r] = cell_value

    def draw_grid(self):
        self.clear_screen()  # you clear the screen before it starts running
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = color_alive
                else:
                    color = color_dead
                pygame.draw.circle(self.screen, color, (int(c * cell_size + (cell_size/2)),
                                                              int(r * cell_size + (cell_size/2))), int(cell_size/2), 0)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(color_dead)

    def update_generation(self):
        #inspect the current active generation
        # update the inactive grid to store next generation
        #swap out the active grid
        #self.set_grid(None) #This means that you randomize the grid
        self.set_grid()

    def handle_events(self):
        for event in pygame.event.get():
            # if event is keypress of "s" then pause the loop/game.
            #if event is keypress "r" then randomize grid
            # if event is keypress of "q"then quit
            if event.type == pygame.QUIT:
                    sys.exit()

    def run(self):
        while True:
            self.handle_events()  # when you run, you want to handle the events
            self.update_generation()  # Upgrade the generation
            self.draw_grid()  # and draw the grid
            time.sleep(1)

if __name__ == "__main__":
    game = GameOfLife()
    game.run()

'''

#https://gist.github.com/bennuttall/6952575
#pygame for the game of life.
#django for website.


#import pygame #Doesn't work now...
# https://www.youtube.com/watch?v=i6xMBig-pP4
from tkinter import *


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
frame = Frame(root, width=500, height=500)
frame.pack()

#topFrame = Frame(root)
#topFrame.pack()

#Code to run sliders.
w = Scale(root, from_=0, to=100, orient=HORIZONTAL)
w.pack()
w = Scale(root, from_=0, to=100, orient=HORIZONTAL)
w.pack()


b = classname(root)
root.mainloop()
'''

"""
#Gives a multiple choice
v = IntVar()
Radiobutton(root, text='GfG', variable=v, value=1).pack(anchor=W)
Radiobutton(root, text='MIT', variable=v, value=2).pack(anchor=W)
"""
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
