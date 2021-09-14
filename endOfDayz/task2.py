from task1 import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
from a2_solution import *


# Task 2 starts
class ImageMap(AbstractGrid):
    """a view class which inherits from AbstractGrid, draw the entities with images"""

    def __init__(self, master, size, **kwargs):
        """Constructor of ImageMap

        Parameter:
            master: the window that contains everything
            size: int, the number of rows or the columns
            width: int, width = 50 the Basic map is 50 pixels high and 50 pixels wide
            **kwargs: set the background colour of the ImageMap instance
        """
        super().__init__(master, rows=size, cols=size, width=CELL_SIZE * size,
                         height=CELL_SIZE * size, **kwargs)
        self._size = size
        self.pack(side=tk.LEFT)
        # get the images ready and resize them to the cell size
        self.background_img = ImageTk.PhotoImage(
            Image.open('images/tileable_background.png', 'r').resize((CELL_SIZE, CELL_SIZE)))
        self.crossbow_img = ImageTk.PhotoImage(
            Image.open('images/crossbow.png', 'r').resize((CELL_SIZE, CELL_SIZE)))
        self.garlic_img = ImageTk.PhotoImage(
            Image.open('images/garlic.png', 'r').resize((CELL_SIZE, CELL_SIZE)))
        self.player_img = ImageTk.PhotoImage(
            Image.open('images/hero.png', 'r').resize((CELL_SIZE, CELL_SIZE)))
        self.hospital_img = ImageTk.PhotoImage(
            Image.open('images/hospital.png', 'r').resize((CELL_SIZE, CELL_SIZE)))
        self.zombie_img = ImageTk.PhotoImage(
            Image.open('images/zombie.png', 'r').resize((CELL_SIZE, CELL_SIZE)))

    def draw_entity(self, position, tile_type):
        """Draws the entity with tile type using the given images identifying the entities

        Parameters:
            position: tuple<col, row>:  the position of Entity
            tile_type: str, the different tile type representing the entities

        Return:
            The basic game map with images representing entities
        """
        # draw the entities images
        image_center = self.get_position_center(position)
        if tile_type == ZOMBIE or tile_type == TRACKING_ZOMBIE:
            self.create_image(image_center, image=self.zombie_img)
        elif tile_type == PLAYER:
            self.create_image(image_center, image=self.player_img)
        elif tile_type == HOSPITAL:
            self.create_image(image_center, image=self.hospital_img)
        elif tile_type == CROSSBOW:
            self.create_image(image_center, image=self.crossbow_img)
        elif tile_type == GARLIC:
            self.create_image(image_center, image=self.garlic_img)

    def draw_background(self):
        """Draw the background of the game map"""
        for i in range(self._size):
            for j in range(self._size):
                pos = (i, j)
                image_center = self.get_position_center(pos)
                self.create_image(image_center, image=self.background_img)


