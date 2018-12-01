import json
import numpy
import pygame
from pathfind import Grid


class Map():
    """Grid based map"""

    json_file = 'maps.json'

    def __init__(self, map_to_load, cell_size):

        self.map_name = map_to_load
        self.data = self.load_map_from_json()
        self.cell_size = cell_size
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.character_list = []
        self.pathfind_grid = self.get_pathfind_grid()
        self.screen = None

    @classmethod
    def save_map_data(cls, input_ndarray, map_name, output_file):
        """Saves numpy arrays in an easy-to-edit format to json file."""
        map_data_strings = []
        for row in range(len(input_ndarray)):
            row_as_string = ''.join(input_ndarray[row])
            map_data_strings.append(row_as_string)

        json_entry = {map_name: map_data_strings}

        with open(output_file) as f:
            json_data = json.load(f)

        json_data.update(json_entry)

        with open(output_file, 'w') as f:
            json.dump(json_data, f)

    def set_screen(self, screen):
        self.screen = screen

    def load_map_from_json(self):
        """Loads a map layout from json file and converts it to numpy two dimensional array."""
        with open(Map.json_file) as f:
            json_data = json.load(f)

        height = len(json_data[self.map_name])
        width = len(json_data[self.map_name][0])
        map = numpy.empty((height, width), dtype=str)

        for y in range(height):
            for x in range(width):
                map[y][x] = json_data[self.map_name][y][x]

        return map

    def get_size(self):
        w_width = self.cell_size * self.width
        w_height = self.cell_size * self.height
        return (w_width, w_height)

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                cell_color = (70, 70, 70) if self.data[y][x] == '.' else (
                    160, 160, 160)
                pygame.draw.rect(self.screen, cell_color, rect)

    def contains_position(self, pos):
        """Test if position is on the map"""
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width and pos[1] < self.height:
            return True
        else:
            return False

    def get_pos(self, pos):
        """Return info about position('X', '.' or None)"""
        if self.contains_position(pos):
            return self.data[pos[1]][pos[0]]
        else:
            return None

    def can_move_to_position(self, pos):
        """Test if position is walkable, a '.'"""
        if self.get_pos(pos) == '.':
            return True
        else:
            return False

    def get_pathfind_grid(self):
        """
        Return a pathfind Grid with map data turned into booleans(1 or 0)
        """
        grid_data = []
        for y in range(len(self.data)):
            grid_data.append([])
            for x in range(len(self.data[0])):
                if self.get_pos((x, y)) == '.':
                    grid_data[y].append(1)
                else:
                    grid_data[y].append(0)
        return Grid(grid_data)

    def find_path(self, start, end):
        """Find path from pathfinding grid"""
        self.pathfind_grid.find_path(start, end)


# Snippet for setting up a new map and adding it to json

# map1 = numpy.empty((16, 16), dtype=str)
# print(f'{len(map1)} x {len(map1[0])}')


# for y in range(len(map1)):
#     for x in range(len(map1[0])):
#         if (y == 0) or (x == 0) or (y == (len(map1) - 1)) or (x == len(map1[0]) - 1):
#             map1[y][x] = 'X'
#         elif (y == 5 and x > 2 and x < len(map1) - 3):
#             map1[y][x] = 'X'
#         else:
#             map1[y][x] = '.'

# MapData.save_map_data(map1, 'map2', 'maps.json')
