import tkinter as tk
from tkinter import messagebox
from a2_solution import *


# task 1 starts here
class AbstractGrid(tk.Canvas):
    """AbstractGrid is an abstract view class which inherits from tk.canvas
       And is the parent class of BasicMap, InventoryView."""

    def __init__(self, master, rows, cols, width, height, **kwargs):
        """Constructor of the AbstractGrid

        Parameters:
            master: the window display the grid
            rows: the rows of the grids
            cols: the columns of the grids
            width: the width in pixels of grid
            height: the height in pixels of grid
            **kwargs: signifies that any named arguments supported by tk.Canvas
                        class should also supported by AbstractGrid.
        """
        super().__init__(master, width=width, height=height, **kwargs)
        self._rows = rows
        self._cols = cols
        self._row_step = height // rows
        self._col_step = width // cols

    def get_bbox(self, position):
        """Returns the bounding box for the (row, column) position

        Parameters:
            position: <tuple> the row-col position of the bounding box

        Returns:
            the pixel positions of the edges of the shape, in the form
            (x min, y min, x max, y max).
        """
        row = position[1]
        col = position[0]
        # the pixel position of this shape
        x1 = col * self._col_step
        y1 = row * self._row_step
        x2 = x1 + self._col_step
        y2 = y1 + self._row_step
        return x1, y1, x2, y2

    def pixel_to_position(self, pixel):
        """Converts the (x, y) pixel position (in graphics units) to
        a (row, column) position.

        Parameter:
            pixel:<tuple> the pixel position in graphics units

        Return:
            list: (col, row) position
        """
        row = pixel[1] // self._row_step
        col = pixel[0] // self._col_step
        return col, row

    def position_to_pixel(self, position):
        """Converts the pixel position to a (row, col) position in the map

        Parameters:
            position: The (col, row) position in the gird
        """
        x = position[0] * self._col_step
        y = position[1] * self._row_step
        return x, y

    def get_position_center(self, position):
        """Gets the graphics coordinates for the center of the cell at the
        given (row, column) position

        Parameter:
            position: <tuple>(col, row)

        Returns:
            int: x, y, the center of the position x, y in pixels
        """
        # get the 4 edges of the cell
        edges = self.get_bbox(position)
        x = int(edges[2] - self._col_step / 2)
        y = int(edges[3] - self._row_step / 2)
        return x, y

    def annotate_position(self, position, text):
        """Annotates the center of the cell at the given (row, column)
        position with the provided text.

        Parameter:
            position: <tuple> (col, row) of the cell to be annotated
            text : <str> the text that will be annotated

        Returns:
            None
        """
        self.create_text(self.get_position_center(position), text=text)


class BasicMap(AbstractGrid):
    """a view class which inherits from AbstractGrid"""

    def __init__(self, master, size, **kwargs):
        """Constructor of BasicMap

        Parameter:
            master: the window that contains everything
            size: int, the number of rows or the columns
            width: int, width = 50 the Basic map is 50 pixels high and 50 pixels wide
            **kwargs: set the background colour of the BasicMap instance by
            using the kwargs
        """
        super().__init__(master, rows=size, cols=size, width=CELL_SIZE*size,
                         height=CELL_SIZE*size, **kwargs)
        self._size = size
        self.pack(side=tk.LEFT)

    def draw_entity(self, position, tile_type):
        """Draws the entity with tile type at the given position using a
        coloured rectangle with superimposed text identifying the entity

        Parameters:
            position: tuple<col, row>:  the position of Entity
            tile_type: str, the different tile type representing the entities

        Return:
            The basic game map with rectangles and texts
        """
        if tile_type == PLAYER or tile_type == HOSPITAL:
            self.create_rectangle(self.get_bbox(position),
                                  fill=ENTITY_COLOURS[tile_type])
            self.create_text(self.get_position_center(position),
                             text=tile_type, fill="white")
        else:
            # create the bounding box of the cell
            self.create_rectangle(self.get_bbox(position),
                                  fill=ENTITY_COLOURS[tile_type])
            # create text of entity in the cell
            self.create_text(self.get_position_center(position), text=tile_type)


class InventoryView(AbstractGrid):
    """ a view class which inherits from AbstractGrid and displays the items
    the player has in their inventory"""

    def __init__(self, master, rows, **kwargs):
        """Constructor of InventoryView

        Parameter:
            master: the window that contains everything
            rows: int the number of rows of the inventory
            **kwargs: signifies that any named arguments supported by tk.Canvas
            class should also supported by InventoryView
            """
        super().__init__(master, rows=rows, cols=2, width=INVENTORY_WIDTH,
                         height=CELL_SIZE*rows, **kwargs)
        self._rows = rows
        self._row_step = CELL_SIZE
        self.pack(side=tk.RIGHT)

    def draw(self, inventory):
        """ Draws the inventory label and current items with their lifetimes

        Parameter:
            inventory: the model in a2 that containing pick-up items
        """
        self.create_text((100, 20), text='Inventory', fill=DARK_PURPLE,
                         font=('bold', 20))
        rows = 1
        item_dict = {GARLIC:'Garlic', CROSSBOW:'Crossbow'}
        font_color = {True:'white', False:DARK_PURPLE}
        for item in inventory.get_items():
            if item.is_active():
                self.create_rectangle(0, CELL_SIZE*rows, 200, CELL_SIZE*(rows+1),
                                      fill=ACCENT_COLOUR)
            self.create_text(self.get_position_center((0, rows)),
                             text=item_dict[item.display()], fill=font_color[item.is_active()])
            self.create_text(self.get_position_center((1, rows)),
                             text=f'{item.get_lifetime()}', fill=font_color[item.is_active()])
            rows += 1

    def toggle_item_activation(self, pixel, inventory):
        """Activates or deactivates the item (if one exists) in the row
        containing the pixel

        Parameter:
            pixel: The click  position in pixel
            inventory: the model in a2 that containing pick-up items
        """
        # translate the pixel into row-col position of the click event
        click_position = self.pixel_to_position(pixel)
        row = click_position[1]
        if row in range(1, len(inventory.get_items()) + 1):
            click_item = inventory.get_items()[row - 1]
            if not inventory.any_active():
                click_item.toggle_active()
            elif click_item.is_active():
                click_item.toggle_active()


