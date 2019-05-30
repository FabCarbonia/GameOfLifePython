#To do:
# Python ruies
# Limit all lines to 72 characters.
# Create a package, so that other people can use it.

# Packing not needed if placed.

import tkinter as tk
import itertools, os, platform, pygame, random

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

        # Define the location of the frame.
        self.pixel_width = self.root.winfo_screenwidth()
        self.pixel_height = self.root.winfo_screenheight()
        # calculate x and y coordinates for the Tk root window
        self.cor_x = (self.pixel_width  / 2) - (1000 / 2)  # tk.Frame width = 1000
        self.cor_y = (self.pixel_height/ 2) - (1000 / 2)  # tk.Frame height = 1000
        # Set the location.
        self.root.geometry('%dx%d+%d+%d' % (1000, 1000, self.cor_x, self.cor_y))

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
                                             self.options_figures[2])
        self.var_figure.set(self.options_figures[0])

        self.dropdown_figure.place(x=115, y=10)

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
        self.dropdown_colors.place(x=40, y=10)

        # Defining the menu with the instructions
        self.menu_bar = tk.Menu(self.root)
        self.dropdown_menu = tk.Menu(self.menu_bar, tearoff=0) # No ugly line.
        self.menu_bar.add_cascade(label="Click here for instructions", menu=self.dropdown_menu)
        self.dropdown_menu.add_command(label="Instructions", command=self.create_window)
        self.root.config(menu=self.menu_bar)

        # This embeds the pygame window in the tkinter frame.
        os.environ['SDL_WINDOWID'] = str(self.game_border.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        # Defining the grid dimensions.
        self.GRID_SIZE = self.WIDTH, self.HEIGHT = 750, 1000

        # Defining the cell size and the number of cells in the X and Y direction.
        self.CELL_SIZE = 10
        self.X_CELLS = int(self.WIDTH / self.CELL_SIZE)
        self.Y_CELLS = int(self.HEIGHT / self.CELL_SIZE)

        # Defining the number and color for dead and living cells.
        self.COLOR_DEAD = 0
        self.COLOR_ALIVE = 1
        self.colors = []
        self.colors.append((0, 0, 0))  # Black
        self.colors.append((0, 128, 128))  # blue

        # Defining two lists: current generation and next generation.
        self.current_generation = [[self.COLOR_DEAD for col in range(self.Y_CELLS)] for row in range(self.X_CELLS)]
        self.next_generation = [[self.COLOR_DEAD for col in range(self.Y_CELLS)] for row in range(self.X_CELLS)]

        # Defining the max frames per second/speed of the game.
        self.FPS_MAX = 10

        # Initializing pygame.
        pygame.init()
        self.screen = pygame.display.set_mode(self.GRID_SIZE)
        # Initializing the generations.
        self.init_gen(self.current_generation, self.COLOR_DEAD)
        # Defining a clock to set the FPS.
        self.fps_clock = pygame.time.Clock()
        # Setting variables for later use.
        self.next_iteration = False
        self.game_over = False

    def create_window(self):
        self.instruction_window = tk.Toplevel(self.root, background="LightCyan3")
        self.instruction_window.title("Instructions")
        tk.Label(self.instruction_window, text='Welcome to this version of the Game of Life.'
                                               '\nThe on-screen buttons can be used to play the game. '
                                               '\nAlternatively, you can press q (Quit), space (Next iteration), a (Automated game), s (Stop the game) and r (Reset).',
                 background="LightCyan3").pack(padx=30, pady=30)  #padx=30, pady=30

        tk.Button(self.instruction_window, text="Understood, let's play!", background="LightCyan4", activebackground="LightCyan4", command=self.instruction_window.destroy).pack()
        self.x_loc = self.root.winfo_x()
        self.y_loc = self.root.winfo_y()
        self.instruction_window.geometry("+%d+%d" % (self.x_loc + 295, self.y_loc + 450))


    def options_shape(self, value):
        return self.var_figure.get()

    def options_color(self,value):
        return self.var_color.get()

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
        self.init_gen(self.next_generation, self.COLOR_DEAD)
    def quit_button(self):
        self.game_over = True

    # Initializing all the cells.
    def init_gen(self, generation, c):
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                generation[col][row] = c             # MAYBE CHANGE ROW AND COL??

    # Creates a random grid based on the slider value.
    def random_grid(self):
        self.next_iteration = False
        self.init_gen(self.next_generation, self.COLOR_DEAD)
        self.percentage_zero = list(itertools.repeat(0,
                                                     (100 - self.slider_random.get())))
        self.percentage_one = list(itertools.repeat(1,
                                                    (self.slider_random.get())))
        # print(self.percentage_zero)
        # print(self.percentage_one)
        for col in range(self.X_CELLS):
            for row in range(self.Y_CELLS):
                self.next_generation[col][row] = random.choice(self.percentage_zero + self.percentage_one)
                # print(next_generation[row][col])

    # Drawing the cells, color black or blue at location (x,y).
    def draw_cell(self, x, y, c):
        pos = (int(x * self.CELL_SIZE + self.CELL_SIZE / 2),
               int(y * self.CELL_SIZE + self.CELL_SIZE / 2))
        if c == 1:
            if self.options_shape(self) == "circles":
                if self.options_color(self) == "blue":
                    pygame.draw.circle(self.screen, (0, 128, 128), pos, 5, 0)
                if self.options_color(self) == "red":
                    pygame.draw.circle(self.screen, (255, 0, 0), pos, 5, 0)
                if self.options_color(self) == "white":
                    pygame.draw.circle(self.screen, (255, 255, 255), pos, 5, 0)
                if self.options_color(self) == "green":
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 5, 0)
                if self.options_color(self) == "yellow":
                    pygame.draw.circle(self.screen, (255, 255, 0), pos, 5, 0)
                if self.options_color(self) == "purple":
                    pygame.draw.circle(self.screen, (255, 0, 255), pos, 5, 0)
                if self.options_color(self) == "grey":
                    pygame.draw.circle(self.screen, (155, 155, 155), pos, 5, 0)
                if self.options_color(self) == "pink":
                    pygame.draw.circle(self.screen, (255, 75, 150), pos, 5, 0)

            elif self.options_shape(self) == "squares":
                if self.options_color(self) == "blue":
                    pygame.draw.rect(self.screen, (0, 128, 128),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "red":
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "white":
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "green":
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "yellow":
                    pygame.draw.rect(self.screen, (255, 255, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "purple":
                    pygame.draw.rect(self.screen, (255, 0, 255),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "grey":
                    pygame.draw.rect(self.screen, (155, 155, 155),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "pink":
                    pygame.draw.rect(self.screen, (255, 75, 150),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1))

            elif self.options_shape(self) == "surprise":
                if self.options_color(self) == "blue":
                    pygame.draw.circle(self.screen, (0, 128, 128), pos, 5, 2)
                if self.options_color(self) == "red":
                    pygame.draw.circle(self.screen, (255, 0, 0), pos, 5, 2)
                if self.options_color(self) == "white":
                    pygame.draw.circle(self.screen, (255, 255, 255), pos, 5, 2)
                if self.options_color(self) == "green":
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 5, 2)
                if self.options_color(self) == "yellow":
                    pygame.draw.circle(self.screen, (255, 255, 0), pos, 5, 2)
                if self.options_color(self) == "purple":
                    pygame.draw.circle(self.screen, (255, 0, 255), pos, 5, 2)
                if self.options_color(self) == "grey":
                    pygame.draw.circle(self.screen, (155, 155, 155), pos, 5, 2)
                if self.options_color(self) == "pink":
                    pygame.draw.circle(self.screen, (255, 75, 150), pos, 5, 2)

    # Updating the cells in the current generation.
    def update_gen(self):
        global current_generation
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                c = self.next_generation[col][row]
                self.draw_cell(col, row, c)
                self.current_generation[col][row] = self.next_generation[col][row]  # assign element by element

        # Activate a living cell.
    def activate_living_cell(self, x, y):
        self.next_generation[x][y] = self.COLOR_ALIVE

        # Deactivate a living cell.
    def deactivate_living_cell(self, x, y):
        self.next_generation[x][y] = self.COLOR_DEAD

    # Function to check neighbor cells.
    def check_cells(self, x, y):
        # Check the edges.
        if (x < 0) or (y < 0):
            return 0
        if (x >= self.X_CELLS) or (y >= self.Y_CELLS):
            return 0
        if self.current_generation[x][y] == self.COLOR_ALIVE:
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
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                n = self.check_cell_neighbors(col, row)  # Number of neighbors.
                c = self.current_generation[col][row]  # Current cell (either dead or alive).  #CHANGE C into another var.
                if c == self.COLOR_ALIVE:
                    if (n < 2):  # Rule number 1.
                        self.next_generation[col][row] = self.COLOR_DEAD
                    elif (n > 3):  # Rule number 3.
                        self.next_generation[col][row] = self.COLOR_DEAD
                    else:  # Rule number 2.
                        self.next_generation[col][row] = self.COLOR_ALIVE
                elif c == self.COLOR_DEAD:
                    if (n == 3):  # Rule number 4.
                        self.next_generation[col][row] = self.COLOR_ALIVE
                    else:
                        self.next_generation[col][row] = self.COLOR_DEAD

#Problem: first counting, then next iteration.

    # Defines button and mouse clicks.
    def handle_events(self):
        for event in pygame.event.get():
            # Turns the mouse position into a position in the grid.
            posn = pygame.mouse.get_pos()
            x = int(posn[0] / self.CELL_SIZE)
            y = int(posn[1] / self.CELL_SIZE)
            # Pressing quit --> quit the game.
            if event.type == pygame.QUIT:
                self.game_over = True
            # Pressing the left mouse button to activate or deactivate a cell.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.current_generation[x][y] == self.COLOR_DEAD:
                        self.activate_living_cell(x, y)
                    else:
                        self.deactivate_living_cell(x, y)
                    self.update_gen() # If this is active, cell can be activated or deactivated when the game is running.
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
                    self.init_gen(self.next_generation, self.COLOR_DEAD)
                    print("r")

    # Runs the game loop
    def run(self):
        while not self.game_over:

            self.handle_events()
            self.screen.fill((0, 0, 0))
            if self.next_iteration:
                self.create_next_gen() # compute "next_generation" from "current_generation"
            self.update_gen() # copy "current_generation" from "next_generation"
            pygame.display.flip()
            self.fps_clock.tick(self.FPS_MAX)
            self.root.update()

if __name__ == "__main__":
    GAME = GameOfLife()
    GAME.run()