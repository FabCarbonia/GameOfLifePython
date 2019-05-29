#To do:
#Create a button that counts the living and dead cells.
# SLider for the grid size.
# Increase the speed of the drawing
#If slider = 100, all the cells are activated. This means = overpopulation, so everything should die. This does not happen. Fix this.
#Explain that the qsa space buttons can be used as well.
# Square or circles button. ANd color button.
# Python ruies
# add a dropdown file menu with an instruction button.
# Limit all lines to 72 characters.
# Neighbors 1 row/col further from the cell.
# Create a package, so that other people can use it.
# Explain the keyboard presses.
# Iteration counter.
# Packing not needed if placed.

import tkinter as tk
import itertools, os, platform, pygame, random

# Defining the grid dimensions.
GRID_SIZE = WIDTH, HEIGHT = 750, 1000

# Defining the cell size and the number of cells in the X and Y direction.
CELL_SIZE = 10
X_CELLS = int(WIDTH/CELL_SIZE)
Y_CELLS = int(HEIGHT/CELL_SIZE)

# Defining the number and color for dead and living cells.
COLOR_DEAD = 0
COLOR_ALIVE = 1
colors = []
colors.append((0, 0, 0))  # Black
colors.append((0, 128, 128))  # blue

# Defining two lists: current generation and next generation.
current_generation = [[COLOR_DEAD for y in range(Y_CELLS)] for x in range(X_CELLS)]
next_generation = [[COLOR_DEAD for y in range(Y_CELLS)] for x in range(X_CELLS)]

# Defining the max frames per second/speed of the game.
FPS_MAX = 10