class BasicGraphicalInterface:
    """ This class will manage the overall views and handle events"""

    def __init__(self, root, size):
        """Constructor of BasicGraphicalInterface and  draw the title label

        Parameters:
            root:  the root window that will be displayed
            size:  the number of rows (= number of columns) in the game map
        """
        self._root = root
        self._size = size
        root.title(TITLE)
        self._title = tk.Label(root, text=TITLE, bg=DARK_PURPLE, fg='White',
                               font=('calibri', 20))
        self._title.pack(side=tk.TOP, fill=tk.X)
        # Basic map view
        self._map = BasicMap(root, self._size, bg=MAP_BACKGROUND_COLOUR)
        self._map.pack(side=tk.LEFT)
        # Inventory view
        self._inventory = InventoryView(root, self._size, bg='Light grey')
        self._inventory.pack(side=tk.LEFT)
        self._initial_game = None

    def _inventory_click(self, event, inventory):
        """Handle click events, and this method should be called when the user
        left clicks on inventory view

        Parameters:
            event: The click event that will activate or deactivate one pick_up
             item once
            inventory: The Inventory instance
        """
        self._inventory.delete(tk.ALL)
        click_pixel = [event.x, event.y]
        self._inventory.toggle_item_activation(click_pixel, inventory)
        self._inventory.draw(inventory)

    def draw(self, game):
        """Clears and redraws the view based on the current game state

        Parameters:
            game: The current game playing
        """
        self._map.delete(tk.ALL)
        self._inventory.delete(tk.ALL)
        for position, entity in game.get_grid().serialize().items():
            self._map.draw_entity(position, entity)
        self._inventory.draw(game.get_player().get_inventory())

    def reset_game(self):
        """reset the game to the initial status"""
        self._root.after_cancel(self.loop)
        self._initial_game = advanced_game(MAP_FILE)
        inventory = self._initial_game.get_player().get_inventory()
        self.draw(self._initial_game)
        self._root.bind("<Key>", lambda event: self._move(self._initial_game, self.key_press(event)))
        self._inventory.bind("<Button-1>", lambda event: self._inventory_click(event, inventory))
        self._root.after(1000, self._step, self._initial_game)

    def key_press(self, e):
        """Translate the press on keyboard into the direction of moving

        Parameter:
            str: press: the input of pressing keyboard

        Return:
            str: W, A, S, D represent the direction of moving
        """
        press = e.char
        dir_press = e.keysym
        direction = ''
        if press == 'w':
            direction = UP
        elif press == 'a':
            direction = LEFT
        elif press == 's':
            direction = DOWN
        elif press == 'd':
            direction = RIGHT
        elif dir_press == 'Up' or dir_press == 'Left' or dir_press == 'Down'\
                or dir_press == 'Right':
            direction = dir_press
        return direction

    def _move(self, game, direction):
        """Handles moving the player and redrawing the game

        Parameters:
            game: The current game playing
            direction: The direction that entered by player to move the player entity
        """
        offset = game.direction_to_offset(direction)
        if direction in DIRECTIONS:
            game.move_player(offset)
        if direction in ['Up', 'Left', 'Down', 'Right']:
            self.fire_crossbow(game, direction)
        self.draw(game)

    def fire_crossbow(self, game, direction):
        """Shoot the zombie if player press 'F' and there is a crossbow item
        in the inventory is activated

        Parameters:
            game: the current game instance playing
            action: the key pressed by the user to prompt an action
        """
        action = ARROWS_TO_DIRECTIONS[direction]
        player = game.get_player()
        # Ensure the crossbow has been activated.
        if player.get_inventory().has_active(CROSSBOW):
            start = game.get_grid().find_player()
            offset = game.direction_to_offset(action)
            # Find the first entity in the direction player fired.
            first = first_in_direction(
                game.get_grid(), start, offset
            )
            # If the entity is a zombie, kill it.
            if first is not None and first[1].display() in ZOMBIES:
                position, entity = first
                game.get_grid().remove_entity(position)
                self.draw(game)

    def _step(self, game):
        """This method triggers the step method of the game every second and
         updates the view accordingly

        Parameters:
            game: the current game playing
        """
        for position, entity in game.get_grid().get_mapping().items():
            if entity.display() != PLAYER:
                entity.step(position, game)
        inventory = game.get_player().get_inventory()
        self.draw(game)
        self.loop = self._root.after(1000, self._step, game)
        if inventory.any_active():
            inventory.step()
        if game.has_lost() or game.has_won():
            dialog = messagebox.askyesno(message='Do you want to play again?')
            if dialog:
                self.reset_game()
            else:
                self._root.destroy()

    def play(self, game):
        """Binds events and initialises gameplay

        Parameters:
            game: the current game playing
        """
        inventory = game.get_player().get_inventory()
        self._root.bind("<Key>", lambda event: self._move(game, self.key_press(event)))
        self._inventory.bind("<Button-1>", lambda event: self._inventory_click(event, inventory))
        self._step(game)