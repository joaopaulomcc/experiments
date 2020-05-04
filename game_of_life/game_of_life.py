"""
Game of life
============

Python implementation of the famous John Conway's game of life.

Based on the "starting_template.py", "shape_list_demo_3.py",
, "array_backed_grid_buffered.py" and other examples from
"https://arcade.academy/examples/index.html" by Paul Vincent Craven.

The followig description comes from https://playgameoflife.com/,
by Edwin Martin <edwin@bitstorm.org>.

The Game
--------

The Game of Life is not your typical computer game. It is a cellular automaton,
and was invented by Cambridge mathematician John Conway.

This game became widely known when it was mentioned in an article published
by Scientific American in 1970. It consists of a collection of cells which,
based on a few mathematical rules, can live, die or multiply.
Depending on the initial conditions, the cells form various patterns
throughout the course of the game.

The Rules
---------

For a space that is populated:
    Each cell with one or no neighbors dies, as if by solitude.
    Each cell with four or more neighbors dies, as if by overpopulation.
    Each cell with two or three neighbors survives.

For a space that is empty or unpopulated
    Each cell with three neighbors becomes populated.
"""
# --------------------------------------------------------------------------------------
# Imports
import arcade
import numpy as np

# --------------------------------------------------------------------------------------
# Configuration constants

# Set how many rows and columns the game grid we will have
ROW_COUNT = 50
COLUMN_COUNT = 50

# Set the width, height of the grid cells and the margin between the
WIDTH = 10
HEIGHT = 10
MARGIN = 1

# Calculate screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

# Set the grid and cells colors
BACKGROUNG_COLOR = arcade.color.GRAY
ALIVE_CELL_COLOR = arcade.color.BLACK
DEAD_CELL_COLOR = arcade.color.WHITE

# Define screen title
SCREEN_TITLE = "Game of Life"

# ---------------------------------------------------------------------------------------
# Main Code


