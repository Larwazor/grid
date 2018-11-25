import pygame
import tkinter as tk
import os
import cursor
import numpy
import maps


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

        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                cell_color = (70, 70, 70) if self.map.data[y][x] == '.' else (
                    160, 160, 160)
                pygame.draw.rect(screen, cell_color, rect)

        pygame.display.update()


# Test function.
def draw_circle():
    pygame.draw.circle(screen, (127, 63, 191), (250, 250), 125)
    pygame.display.update()

# Function to create a test grid.


def draw_grid(map_name):
    grid = Grid(map_name, 32)
    print(grid.map.data)
    print(f'{grid.height} x {grid.width}')


# Create tkinter embed for Pygame window.
root = tk.Tk()
embed = tk.Frame(root, width=512, height=512)
embed.grid(columnspan=(512), rowspan=512)
embed.pack(side=tk.TOP)

# Create menu bar.
menu_bar = tk.Menu(root)
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Draw Circle", command=draw_circle)
options_menu.add_command(
    label="Create Map1", command=lambda: draw_grid('map1'))
options_menu.add_command(
    label="Create Map2", command=lambda: draw_grid('map2'))
options_menu.add_command(
    label="Create Map3", command=lambda: draw_grid('map3'))
options_menu.add_separator()
options_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="Options", menu=options_menu)

# Mysterious OS settings, latter seems obsolete nowadays.
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# Create Pygame screen
screen = pygame.display.set_mode((512, 512))
screen.fill(pygame.Color(31, 31, 31))
pygame.display.init()
pygame.display.update()

# Create cursor to replace the awkward default one.
cursor.create_cursor()

# Mainloop.
root.update()
root.config(menu=menu_bar)
root.mainloop()
