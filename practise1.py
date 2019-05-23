import os
import pygame
import tkinter as tk
import platform

# Defining the grid dimensions.
GRID_SIZE = width, height = 500, 500
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

class GameOfLife:
    def __init__(self):
        # Starting pygame
        pygame.init()
        pygame.display.set_caption("Game of Life - Created by Fabio Melis")  # Gives a title to the window
        self.screen = pygame.display.set_mode(GRID_SIZE)  # Create the window with the GRID_SIZE.



        #main window
        self.root = tk.Tk()
        self.root.title("Main window title") #title
        #Create a frame
        self.frame = tk.Frame(self.root, width=1000, height=1000, highlightbackground='red', highlightthickness=10) #Main frame
        # menu for buttons
        self.menu = tk.Frame(self.frame, width=100, height=100, highlightbackground='#595959', highlightthickness=10)
        # space for pygame
        self.game_border = tk.Frame(self.frame, width=500, height=500, highlightbackground='green', highlightthickness=10)

        # Packing them into the window
        self.frame.pack(expand=True)
        self.frame.pack_propagate(0)
        self.menu.pack(side="left")
        self.menu.pack_propagate(0)
        self.game_border.pack(side="bottom")

        #This embeds the pygame window in the pygame frame.
        os.environ['SDL_WINDOWID'] = str(self.game_border.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'



        #Clock to set the FPS
        self.clock = pygame.time.Clock()

    # Initializing all the cells.
    def init_gen(self, generation, c):
        for y in range(self.Y_CELLS):
            for x in range(self.X_CELLS):
                self.generation[x][y] = c
        # Initialise the generations
        self.initGeneration(current_generation, COLOR_DEAD)

        # Two lists, one for the current generation, and one for the next generation, so you can have iterations.
        self.current_generation = [[COLOR_DEAD for y in range(ycells)] for x in range(xcells)]
        self.next_generation    = [[COLOR_DEAD for y in range(ycells)] for x in range(xcells)]

        self.root.mainloop()

    # Drawing the cells, color black or blue at location x/y.
    def draw_cell(self, x, y, c):
        pos = (int(x * CELL_SIZE + CELL_SIZE / 2),
               int(y * CELL_SIZE + CELL_SIZE / 2))
        # pygame.draw.rect(screen, colors[c], pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        # pygame.draw.circle(screen, colors[c], pos, CELL_SIZE, CELL_SIZE) #Weird form, can also be used instead of rectangles
        pygame.draw.circle(screen, colors[c], pos, 5,0)  # Use the last two arguments (radius, width) to change the look of the circles.

    # Updating the cells.
    def update_gen(self):
        global current_generation
        for y in range(self.Y_CELLS):
            for x in range(self.X_CELLS):
                c = next_generation[x][y]
                draw_cell(x, y, c)
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
        if (x >= self.X_CELLS) or (y >= self.Y_CELLS): return 0
        if current_generation[x][y] == COLOR_ALIVE:
            return 1
        else:
            return 0

    def check_cell_neighbors(self, row_index, col_index):
        # Get the number of alive cells surrounding the current cell
        # self.grids[self.active_grid][r][c]   #is the current cell
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
        for y in range(self.Y_CELLS):
            for x in range(self.X_CELLS):
                # If cell is live, count neighboring live cells
                n = check_cell_neighbors(x, y)  # number of neighbors
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

    # Initialise variables


    # Runs the game loop
    def handle_events(self):
        self.next_iteration = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = True  # If pressing the quit button, it closes the window.
            if event.type == pygame.MOUSEBUTTONDOWN:  # if pressing the mouse button, it gets the position. If the cell is dead, make it alive, if the cell is alive, make it dead.
                posn = pygame.mouse.get_pos()
                x = int(posn[0] / CELL_SIZE)
                y = int(posn[1] / CELL_SIZE)
                if next_generation[x][y] == COLOR_DEAD:
                    activate_living_cell(x, y)
                else:
                    deactivate_living_cell(x, y)
            # Check for q, g, s or w keys
            if event.type == pygame.KEYDOWN:  # keydown --> quits when the button goes down. keyup --> quits when the button goes up again.
                if event.unicode == 'q':  # Press q to quit.
                    ended = True
                elif event.key == pygame.K_SPACE:  # Space for the next iteration manually.
                    create_next_gen()
                elif event.unicode == 'a':  # a to automate the iterations.
                    next_iteration = True
                elif event.unicode == 's':  # s to stop the automated iterations.
                    next_iteration = False
                elif event.unicode == 'r':  # r to reset the grid.
                    next_iteration = False
                    init_gen(next_generation, COLOR_DEAD)


    def run(self):
        ended = False
        while not ended:
            self.handle_events()
            if next_iteration:  # if next iteration is true, the next gen is created according to the rules.
                create_next_gen()

        # Updating
        self.update_gen()
        # Updates the content of the entire display.
        pygame.display.flip()
        # Set the frames per second.
        self.clock.tick(10)

if __name__ == "__main__":
    game = GameOfLife()
    game.run()
screen = GameOfLife()
tk.mainloop()








