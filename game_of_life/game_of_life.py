"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import numpy as np

# Set how many rows and columns we will have
ROW_COUNT = 50
COLUMN_COUNT = 50

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 10
HEIGHT = 10

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 1

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Game of Life"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.GRAY)

        self.shape_list = []
        self.point_list = []
        self.color_list = []
        self.grid = []
        self.simulate = False

        # If you have sprite lists, you should create them here,
        # and set them to None

    def update_grid(self):
        self.shape_list = arcade.ShapeElementList()
        self.color_list = []

        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                if self.grid[i][j] == 0:
                    for k in range(4):
                        self.color_list.append(arcade.color.WHITE)
                else:
                    for k in range(4):
                        self.color_list.append(arcade.color.BLACK)

        shape = arcade.create_rectangles_filled_with_colors(self.point_list,
                                                            self.color_list)
        self.shape_list.append(shape)

    def create_random_grid(self):

        total_cells = ROW_COUNT * COLUMN_COUNT
        active_cells = np.random.randint(0, total_cells)

        grid = np.zeros(total_cells)
        grid[:active_cells] = 1
        np.random.shuffle(grid)
        grid = grid.reshape((ROW_COUNT, COLUMN_COUNT))
        self.grid = grid

    def apply_rules(self):

        old_grid = np.copy(self.grid)
        new_grid = np.copy(old_grid)

        for i, row in enumerate(old_grid):
            for j, cell in enumerate(row):

                left = j - 1
                right = j + 2
                top = i - 1
                bottom = i + 2

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

                if old_grid[i][j] == 1:
                    if (neighbourhood.sum() <= 2) or (neighbourhood.sum() >= 5):
                        new_grid[i][j] = 0
                    #print(neighbourhood)

                else:
                    if neighbourhood.sum() == 3:
                        new_grid[i][j] = 1

        self.grid = np.copy(new_grid)

    def setup(self):
        # Create your sprites and sprite lists here

        self.create_random_grid()
        #self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT))

        # Calculate rectangle points
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
                # Rotate around the rectangle, don't append points caty-corner
                self.point_list.append(top_left)
                self.point_list.append(top_right)
                self.point_list.append(bottom_right)
                self.point_list.append(bottom_left)

        self.update_grid()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.shape_list.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.simulate:
            self.apply_rules()
            self.update_grid()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        # print(key, key_modifiers)
        # self.apply_rules()
        # self.update_grid()
        self.simulate = not self.simulate

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        # print("mouse motio:")
        # print(x, y, delta_x, delta_y)
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        # print(x, y, button, key_modifiers)
        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int((SCREEN_HEIGHT - y) // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the location between 1 and 0.
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            else:
                self.grid[row][column] = 0

        self.update_grid()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
