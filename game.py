import pygame
import tkinter as tk
import os
import cursor
import numpy
import maps

app_width = 512
app_height = 512
root = None
screen = None
embed = None
menu_bar = None


class Grid():
    """Handles drawing grid based maps."""

    def __init__(self, map_name, cell_size):
        self.map_name = map_name
        self.cell_size = cell_size
        self.map = maps.MapData(map_name)
        self.height = len(self.map.data)
        self.width = len(self.map.data[0])
        self.draw_map()

    def draw_map(self):
        global screen

        width = self.cell_size * self.width
        height = self.cell_size * self.height
        create_window(width, height)

        create_screen(width, height)
        # set_sdl()

        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                cell_color = (70, 70, 70) if self.map.data[y][x] == '.' else (
                    160, 160, 160)
                pygame.draw.rect(screen, cell_color, rect)


def draw_circle():
    # Test function.
    pygame.draw.circle(screen, (127, 63, 191), (250, 250), 125)


def draw_grid(map_name, cell_size):
    # Function to create a test grid.
    grid = Grid(map_name, cell_size)


def create_window(window_width, window_height):
    """Create tkinter embed for Pygame window."""
    global root
    global embed

    # SET WINDOW POS ON SCREEN

    if embed == None:
        root.geometry(f'{window_width}x{window_height}+300+100')
        # screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()
        # x = (screen_width/2) - (window_width/2)
        # y = (screen_height/2) - (window_height/2)
        # root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    root.minsize(window_width, window_height)
    root.maxsize(window_width, window_height)

    embed = tk.Frame(root, width=window_width, height=window_height)

    # side=tk.TOP, fill=tk.BOTH, expand=1
    embed.pack(ipadx=window_width, ipady=window_height)

    #print(f'{window_width} x {window_height}')
    # print(embed.pack_info())


def create_menu_bar():
    # Create menu bar.
    global root
    global menu_bar
    menu_bar = tk.Menu(root)
    options_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu.add_command(label="Draw Circle", command=draw_circle)
    options_menu.add_command(
        label="Create Map1", command=lambda: draw_grid('map1', 16))
    options_menu.add_command(
        label="Create Map2", command=lambda: draw_grid('map2', 32))
    options_menu.add_command(
        label="Create Map3", command=lambda: draw_grid('map3', 64))
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Options", menu=options_menu)


def set_sdl():
    global embed
    # Mysterious OS settings, latter seems obsolete nowadays.
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


def game_loop():
    # Pygame Mainloop
    global root
    # print('game_loop')
    pygame.display.update()
    root.after(16, game_loop)


# Mainloop
root.resizable(False, False)
root.config(menu=menu_bar)
game_loop()
root.mainloop()
