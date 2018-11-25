import json
import numpy


class MapData():
    """Handles data about grid based maps."""

    json_file = 'maps.json'

    def __init__(self, map_to_load):

        self.data = self.load_map_from_json(map_to_load)

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

    def load_map_from_json(self, map_name):
        """Loads a map layout from json file and converts it to numpy two dimensional array."""
        with open(MapData.json_file) as f:
            json_data = json.load(f)

        height = len(json_data[map_name])
        width = len(json_data[map_name][0])
        map = numpy.empty((height, width), dtype=str)

        for y in range(height):
            for x in range(width):
                map[y][x] = json_data[map_name][y][x]

        return map


loaded_map1 = MapData('map1')

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
