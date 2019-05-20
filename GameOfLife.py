#Two grids represent the game board
# the new generation is built in the grid that is not active.
# But the old state is still there, this is wiped out.
# https://www.youtube.com/watch?v=4_9twnEduFA

import sys, pygame
import random
import time
from datetime import datetime

#To do add dostrings.
#Package as pip package
# TODO add keybinds
# GUI.
# TODO take all of these as constructor arguments.
grid_size = width, height = 400, 400
cell_size = 10
color_dead = 0, 0, 0  # Background
color_alive = 255, 0, 0  # alive cell, can be any color.  #orange = 255, 100, 0 #yellow = 255,255,0, # red=255,0,0 #Green 0,200,0
#fps_max = 10

class GameOfLife:

    def __init__(self):

        #The screen
        pygame.init()
        self.screen = pygame.display.set_mode(grid_size)
        self.clear_screen()  # you clear the screen before it starts running


        pygame.display.flip()
        self.last_update_completed = 0
        #self.desired_milliseconds_between_updates = (1.0 / fps_max) * 1000
        self.active_grid = 0
        self.num_cols = int(width / cell_size)
        self.num_rows = int(height / cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.paused = False
        self.game_over = False




    def init_grids(self):

        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())
        self.active_grid = 0


        #print(self.grids[0])
        #print(rows)
        #print(type(rows))


    #set_grid(0)  = all dead
    #set_grid(1) = all alive
    #set_grid() = random
    #set_grid(None) = random
    def set_grid(self, value=None, grid =0):
       for r in range(self.num_rows):
           for c in range(self.num_cols):
                if value is None:
                    cell_value = random.choice([0,1])
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        self.clear_screen()  # you clear the screen before it starts running
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = color_alive
                else:
                    color = color_dead
                pygame.draw.circle(self.screen,
                                color,
                                (int(c * cell_size + (cell_size/2)),
                                int(r * cell_size + (cell_size/2))),
                                int(cell_size/2), 0)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(color_dead)

    def get_cell(self, r, c):
        try:
            cell_value = self.grids[self.active_grid][r][c]
        except:
            #print("Couldn't get cell value: row: %d, col %d" % (r, c))
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):

        # Get the number of alive cells surrounding the current cell
        # self.grids[self.active_grid][r][c]   #is the current cell
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        #print(num_alive_neighbors)
        #print("alive neighbors: %d")

# Rules
#1 Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#2 Any live cell with two or three live neighbours lives on to the next generation.
#3 Any live cell with more than three live neighbours dies, as if by overpopulation.
#4 Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


        if self.grids[self.active_grid][row_index][col_index] == 1: #Alive
            if num_alive_neighbors > 3:
                return 0  # it dies of overpopulation # More than three live neighbors, rule number 3.
            if num_alive_neighbors < 2:
                return 0  # it dies of underpopulation = Rule number 1 = fewer than two live neighbors
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:  # If there are 3 or 4 neighbors, and the cell is alive, it stays alive.
                return 1  # Rule number 2. Two or three live neighbours, it continuous to live.
        elif self.grids[self.active_grid][row_index][col_index] == 0: #Dead
            if num_alive_neighbors ==3:
                return 1 #It comes to life.
        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        """
        Inspect current generation state, prepare next generation
        :return:
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r, c)
                #Set inactive grid future cell state
                self.grids[self.inactive_grid()][r][c]  = next_gen_state #if it is zero, than is is 1. if it is 1, it is gonna be 0. Picks the offgrid.
        self.active_grid = self.inactive_grid()


        #inspect the current active generation
        # update the inactive grid to store next generation
        #swap out the active grid
        #self.set_grid(None) #This means that you randomize the grid

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 's':
                    if self.paused:
                        self.paused = False
                        print("unpaused")
                    else:
                        self.paused = True
                        print("paused")
                #Randomizin the grid
                elif event.unicode == 'r':
                    print("randomizing the grid")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid) #randomizing
                    self.set_grid(0,self.inactive_grid()) #set to 0.
                    self.draw_grid() #Even if it is paused.
                # Quitfunction
                elif event.unicode == 'q':
                    print("Quitting the grid")
                    self.game_over = True


                # print(event.unicode)
                # print("Key pressed")
                # print(event.unicode)



            # if event is keypress of "s" then pause the loop/game.
            #if event is keypress "r" then randomize grid
            # if event is keypress of "q"then quit
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            if self.game_over:
                return #So if it is game_over by pressing Q, you leave the loop.
            self.handle_events()  # when you run, you want to handle the events
            if self.paused:
                continue
            self.update_generation()  # Upgrade the generation
            self.draw_grid()  # and draw the grid
            #time.sleep(1)
            #self.cap_frame_rate()

"""" 
    def cap_frame_rate(self):
        now = pygame.time.get_ticks() #0 may also work.
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        print(time_to_sleep)
        if time_to_sleep > 1:  #Or True
            pygame.time.delay(int(time_to_sleep))
            self.last_update_completed = now

"""



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