class StatusBar(tk.Frame):
    """The StatusBar class inherits from tk.Frame. Shows the basic status of the game"""

    def __init__(self, master, moves_made, reset_func, **kwargs):
        """Constructor of StatusBar

        Parameters:
            master: the window contains everything
            reset_func: a function for resetting a new game
            **kwargs: signifies that any named arguments supported by tk.Canvas
             class should also supported by StatusBar
        """
        super().__init__(master, **kwargs)
        self._master = master
        # set the default value of time 0m/0s
        self.time_second = 0
        self.time_minute = 0
        # record the seconds count without converting to minutes (61s, 100s etc)
        self.seconds = 0
        self._moves_made = moves_made
        # chaser and chasee images
        self.chaser_img = ImageTk.PhotoImage(
            Image.open('images/chaser.png', 'r').resize((50, 50)))
        self.chasee_img = ImageTk.PhotoImage(
            Image.open('images/chasee.png', 'r').resize((50, 50)))
        # chaser image frame
        self._chaser_frame = tk.Frame(self)
        self._chaser_frame.pack(side=tk.LEFT)
        self._chaser = tk.Label(self._chaser_frame, image=self.chaser_img)
        self._chaser.pack(padx='15')
        # the timer frame
        self._timer_frame = tk.Frame(self)
        self._timer_frame.pack(side=tk.LEFT, padx='15')
        self._timer_label = tk.Label(self._timer_frame, text='Timer', font=('calibri', '13'))
        self._timer_label.pack(side=tk.TOP)
        self.time = tk.Label(self._timer_frame, text=f'{self.time_minute}m {self.time_second}s')
        self.time.pack(side=tk.TOP)
        self.time_runner = None
        self.count_time()
        # the moves made frame
        self._moves_outer_frame = tk.Frame(self)
        self._moves_outer_frame.pack(side=tk.LEFT, expand=True)
        self._moves_inner_frame = tk.Frame(self._moves_outer_frame)
        self._moves_inner_frame.pack()
        self._move_label = tk.Label(self._moves_inner_frame, text='Moves made', font=('calibri', '13'))
        self._move_label.pack(side=tk.TOP)
        self._moves_count = tk.Label(self._moves_inner_frame, text=f'{self._moves_made} moves')
        self._moves_count.pack(side=tk.TOP)
        # Restart Game and Quit Game frame
        self._game_buttons = tk.Frame(self)
        self._game_buttons.pack(side=tk.LEFT, padx='25')
        self._restart_game = tk.Button(self._game_buttons, text='Restart Game', command=reset_func)
        self._restart_game.pack(side=tk.TOP)
        self._quit_game = tk.Button(self._game_buttons, text='Quit Game', command=self.quit)
        self._quit_game.pack(side=tk.TOP)
        # chasee image frame
        self._chasee_frame = tk.Frame(self)
        self._chasee_frame.pack(side=tk.LEFT)
        self._chasee = tk.Label(self._chasee_frame, image=self.chasee_img)
        self._chasee.pack(side=tk.RIGHT, padx='15')

    def update_moves(self, moves):
        """Update the moves made on status bar"""
        self._moves_count.config(text=f'{moves} moves')

    def count_time(self):
        """count time and update it on the status bar"""
        # 60 seconds convert to 1 minute
        if self.time_second == 59:
            self.time_second = 0
            self.time_minute += 1
        else:
            self.time_second += 1
        self.seconds += 1
        self.time_runner = self.time.after(1000, self.count_time)
        self.time.config(text=f'{self.time_minute}mins {self.time_second}seconds')

    def set_seconds(self, seconds):
        """Handles the time in load game situation

        Parameter:
            seconds: <int>; the time count in seconds without converting to minutes

        Return:
            tuple: <minutes, seconds>
        """
        self.seconds = seconds
        self.time_minute = seconds // 60
        self.time_second = seconds % 60

    def reset_time(self):
        """Reset the time and start count"""
        self.time_second = 0
        self.time_minute = 0
        self.seconds = 0
        self.time.after_cancel(self.time_runner)
        self.count_time()

    def stop_count(self):
        """Stop time elapse when the game is over, won or lost"""
        self.time.after_cancel(self.time_runner)

    def get_seconds(self):
        """get the seconds elapse"""
        return self.seconds

    def quit(self):
        """Ask the user quit or not and close the game window"""
        ans = messagebox.askyesno('Quit?', 'Are you sure you would like to quit?')
        if ans:
            self._master.destroy()


class WinDialog(tk.Toplevel):
    """This class will prompt the user enter their name if they won the game"""

    def __init__(self, root, time_minute, time_second, seconds, reset_fun):
        """Constructor of HighScores"""
        # pack the label and entry widget
        super().__init__(root)
        self.title = "You Won!"
        self.reset_game = reset_fun
        self.total_seconds = seconds
        self.time_minute = time_minute
        self.time_second = time_second
        self.label = tk.Label(self, text=f'You won in {self.time_minute}m {self.time_second}s! Enter Your name:')
        self.label.pack(side=tk.TOP)
        self.entry = tk.Entry(self, width=20)
        self.entry.pack(side=tk.TOP)
        # pack the button widget
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=30)
        self.button1 = tk.Button(self.buttons_frame, text="Enter", command=self.entry_name)
        self.button1.pack(side=tk.LEFT, padx=20)
        self.button2 = tk.Button(self.buttons_frame, text="Enter and play again", command=self.entry_reset)
        self.button2.pack(side=tk.RIGHT, padx=20)

    def entry_name(self):
        """Entry button to get the user's name to leaderboard"""
        name = str(self.entry.get())
        fd = open(HIGH_SCORES_FILE, 'a')
        time_name = {self.total_seconds: name}
        # store the time_name dict into the file
        fd.writelines(str(time_name) + '\n')
        fd.close()
        # sort the rows by time increase(eg 1s , 3s, 4s)
        fd = open(HIGH_SCORES_FILE, 'r')
        rows = fd.readlines()
        fd.close()
        sorted_rows = sorted(rows, key=lambda x: int(x.split(':')[0][1:]), reverse=False)
        # rewrite the file with sorted rows
        fd = open(HIGH_SCORES_FILE, 'w')
        for row in sorted_rows:
            fd.writelines(row)
        # check if user won and into the top3, if does, show the high scores
        if len(sorted_rows) <= 3:
            fd.close()
            high_scores()
        elif len(sorted_rows) > 3:
            fd.close()
            third_socre = int(sorted_rows[3][1])
            if self.total_seconds <= third_socre:
                high_scores()
        else:
            fd.close()
        self.destroy()

    def entry_reset(self):
        """second button for entrying and resetting the game """
        self.entry_name()
        self.reset_game()


