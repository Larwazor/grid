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
                print('del', char)
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
        pos_on_grid = self.get_pos(pos)
        if pos_on_grid == '.':
            return True
        else:
            return False


def draw_circle():
    # Test function.
    pygame.draw.circle(screen, (127, 63, 191), (250, 250), 125)


def draw_grid(map_name, cell_size):
    # Function to create a test grid.
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
    # Create menu bar.
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


def get_kb_input():
    kb_input = pygame.key.get_pressed()
    if kb_input[pygame.K_a]:
        current_grid.character_list[0].set_direction('w')
    elif kb_input[pygame.K_d]:
        current_grid.character_list[0].set_direction('e')
    elif kb_input[pygame.K_w]:
        current_grid.character_list[0].set_direction('n')
    elif kb_input[pygame.K_s]:
        current_grid.character_list[0].set_direction('s')


def get_mouse_input():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (pygame.mouse.get_pos()[
                         0] // current_grid.cell_size, pygame.mouse.get_pos()[1] // current_grid.cell_size)

            for pos in get_line(current_grid.character_list[0].pos, mouse_pos):
                flash_pos(pos)


def flash_pos(pos):
    flash_size = current_grid.cell_size
    flash_color = (255, 0, 0)
    current_grid.get_pos(pos)
    rect = pygame.Rect(pos[0]*flash_size, pos[1] *
                       flash_size, flash_size, flash_size)

    pygame.draw.rect(screen, flash_color, rect)


def draw_line(start_pos, end_pos):
    x0 = start_pos[0]
    y0 = start_pos[1]
    x1 = end_pos[0]
    y1 = end_pos[1]

    tiles_in_line = []

    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = (dx if dx > dy else dy) / 2
    e2 = 0

    tiles_in_line.append(current_grid.get_pos((x0, y0)))

    while True:
        if (x0 == x1 and y0 == y1):
            break
            e2 = err
        if (e2 > -dx):
            err -= dy
            x0 += sx
        if (e2 < dy):
            err += dx
            y0 += sy

    return tiles_in_line


def bresenham(start_pos, end_pos):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """

    x0 = start_pos[0]
    y0 = start_pos[1]
    x1 = end_pos[0]
    y1 = end_pos[1]

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx

    D += 2*dy


def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


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
