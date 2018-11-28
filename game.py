import pygame
import tkinter as tk
import os
import cursor
import numpy
import maps
from character import Character

app_width = 512  # Start width
app_height = 512  # Start height
root = None
screen = None
embed = None
menu_bar = None
current_grid = None


class Grid():
    """Handles drawing grid based maps."""

    def __init__(self, map_name, cell_size):
        global current_grid
        self.map_name = map_name
        self.cell_size = cell_size
        self.map = maps.MapData(map_name)
        self.height = len(self.map.data)
        self.width = len(self.map.data[0])
        self.set_current_grid()
        self.draw_map()
        self.character_list = []

    def draw_map(self):
        """Draws map based on letters in json map data file."""
        global screen

        width = self.cell_size * self.width
        height = self.cell_size * self.height
        create_window(width, height)
        create_screen(width, height)

        self.draw()

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                cell_color = (70, 70, 70) if self.map.data[y][x] == '.' else (
                    160, 160, 160)
                pygame.draw.rect(screen, cell_color, rect)

    def set_current_grid(self):
        """Set self as current grid and clear old one's character list."""
        global current_grid
        try:
            for char in current_grid.character_list:
                del char
        except Exception:
            pass
        current_grid = self

    def contains_position(self, pos):
        """Test if position is on the grid"""
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width and pos[1] < self.height:
            return True
        else:
            return False

    def get_pos(self, pos):
        """Return info about position('X', '.' or None)"""
        if self.contains_position(pos):
            return self.map.data[pos[1]][pos[0]]
        else:
            return None

    def can_move_to_position(self, pos):
        """Test if position is walkable, a '.'"""
        pos_on_grid = self.get_pos(pos)
        if pos_on_grid == '.':
            return True
        else:
            return False


def draw_circle():
    """Test function."""
    pygame.draw.circle(screen, (127, 63, 191), (250, 250), 125)


def draw_grid(map_name, cell_size):
    """Function to create a test grid."""
    grid = Grid(map_name, cell_size)
    add_character()


def add_character():
    global current_grid
    global character_list
    char = Character('wizard.png', (1, 1), current_grid)


def create_window(window_width, window_height):
    """Create tkinter embed for Pygame window."""
    global root
    global embed

    # Set window pos on start
    if embed == None:
        root.geometry(f'{window_width}x{window_height}+300+100')

    root.minsize(window_width, window_height)
    root.maxsize(window_width, window_height)

    embed = tk.Frame(root, width=window_width, height=window_height)

    embed.pack(ipadx=window_width, ipady=window_height)


def create_menu_bar():
    """Create menu bar."""
    global root
    global menu_bar
    menu_bar = tk.Menu(root)
    options_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu.add_command(label="Draw Circle", command=draw_circle)
    options_menu.add_command(
        label="Create Map1, Cell size: 16x16", command=lambda: draw_grid('map1', 16))
    options_menu.add_command(
        label="Create Map2, Cell size: 32x32", command=lambda: draw_grid('map2', 32))
    options_menu.add_command(
        label="Create Map3, Cell size: 64x64", command=lambda: draw_grid('map3', 64))
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Options", menu=options_menu)


def set_sdl():
    global embed
    """Mysterious OS settings, latter seems obsolete nowadays."""
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'


def create_screen(screen_width, screen_height):
    """Create Pygame screen."""
    global screen
    screen = pygame.display.set_mode((screen_width, screen_width))
    screen.fill(pygame.Color(31, 31, 31))
    pygame.display.init()


# Initialize
root = tk.Tk()
create_window(app_width, app_height)
create_menu_bar()
set_sdl()
create_screen(app_width, app_height)


# Create cursor to replace the awkward default one.
cursor.create_cursor()


def get_kb_input():
    kb_input = pygame.key.get_pressed()
    if kb_input[pygame.K_a]:
        current_grid.character_list[0].move_to_direction('w')
    elif kb_input[pygame.K_d]:
        current_grid.character_list[0].move_to_direction('e')
    elif kb_input[pygame.K_w]:
        current_grid.character_list[0].move_to_direction('n')
    elif kb_input[pygame.K_s]:
        current_grid.character_list[0].move_to_direction('s')
    elif kb_input[pygame.K_g]:
        current_grid.character_list[0].set_sequence(
            ((2, 1), (3, 1), (4, 1), (4, 2), (5, 2), (5, 3), (6, 3), (7, 3)))
    elif kb_input[pygame.K_j]:
        print(current_grid.character_list[0].pos)


def get_mouse_input():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (pygame.mouse.get_pos()[
                0] // current_grid.cell_size, pygame.mouse.get_pos()[1] // current_grid.cell_size)
            flash_pos(mouse_pos)


def flash_pos(pos):
    flash_size = current_grid.cell_size
    flash_color = (255, 0, 0)
    current_grid.get_pos(pos)
    rect = pygame.Rect(pos[0]*flash_size, pos[1] *
                       flash_size, flash_size, flash_size)

    pygame.draw.rect(screen, flash_color, rect)


def game_loop():
    global character_list
    global root
    update_interval = 16
    try:
        current_grid.draw()
        for char in current_grid.character_list:
            char.move(update_interval)
            char.draw(screen)
    except Exception:
        pass
    get_kb_input()
    get_mouse_input()
    pygame.display.update()
    root.after(update_interval, game_loop)


# Tkinter Mainloop
root.resizable(False, False)
root.config(menu=menu_bar)
root.title('Grid Game')
img = tk.Image("photo", file="images/wizard.png")
root.wm_iconphoto(True, img)
game_loop()
root.mainloop()