class GameOfLife(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Definition of the main variables
        self.shape_list = []
        self.point_list = []
        self.color_list = []

        # Representation of the the cells' states, 1 for alive and 0 for dead
        self.grid = []

        # Defines if the simulation is running or not
        self.simulate = False

    def setup(self):
        """
        Initial grid setup and cell coordinates calculation
        """

        arcade.set_background_color(BACKGROUNG_COLOR)

        # Create inital grid using random cell states
        self.create_random_grid()

        # Calculate cell corners coordinates
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):

                top_left = [
                    MARGIN + (MARGIN + WIDTH) * j,
                    SCREEN_HEIGHT - MARGIN - (MARGIN + HEIGHT) * i,
                ]
                top_right = [
                    MARGIN + WIDTH + (MARGIN + WIDTH) * j,
                    SCREEN_HEIGHT - MARGIN - (MARGIN + HEIGHT) * i,
                ]
                bottom_right = [
                    MARGIN + WIDTH + (MARGIN + WIDTH) * j,
                    SCREEN_HEIGHT - MARGIN - HEIGHT - (MARGIN + HEIGHT) * i,
                ]
                bottom_left = [
                    MARGIN + (MARGIN + WIDTH) * j,
                    SCREEN_HEIGHT - MARGIN - HEIGHT - (MARGIN + HEIGHT) * i,
                ]

                # Add the points to the points list.
                # ORDER MATTERS!
                # Rotate around the rectangle
                self.point_list.append(top_left)
                self.point_list.append(top_right)
                self.point_list.append(bottom_right)
                self.point_list.append(bottom_left)

        self.update_shapes()

    def update_shapes(self):
        """
        Updates the shape_list so it reflects the new grid states
        """

        self.shape_list = arcade.ShapeElementList()
        self.color_list = []

        # Iterate over the grid and set cell color according to the cell state
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                if self.grid[i][j] == 0:
                    for k in range(4):
                        self.color_list.append(DEAD_CELL_COLOR)
                else:
                    for k in range(4):
                        self.color_list.append(ALIVE_CELL_COLOR)

        # Create the cells's rectangles and add then to the shape list
        shape = arcade.create_rectangles_filled_with_colors(
            self.point_list, self.color_list
        )
        self.shape_list.append(shape)

    def create_random_grid(self):
        """
        Generates a new grid with states defined by chance
        """

        # Define the total number of cells and pick a random number
        # of cells to be alive
        total_cells = ROW_COUNT * COLUMN_COUNT
        alive = np.random.randint(0, total_cells)

        # Create a vector of zeros according to the total number of cells
        grid = np.zeros(total_cells)
        # Change the first n alive elements to 1
        grid[:alive] = 1
        # Shuffle the vector elements randomly
        np.random.shuffle(grid)
        # Reshape vector to the correct number of rows and columns
        grid = grid.reshape((ROW_COUNT, COLUMN_COUNT))

        # Update grid variables
        self.grid = grid

    def apply_rules(self):
        """
        Iterate over current grid states and apply the Game of life rules
        generating a new state for each cell.
        """

        # Copy current grid states to new variables
        # It is importante to use np.copy here
        # simply making new_grid = old_grid would generate problems
        # as both variables would reference the same object in memory
        # np.copy creates a new independente object
        old_grid = np.copy(self.grid)
        new_grid = np.copy(old_grid)

        # Iterate over cells
        for i, row in enumerate(old_grid):
            for j, cell in enumerate(row):

                # For each cell a neighbourhood of 9 cells is created by slicing
                # a part of the main grid

                left = j - 1
                right = j + 2
                top = i - 1
                bottom = i + 2

                # If the cell is in one of the grid borders change the neighbourhood
                # limits so they do not go beyond the grid limits
                if left < 0:
                    left = 0
                if right > COLUMN_COUNT:
                    right = COLUMN_COUNT
                if top < 0:
                    top = 0
                if bottom > ROW_COUNT:
                    bottom = ROW_COUNT

                neighbourhood = old_grid[top:bottom, left:right]

                # Apply game of life rules

                # If the cell is alive check if it will survive
                if old_grid[i][j] == 1:

                    # If the total number of neighbours is too small
                    # the cell dies from loniness, if it is too big
                    # the cell dies from over population
                    if (neighbourhood.sum() <= 2) or (neighbourhood.sum() >= 5):
                        # Save new cell state to new grid
                        new_grid[i][j] = 0

                # If the cell is dead check if there are the correct number
                # of neighbours to repopulate via reproduction
                else:
                    if neighbourhood.sum() == 3:
                        # Save new cell state to new grid
                        new_grid[i][j] = 1

        # Update grid variable to the new state
        self.grid = np.copy(new_grid)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        self.shape_list.draw()

    def on_update(self, delta_time):
        """
        Run updates
        """
        # If the simulation flag is activated apply the game of life rules
        # to generate a new state, then update the shape list
        if self.simulate:
            self.apply_rules()
            self.update_shapes()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        # print(key, key_modifiers)
        # self.apply_rules()
        # self.update_shapes()

        # Press SPACE to pause or unpause simulation
        if key == arcade.key.SPACE:
            self.simulate = not self.simulate

        # Press C to clear the grid
        elif key == arcade.key.C:
            self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
            self.update_shapes()

        # Press R to reset the grid to a new random state
        elif key == arcade.key.R:
            self.create_random_grid()
            self.update_shapes()

        # Press Q to close the window and quit the game
        elif key == arcade.key.Q:
            self.close()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Change the state of a cell with a mouse click
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int((SCREEN_HEIGHT - y) // (HEIGHT + MARGIN))

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the cell state between alive and dead
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            else:
                self.grid[row][column] = 0

        # Update the shapes with the new grid state
        self.update_shapes()


def main():
    """ Main method """
    game = GameOfLife(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
