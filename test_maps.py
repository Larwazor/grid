import unittest
import numpy
from maps import MapData
from game import Grid


class TestMaps(unittest.TestCase):

    def setUp(self):
        MapData.json_file = 'test_maps.json'
        self.test_data = MapData('test_map')

    def test_load_map_from_json(self):
        loaded_test_map = self.test_data.load_map_from_json()
        self.assertEqual((16 * 16), len(loaded_test_map)
                         * len(loaded_test_map[0]))
        self.assertEqual(loaded_test_map[0][0], 'X')
        self.assertEqual(loaded_test_map[10][8], '.')


if __name__ == '__main__':
    unittest.main()