def high_scores():
    """show the leaderboard of the game when player won the game and come into TOP3"""

    tl = Toplevel()
    tl.title('TOP3')
    lable = Label(tl, text="High Scores", bg=DARK_PURPLE, fg="white", font=('calibri', '30'))
    lable.pack(side=tk.TOP)

    # set the method for closing top level window
    def close_high_scores():
        tl.destroy()

    # convert the str data into a new list
    new_list = []
    try:
        fd = open(HIGH_SCORES_FILE, 'r')
        for line in fd.readlines():
            new_list.append(line.strip('\n'))
        # read lines from the new list and create top3 records:
        for line in new_list[:MAX_ALLOWED_HIGH_SCORES]:
            # get the name, minutes and seconds elapse
            seconds = int(line.split(':')[0][1:])
            minute = seconds // 60
            second = seconds % 60
            name = line.split(':')[1][2:-2]
            if minute < 1:
                lable = tk.Label(tl, text=f'{name}: {second}s')
                lable.pack(side=tk.TOP)
            else:
                lable = tk.Label(tl, text=f'{name}: {minute}m {second}s')
                lable.pack(side=tk.TOP)
        fd.close()
    except:
        pass  # make sure if there is not high scores file, no error raise
    button = Button(tl, text='Done', command=close_high_scores)
    button.pack(side=tk.BOTTOM)