class GameOfLife:
    """
    describe what the method does.
    """
    def __init__(self):
        # Initializing the interpreter and creating a root window and title.
        self.root = tk.Tk()
        self.root.title("Game of Life - Created by Fabio Melis - Have fun")
        # Defining the main frame, left-side frame and right-side frame.
        self.frame = tk.Frame(self.root , width=1000, height=1000, highlightbackground='red')
        self.menu = tk.Frame(self.frame, width=250, height=1000, highlightbackground='#595959', highlightthickness=10)
        self.game_border = tk.Frame(self.frame, width=750, height=1000, highlightbackground='green', highlightthickness=10)
        # Packing the windows.
        self.frame.pack()
        self.frame.pack_propagate(0)
        self.menu.pack(side="left")
        self.menu.pack_propagate(0)
        self.game_border.pack()

        # Defining the buttons.
        self.button_start = tk.Button(self.menu, text="Start", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.start_button)
        self.button_stop = tk.Button(self.menu, text="Stop", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.stop_button)
        self.button_iteration = tk.Button(self.menu, text="Next iteration", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.create_next_gen)
        self.button_random = tk.Button(self.menu, text="Random", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.random_grid)
        self.button_reset = tk.Button(self.menu, text="Reset", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.reset_button)
        self.button_quit = tk.Button(self.menu, text="Quit", height=5, width=20, fg="black", activeforeground="red", background="grey80", activebackground="grey80", command=self.quit_button)
        # Packing the buttons.
        self.button_start.pack()
        self.button_stop.pack()
        self.button_iteration.pack()
        self.button_random.pack()
        self.button_reset.pack()
        self.button_quit.pack()
        # Placing the buttons.
        self.button_start.place(x=40, y=50)
        self.button_stop.place(x=40, y=200)
        self.button_iteration.place(x=40, y=350)
        self.button_random.place(x=40, y=500)
        self.button_reset.place(x=40, y=650)
        self.button_quit.place(x=40, y=800)

        # Defining the slider.
        self.slider_random = tk.Scale(self.menu, from_=0, to=100, orient="horizontal", command=self.slider_value)
        self.slider_random.set(50)
        # Packing the slider.
        self.slider_random.pack()
        # Placing the slider.
        self.slider_random.place(x=62, y=590)

        # Defining a dropdown menu for the form and color.

        self.options_figures = [
            "circles",
            "squares",
            "surprise"
        ]
        self.var_figure = tk.StringVar(self.root)
        self.dropdown_figure = tk.OptionMenu(self.menu, self.var_figure,
                                             self.options_figures[0], self.options_figures[1],
                                             self.options_figures[2], command=self.options_shape)
        self.var_figure.set(self.options_figures[0])
        #self.var_color.trace("w", FUNCTIONNAME)
        self.dropdown_figure.pack()

        # Dropdown menu for the cell color
        self.options_colors = [
            "blue",
            "red",
            "white",
            "green",
            "yellow",
            "purple",
            "grey",
            "pink"
        ]
        self.var_color = tk.StringVar(self.root)
        self.dropdown_colors = tk.OptionMenu(self.menu, self.var_color,
                                             self.options_colors[0], self.options_colors[1],
                                             self.options_colors[2], self.options_colors[3],
                                             self.options_colors[4], self.options_colors[5],
                                             self.options_colors[6], self.options_colors[7])
        self.var_color.set(self.options_colors[0])
        #self.var_color.trace("w", FUNCTION NAME)
        self.dropdown_colors.pack()

        # Defining the labels that count the dead and living cells.
        """
        self.label_alive = tk.Label(self.menu, text="Living cells:"+" 1000", height=5, width=20, fg="black", background="grey80")
        self.label_dead = tk.Label(self.menu, text="Dead cells"+" 1000", height=1, width=20, fg="black", background="grey80")
        Packing the labels
        self.label_alive.pack()
        self.label_dead.pack()
        self.label_alive.place(x=40, y=900)
        self.label_alive.place(x=40, y=900)
        """

        # This embeds the pygame window in the tkinter frame.
        os.environ['SDL_WINDOWID'] = str(self.game_border.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        # Initializing pygame.
        pygame.init()
        self.screen = pygame.display.set_mode(GRID_SIZE)
        # Initializing the generations.
        self.init_gen(current_generation, COLOR_DEAD)
        # Defining a clock to set the FPS.
        self.fps_clock = pygame.time.Clock()
        # Setting variables for later use.
        self.next_iteration = False
        self.game_over = False

    def options_shape(self, value):
        return self.var_figure.get()


    # Get the slider value to change the % of randomness.
    def slider_value(self, value):
        self.value = value

    # Button functions.
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

    # Creates a random grid based on the slider value.
    def random_grid(self):
        self.next_iteration = False
        self.init_gen(next_generation, COLOR_DEAD)
        self.percentage_zero = list(itertools.repeat(0,
                                                     (100 - self.slider_random.get())))
        self.percentage_one = list(itertools.repeat(1,
                                                    (self.slider_random.get())))
        # print(self.percentage_zero)
        # print(self.percentage_one)
        for row in range(X_CELLS):
            for col in range(Y_CELLS):
                next_generation[row][col] = random.choice(self.percentage_zero + self.percentage_one)
                # print(next_generation[row][col])

    # Drawing the cells, color black or blue at location (x,y).
    def draw_cell(self, x, y, c):
        pos = (int(x * CELL_SIZE + CELL_SIZE / 2),
               int(y * CELL_SIZE + CELL_SIZE / 2))

        if self.options_shape(self) == "circles":
            pygame.draw.circle(self.screen, colors[c], pos, 5, 0)
        elif self.options_shape(self) == "squares":
            pygame.draw.rect(self.screen, colors[c], pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        elif self.options_shape(self) == "surprise":
            pygame.draw.circle(self.screen, colors[c], pos, CELL_SIZE, CELL_SIZE)

        #pygame.draw.rect(self.screen, colors[c], pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        #pygame.draw.circle(self.screen, colors[c], pos, CELL_SIZE, CELL_SIZE) #Weird form, can also be used instead of rectangles


    # Updating the cells in the current generation.
    def update_gen(self):
        global current_generation
        for y in range(Y_CELLS):
            for x in range(X_CELLS):
                c = next_generation[x][y]
                self.draw_cell(x, y, c)
        current_generation = list(next_generation)

        # Activate a living cell.
    def activate_living_cell(self, x, y):
        current_generation[x][y] = COLOR_ALIVE

        # Deactivate a living cell.
    def deactivate_living_cell(self, x, y):
        current_generation[x][y] = COLOR_DEAD

    # Function to check neighbor cells.
    def check_cells(self, x, y):
        # Check the edges.
        if (x < 0) or (y < 0):
            return 0
        if (x >= X_CELLS) or (y >= Y_CELLS):
            return 0
        if current_generation[x][y] == COLOR_ALIVE:
            return 1
        else:
            return 0

    def check_cell_neighbors(self, row_index, col_index):
        # Get the number of alive cells surrounding the current cell.
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

    # Rules:
    # 1 Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    # 2 Any live cell with two or three live neighbors lives on to the next generation.
    # 3 Any live cell with more than three live neighbors dies, as if by overpopulation.
    # 4 Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    def create_next_gen(self):
        for y in range(Y_CELLS):
            for x in range(X_CELLS):
                n = self.check_cell_neighbors(x, y)  # Number of neighbors.
                c = current_generation[x][y]  # Current cell (either dead or alive).  #CHANGE C into another var.
                if c == COLOR_ALIVE:
                    if (n < 2):  # Rule number 1.
                        next_generation[x][y] = COLOR_DEAD
                    elif (n > 3):  # Rule number 3.
                        next_generation[x][y] = COLOR_DEAD
                    else:  # Rule number 2.
                        next_generation[x][y] = COLOR_ALIVE
                elif c == COLOR_DEAD:
                    if (n == 3):  # Rule number 4.
                        next_generation[x][y] = COLOR_ALIVE
                    else:
                        next_generation[x][y] = COLOR_DEAD

#Problem: first counting, then next iteration.

    # Defines button and mouse clicks.
    def handle_events(self):
        for event in pygame.event.get():
            # Turns the mouse position into a position in the grid.
            posn = pygame.mouse.get_pos()
            x = int(posn[0] / CELL_SIZE)
            y = int(posn[1] / CELL_SIZE)
            # Pressing quit --> quit the game.
            if event.type == pygame.QUIT:
                self.game_over = True
            # Pressing the left mouse button to activate or deactivate a cell.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if next_generation[x][y] == COLOR_DEAD:
                        self.activate_living_cell(x, y)
                    else:
                        self.deactivate_living_cell(x, y)
            # Keeping the right mouse button pressed activates drawing mode.
            if event.type == pygame.MOUSEMOTION and event.buttons[2]:
                self.activate_living_cell(x, y)

            # Define the keyboard key presses for q, space, a, s, r.
            if event.type == pygame.KEYDOWN:
                # Quit the game.
                if event.unicode == 'q':
                    self.game_over = True
                    print("q")
                # Next iteration - manually.
                elif event.key == pygame.K_SPACE:
                    self.create_next_gen()
                    print("keypress")
                # Next iteration - automated.
                elif event.unicode == 'a':  # a to automate the iterations.
                    self.next_iteration = True
                    print("a")
                # Stop the automated iterations.
                elif event.unicode == 's':
                    self.next_iteration = False
                    print("s")
                # Empty the grid.
                elif event.unicode == 'r':
                    self.next_iteration = False
                    self.init_gen(next_generation, COLOR_DEAD)
                    print("r")

    # Runs the game loop
    def run(self):
        while not self.game_over:
            self.handle_events()
            if self.next_iteration:
                self.create_next_gen()
            self.update_gen()
            pygame.display.flip()
            self.fps_clock.tick(FPS_MAX)
            self.root.update()

if __name__ == "__main__":
    GAME = GameOfLife()
    GAME.run()