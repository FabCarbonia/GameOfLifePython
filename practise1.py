# CLass with tkinter, not working.
import os
import pygame
import tkinter as tk
import platform
import random

# Defining the grid dimensions.
GRID_SIZE = width, height = 750, 1000
# Defining the size of the cells, and how many cells there are in the x and y direction.
CELL_SIZE = 10
X_CELLS = int(width/CELL_SIZE)
Y_CELLS = int(height/CELL_SIZE)

#  Defining a color for dead cells (background) and alive cells.
COLOR_DEAD = 0 #background
COLOR_ALIVE = 1 #alive_cell
colors = []
colors.append((  0,   0,   0)) #Black
colors.append((0, 128, 128)) #blue

# Two lists, one for the current generation, and one for the next generation, so you can have iterations.
current_generation = [[COLOR_DEAD for y in range(Y_CELLS)] for x in range(X_CELLS)]
next_generation = [[COLOR_DEAD for y in range(Y_CELLS)] for x in range(X_CELLS)]

#Set the max FPS
fps_max = 10

class GameOfLife:
    def __init__(self):
        # Clock to set the FPS
        self.FPSCLOCK = pygame.time.Clock()
        # Setting variables for later use
        self.next_iteration = False
        self.game_over = False

        # main window
        self.root = tk.Tk()
        self.root.title("Main window title") #title
        # Create a frame
        self.frame = tk.Frame(self.root, width=1000, height=1000, highlightbackground='red') #Main frame
        # menu for buttons
        self.menu = tk.Frame(self.frame, width=250, height=1000, highlightbackground='#595959', highlightthickness=10)
        # space for pygame
        self.game_border = tk.Frame(self.frame, width=750, height=1000, highlightbackground='green', highlightthickness=10)

        # Buttons
        self.button_start = tk.Button(self.menu, text="Start", height=5 , width=20 , fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.start_button)
        self.button_stop = tk.Button(self.menu, text="Stop", height=5 , width=20 , fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.stop_button)
        self.button_iteration = tk.Button(self.menu, text="Next iteration",  height=5 , width=20 , fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.create_next_gen)
        self.button_random = tk.Button(self.menu, text="Random", height=5, width=20, fg="black", activeforeground="red",background="grey80", activebackground="grey80", command=self.set_grid)
        self.button_reset = tk.Button(self.menu, text="Reset",  height=5 , width=20 , fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.reset_button)
        self.button_quit = tk.Button(self.menu, text="Quit",  height=5 , width=20 , fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.quit_button)

        #Sliders
        self.slider_random = tk.Scale(self.menu, from_=0, to=100, orient="horizontal")



        # Packing the buttons
        self.button_start.pack()
        self.button_stop.pack()
        self.button_iteration.pack()
        self.button_random.pack()
        self.button_reset.pack()
        self.button_quit.pack()

        # Packing the sliders
        self.slider_random.pack()

        # Placing the buttons
        self.button_start.place(x=40, y=50)
        self.button_stop.place(x=40, y=200)
        self.button_iteration.place(x=40, y=350)
        self.button_random.place(x=40, y=500)
        self.button_reset.place(x=40, y=650)
        self.button_quit.place(x=40, y=800)

        # Placing the slicers
        self.slider_random.place(x=62, y=590)

        # Packing the windows
        self.frame.pack(expand=True)
        self.frame.pack_propagate(0)
        self.menu.pack(side="left")
        self.menu.pack_propagate(0)
        self.game_border.pack()

        # This embeds the pygame window in the pygame frame.
        os.environ['SDL_WINDOWID'] = str(self.game_border.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        # Starting pygame
        pygame.init()
        pygame.display.set_caption("Game of Life - Created by ")  # Gives a title to the window
        self.screen = pygame.display.set_mode(GRID_SIZE)  # Create the window with the GRID_SIZE.


        # Initialise the generations
        self.init_gen(current_generation, COLOR_DEAD)


    # Button functions
    def start_button(self):
        self.next_iteration = True
    def stop_button(self):
        self.next_iteration = False
    def reset_button(self):
        self.next_iteration = False
        self.init_gen(next_generation, COLOR_DEAD)
    def quit_button(self):
        self.game_over = True

    # Initializing all the cells.
    def init_gen(self, generation, c):
        for y in range(Y_CELLS):
            for x in range(X_CELLS):
                generation[x][y] = c

    def set_grid(self, value=None, grid=0):
        for r in range(X_CELLS):
            for c in range(Y_CELLS):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                    next_generation[grid][r][c] = cell_value


    def set_grid(self):
        self.next_iteration = False
        self.init_gen(next_generation, COLOR_DEAD)
        self.total_cells = X_CELLS * Y_CELLS
        print(self.total_cells)
        for row in range(X_CELLS):
            for col in range(Y_CELLS):
                next_generation[row][col] = random.choice([0,0,0,0,0,0,0,0,0,1]) #10% : [0,0,0,0,0,0,0,0,0,1]  #25%[0,0,0,1]

    # Drawing the cells, color black or blue at location x/y.
    def draw_cell(self, x, y, c):
        pos = (int(x * CELL_SIZE + CELL_SIZE / 2),
               int(y * CELL_SIZE + CELL_SIZE / 2))
        # pygame.draw.rect(screen, colors[c], pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        # pygame.draw.circle(screen, colors[c], pos, CELL_SIZE, CELL_SIZE) #Weird form, can also be used instead of rectangles
        pygame.draw.circle(self.screen, colors[c], pos, 5,0)  # Use the last two arguments (radius, width) to change the look of the circles.

    # Updating the cells.
    def update_gen(self):
        global current_generation
        for y in range(Y_CELLS):
            for x in range(X_CELLS):
                c = next_generation[x][y]
                self.draw_cell(x, y, c)
        # Update current_generation
        current_generation = list(next_generation)

    # Activate a living cell
    def activate_living_cell(self, x, y):
        global next_generation
        next_generation[x][y] = COLOR_ALIVE

    # Deactivate a living cell
    def deactivate_living_cell(self, x, y):
        global next_generation
        next_generation[x][y] = COLOR_DEAD

    # Function to check neighbor cell
    def check_cells(self, x, y):
        # Ignoring cells off the edge
        if (x < 0) or (y < 0): return 0
        if (x >= X_CELLS) or (y >= Y_CELLS): return 0
        if current_generation[x][y] == COLOR_ALIVE:
            return 1
        else:
            return 0

    def check_cell_neighbors(self, row_index, col_index):
        # Get the number of alive cells surrounding the current cell
        num_alive_neighbors = 0
        num_alive_neighbors += self.check_cells(row_index - 1, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index - 1, col_index)
        num_alive_neighbors += self.check_cells(row_index - 1, col_index + 1)
        num_alive_neighbors += self.check_cells(row_index, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index, col_index + 1)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index + 1)
        return num_alive_neighbors

    # Rules
    # 1 Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    # 2 Any live cell with two or three live neighbors lives on to the next generation.
    # 3 Any live cell with more than three live neighbors dies, as if by overpopulation.
    # 4 Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    def create_next_gen(self):
        for y in range(Y_CELLS):
            for x in range(X_CELLS):
                # If cell is live, count neighboring live cells
                n = self.check_cell_neighbors(x, y)  # number of neighbors
                c = current_generation[x][y]  # current cell (either dead or alive).
                if c == COLOR_ALIVE:  # If the cell is living:
                    if (n < 2):  # Rule number 1, underpopulation
                        next_generation[x][y] = COLOR_DEAD
                    elif (n > 3):  # Rule number 3, overpopulation
                        next_generation[x][y] = COLOR_DEAD
                    else:  # Rule number 3, 2 or 3 neighbors, staying alive.
                        next_generation[x][y] = COLOR_ALIVE
                else:  # if the cell is dead:
                    if (n == 3):
                        # Rule number 4: A dead cell with three living neighbors becomes alive.
                        next_generation[x][y] = COLOR_ALIVE

    # Runs the game loop
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True  # If pressing the quit button, it closes the window.
            if event.type == pygame.MOUSEBUTTONDOWN:  # if pressing the mouse button, it gets the position. If the cell is dead, make it alive, if the cell is alive, make it dead.
                posn = pygame.mouse.get_pos()
                x = int(posn[0] / CELL_SIZE)
                y = int(posn[1] / CELL_SIZE)
                if next_generation[x][y] == COLOR_DEAD:
                    self.activate_living_cell(x, y)
                else:
                    self.deactivate_living_cell(x, y)
            # Check for q, g, s or w keys
            if event.type == pygame.KEYDOWN:  # keydown --> quits when the button goes down. keyup --> quits when the button goes up again.
                if event.unicode == 'q':  # Press q to quit.
                    self.game_over = True
                    print("q")

                elif event.key == pygame.K_SPACE:  # Space for the next iteration manually.
                    self.create_next_gen()
                    print("keypress")
                elif event.unicode == 'a':  # a to automate the iterations.
                    self.next_iteration = True
                    print("a")
                elif event.unicode == 's':  # s to stop the automated iterations.
                    self.next_iteration = False
                    print("s")
                elif event.unicode == 'r':  # r to reset the grid.
                    self.next_iteration = False
                    self.init_gen(next_generation, COLOR_DEAD)
                    print("r")

    def run(self):
        while not self.game_over:
            # Set the frames per second.
            self.handle_events()
            if self.next_iteration:  # if next iteration is true, the next gen is created according to the rules.
                self.create_next_gen()
            # Updating
            self.update_gen()
            pygame.display.flip()
            self.FPSCLOCK.tick(fps_max)
            self.root.update()

if __name__ == "__main__":
    game = GameOfLife()
    game.run()