class ImageGraphicalInterface:
    """ This class will manage the overall views and handle events"""

    def __init__(self, root, size):
        """Constructor of BasicGraphicalInterface and  draw the title label

        Parameters:
            root:  the root window that will be displayed
            size:  the number of rows (= number of columns) in the game map
        """
        self._moves_made = 0
        self._root = root
        self._size = size
        root.title(TITLE)
        self._game_frame = tk.Frame(root)
        # banner image label
        self._banner_img = ImageTk.PhotoImage(
            Image.open('images/banner.png', 'r').resize((700, 100)))
        self._title = tk.Label(root, image=self._banner_img)
        self._title.pack(side=tk.TOP)
        # Image map view
        self._map = ImageMap(self._game_frame, self._size)
        self._map.pack(side=tk.LEFT)
        # Inventory view
        self._inventory = InventoryView(self._game_frame, self._size, bg='Light grey')
        self._inventory.pack(side=tk.LEFT)
        # set the memory point for the initial game status
        self._initial_game = None
        self._filename = None
        # status bar
        self._status_bar = StatusBar(root, self.get_moves(), self.reset_game)
        self._game_frame.pack(side=tk.TOP)
        self._status_bar.pack(side=tk.TOP, fill=tk.BOTH)
        # file menu bar
        menu_bar = tk.Menu(self._root)
        self._root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Reset game', command=self.reset_game)
        file_menu.add_command(label='Save game', command=self.save_game)
        file_menu.add_command(label='Load game', command=self.load_game)
        file_menu.add_command(label='Quit', command=self.quit_game)
        file_menu.add_command(label='High scores', command=high_scores)

    def reset_game(self):
        """reset the game to the initial status"""
        self._root.after_cancel(self.loop)
        self._moves_made = 0
        self._initial_game = advanced_game(MAP_FILE)
        inventory = self._initial_game.get_player().get_inventory()
        self._status_bar.update_moves(self._moves_made)
        self.draw(self._initial_game)
        self._status_bar.reset_time()
        self._inventory.bind("<Button-1>", lambda event: self._inventory_click(event, inventory))
        self._root.after(1000, self._step, self._initial_game)

    def save_game(self):
        """save_game function is used in task two file menu bar.It stores
        the information ofpositions of entities and status bar
        """
        filename = filedialog.asksaveasfilename()
        if filename:
            self._root.title(filename)
            fd = open(filename, 'w')
            lines = []
            # save time count
            lines.append(str(self._status_bar.seconds) + '\n')
            # save moves made
            lines.append(str(self._moves_made) + '\n')
            # save inventory
            inventory = self.game.get_player().get_inventory()
            status = {True: '1', False: '0'}
            # store the amount of items
            lines.append(str(len(inventory.get_items())) + '\n')
            for item in inventory.get_items():
                lifetime = str(item.get_lifetime()) + ' ' + status[item.is_active()]
                lines.append(item.display() + lifetime + '\n')
            # save the entities
            for key, value in self.game.get_grid().serialize().items():
                entities = str(key) + value
                lines.append(''.join(entities) + '\n')
            lines.append(str(self._size))
            fd.writelines(lines)
            fd.close()

    def load_game(self):
        """load_game open the file that save game created and reset game attributes"""
        filename = filedialog.askopenfilename()
        if filename:
            self._root.title(filename)
            fd = open(filename, 'r')
            lines = fd.readlines()
            # load time
            seconds = int(lines[0].strip())
            # load move made
            moves_made = int(lines[1].strip())
            self._moves_made = moves_made
            # load inventory including their lifetime and activation
            item_length = int(lines[2].strip())  # find the line index of items
            item_lines = lines[3:3 + item_length]
            inventory = Inventory()
            for i in item_lines:
                i = i.strip()
                lifetime = i[1:-2]
                item_str = i[0]  # 'C' 'G'
                if item_str == GARLIC:
                    item = Garlic()
                elif item_str == CROSSBOW:
                    item = Crossbow()
                item._lifetime = int(lifetime)
                inventory.add_item(item)
                if i[-1] == '1': # check if the item is activated
                    item.toggle_active()
            # load entities in the map
            self.game = AdvancedGame(Grid(int(lines[-1])))
            entity = {'P': HoldingPlayer(), 'T': TrackingZombie(), 'Z': Zombie(),
                      'H': Hospital(), 'C': Crossbow(), 'G': Garlic()}
            for line in lines[3 + item_length:-1]:
                line = line.strip()
                xy_position = line.strip()[1:-2]  # '5, 6', '7, 8' etc
                x, y = xy_position.split(', ')[0], xy_position.split(', ')[1]
                position = Position(int(x), int(y))
                self.game.get_grid().add_entity(position, entity[line[-1]])
            fd.close()
            # reloading the game to the last status
            self.game._player_position = self.game.get_grid().find_player()
            self.game.get_player()._inventory = inventory
            self._initial_game = None
            self._root.after_cancel(self.loop)
            self._step(self.game)
            self.draw(self.game)
            self._inventory.bind("<Button-1>", lambda event: self._inventory_click(event, inventory))
            self._status_bar.update_moves(moves_made)
            self._status_bar.set_seconds(seconds)

    def quit_game(self):
        """Ask the user quit or not and destroy the master"""
        ans = messagebox.askyesno('Quit?', 'Are you sure you would like to quit?')
        if ans:
            self._root.destroy()

    def _inventory_click(self, event, inventory):
        """Handle click events, and this method should be called when the user
        left clicks on inventory view

        Parameters:
            event: The click event that will activate or deactivate one pick_up item once
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
        self._map.draw_background()
        for position, entity in game.get_grid().serialize().items():
            self._map.draw_entity(position, entity)
        self._inventory.draw(game.get_player().get_inventory())

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
        elif dir_press == 'Up' or dir_press == 'Left' or dir_press == 'Down' \
                or dir_press == 'Right':
            direction = dir_press
        return direction

    def _move(self, game, direction):
        """Handles moving the player and redrawing the game

        Parameters:
            game: The current game playing
            direction: The direction that entered by player to move the player entity
        """
        if self._initial_game is not None:
            # set the game to the initial status
            game = self._initial_game
        offset = game.direction_to_offset(direction)
        if direction in DIRECTIONS:
            game.move_player(offset)
        if direction in ['Up', 'Left', 'Down', 'Right']:
            self.fire_crossbow(game, direction)
        self._moves_made += 1
        self._status_bar.update_moves(self.get_moves())
        self.draw(game)
        # lost game statement is in _step method
        if game.has_won():
            self.time_minute = self._status_bar.time_minute
            self.time_second = self._status_bar.time_second
            self.seconds = self._status_bar.seconds
            self.win_dialog = WinDialog(self._root, self.time_minute,
                                        self.time_second, self.seconds, self.reset_game)
            self._root.after_cancel(self.loop)
            self._status_bar.stop_count()

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

    def get_moves(self):
        """Get the moves made by player"""
        return self._moves_made

    def _step(self, game):
        """This method triggers the step method of the game every second and
        updates the view accordingly

        Parameters:
            game: the current game playing
        """
        if self._initial_game is not None:
            # if click reset then set the game to the initial status
            game = self._initial_game
        for position, entity in game.get_grid().get_mapping().items():
            if entity.display() != PLAYER:
                entity.step(position, game)
        inventory = game.get_player().get_inventory()
        self.draw(game)
        self.loop = self._root.after(1000, self._step, game)
        if inventory.any_active():
            inventory.step()
        if game.has_lost():
            dialog = messagebox.askyesno(message='Do you want to play again?')
            if dialog:
                self.reset_game()
            else:
                # the window should remain open and display final info
                self._root.after_cancel(self.loop)
                self._status_bar.stop_count()

    def play(self, game):
        """Binds events and initialises gameplay

        Parameters:
            game: the current game playing
        """
        self.game = game
        inventory = self.game.get_player().get_inventory()
        self._root.bind("<Key>", lambda event: self._move(self.game, self.key_press(event)))
        self._inventory.bind("<Button-1>", lambda event: self._inventory_click(event, inventory))
        self._step(self.game)

