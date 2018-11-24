import pygame
import tkinter as tk
import os
import cursor
import numpy
import maps


class Tile():
    """
    Holds data about a tile in grid based navigation map.
    """

    def __init__(self, passable):
        self.passable = passable

    def __repr__(self):
        return f"{str(self.passable):<5}"


class Grid():

    def __init__(self, map_name, cell_size):
        self.map_name = map_name
        self.cell_size = cell_size
        self.map = maps.MapData(map_name)
        self.height = len(self.map.data)
        self.width = len(self.map.data[0])
        self.draw_map()

    def draw_map(self):
        print(self.map.data)
        print(self.height, self.width)

        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                cell_color = (70, 70, 70) if self.map.data[y][x] == '.' else (
                    160, 160, 160)
                pygame.draw.rect(screen, cell_color, rect)

        pygame.display.update()

        # class Grid():

        #     def __init__(self, height, width, cell_size, map_name):
        #         self.height = height
        #         self.width = width
        #         self.grid = self.create()
        #         self.cell_size = cell_size

        #     def create(self):
        #         """
        #         Create two-dimensional array containing different types of tiles.
        #         """
        #         grid = numpy.empty((self.height, self.width), dtype=Tile)

        #         for y in range(self.height):
        #             for x in range(self.width):
        #                 #grid[y][x] = self.width * y + x
        #                 if (y+x) % 2 == 0:
        #                     grid[y][x] = Tile(True)
        #                 else:
        #                     grid[y][x] = Tile(False)

        #         print(grid)
        #         return grid

        #     def draw(self):
        #         for y in range(self.height):
        #             for x in range(self.width):
        #                 rect = pygame.Rect(
        #                     x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
        #                 cell_color = (70, 70, 70) if self.grid[y][x].passable else (
        #                     160, 160, 160)
        #                 pygame.draw.rect(screen, cell_color, rect)
        #         pygame.display.update()


def draw_circle():
    pygame.draw.circle(screen, (127, 63, 191), (250, 250), 125)
    pygame.display.update()


def draw_grid():
    grid = Grid('map2', 32)


# def rgb_to_hex(red, green, blue):
    # return '#%02x%02x%02x' % (50, 50, 50)
root = tk.Tk()
embed = tk.Frame(root, width=512, height=512)
embed.grid(columnspan=(512), rowspan=512)
embed.pack(side=tk.TOP)

# menu_color = rgb_to_hex(50, 50, 50)
# menu_active_color = rgb_to_hex(100, 100, 100)
# root.tk_setPalette(background=menu_color,
#    activebackground=menu_active_color)
menu_bar = tk.Menu(root)
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Draw Circle", command=draw_circle)
options_menu.add_command(label="Create Grid", command=draw_grid)
options_menu.add_separator()
options_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="Options", menu=options_menu)

# buttonwin = tk.Frame(root, width=75, height=500)
# buttonwin.pack(side=LEFT)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((512, 512))
screen.fill(pygame.Color(31, 31, 31))

pygame.display.init()
pygame.display.update()

cursor.create_cursor()


# button1 = Button(buttonwin, text='Draw', command=draw)
# button1.pack(side=LEFT)

root.update()
root.config(menu=menu_bar)
root.mainloop()
