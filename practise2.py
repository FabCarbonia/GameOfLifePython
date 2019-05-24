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

        #Starting pygame
        pygame.init()
        pygame.display.set_caption("Game of Life - Created by Fabio Melis")  # Gives a title to the window
        self.screen = pygame.display.set_mode(GRID_SIZE)  # Create the window
            # Blank screen
        self.screen.fill(COLOR_ALIVE)
        # Update the full display surface to the screen
       # pygame.display.flip()


        #Clock to set the FPS
        self.clock = pygame.time.Clock()

        # Initializing all the cells.
    def initGeneration(self, generation, c):
        for y in range(ycells):
            for x in range(xcells):
                 generation[x][y] = c
        # Initialise the generations
        self.initGeneration(current_generation, COLOR_DEAD)

        # Two lists, one for the current generation, and one for the next generation, so you can have iterations.
        self.current_generation = [[COLOR_DEAD for y in range(ycells)] for x in range(xcells)]
        self.next_generation    = [[COLOR_DEAD for y in range(ycells)] for x in range(xcells)]

        self.root.mainloop()

    # Define a function to draw a square of color(c) at coordinates, x and y
    def drawCell(self, x, y, c):
        pos = (int(x * cell_size + cell_size / 2 ),
               int(y * cell_size + cell_size / 2))
        #pygame.draw.rect(screen, colors[c], pygame.Rect(x * cell_size, y * cell_size, cell_size-1, cell_size-1))
        # pygame.draw.circle(screen, colors[c], pos, cell_size, cell_size) #Weird form, can also be used instead of rectangles
        pygame.draw.circle(screen, colors[c], pos, cell_size, 0) #Use the last two arguments (radius, width) to change the look of the circles.

    # Define a function to update cells on screen from next_generation array
    def update_generation(self):
        for y in range(ycells):
            for x in range(xcells):
                c = next_generation[x][y]
                drawCell(x, y, c)
        # Update current_generation
        self.current_generation = list(next_generation)

    # Create a Live cell
    def createLiveCell(self,x,y):
        global next_generation
        next_generation[x][y] = COLOR_ALIVE

    # Kill a Live cell
    def killLiveCell(self, x,y):
        global next_generation
        next_generation[x][y] = COLOR_DEAD

    # Function to check neighbour cell
    def checkNeighbour(self, x, y):
        # Ignore cell off the edge of the grid
        if (x < 0) or (y < 0): return 0
        if (x >= xcells) or (y >= ycells): return 0
        # Check if cell is live
        if current_generation[x][y] == COLOR_ALIVE:
            return 1
        else:
            return 0

    def check_cell_neighbors(self, row_index, col_index):
            # Get the number of alive cells surrounding the current cell
            # self.grids[self.active_grid][r][c]   #is the current cell
            num_alive_neighbors = 0
            num_alive_neighbors += checkNeighbour(row_index - 1, col_index - 1)
            num_alive_neighbors += checkNeighbour(row_index - 1, col_index)
            num_alive_neighbors += checkNeighbour(row_index - 1, col_index + 1)
            num_alive_neighbors += checkNeighbour(row_index, col_index - 1)
            num_alive_neighbors += checkNeighbour(row_index, col_index + 1)
            num_alive_neighbors += checkNeighbour(row_index + 1, col_index - 1)
            num_alive_neighbors += checkNeighbour(row_index + 1, col_index)
            num_alive_neighbors += checkNeighbour(row_index + 1, col_index + 1)
            return num_alive_neighbors

    # Define a function to breed the next generation of cells
    def breedNextGeneration(self):
        global next_generation
        for y in range(ycells):
            for x in range(xcells):
                # If cell is live, count neighbouring live cells
                n = check_cell_neighbors(x,y)
                c = current_generation[x][y]
                # If cell is live check rules 1, 2 and 3
                if c == COLOR_ALIVE:
                    if (n < 2) or (n > 3):
                        # Cell dies (rules 1 and 3)
                        next_generation[x][y] = COLOR_DEAD
                    else:
                        # Cell lives on (rule 2)
                        next_generation[x][y] = COLOR_ALIVE
                else:
                    if (n == 3):
                        # Cell is reborn (rule 4)
                        next_generation[x][y] = COLOR_ALIVE

    # Initialise variables
    done = False
    breedCells = False

    # Runs the game loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                # handle Mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posn = pygame.mouse.get_pos()
                    x = int(posn[0] / cell_size)
                    y = int(posn[1] / cell_size)
                    if next_generation[x][y] == COLOR_DEAD:
                        createLiveCell(x, y)
                    else:
                        killLiveCell(x, y)
                # Check for q, g, s or w keys
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:  # Press q to quit.
                        done = True
                    elif event.key == pygame.K_SPACE:  # Press space to go to the next generation
                        breedNextGeneration()
                    elif event.key == pygame.K_g:  # press g to breed cells automatically
                        breedCells = True
                    elif event.key == pygame.K_s:  # press s to stop breading automatically
                        breedCells = False
                    elif event.key == pygame.K_w:  # press w to reset the grid.
                        breedCells = False
                        initGeneration(next_generation, COLOR_DEAD)

        if breedCells:
            breedNextGeneration()

            # Update and draw
        update_generation()

        # Update the full display surface to the screen
        pygame.display.flip()

        # Limit the game to 60 frames per second
        clock.tick(60)


screen = GameOfLife()
tk.mainloop()








