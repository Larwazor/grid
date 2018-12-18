import unittest
from maps import Map


class TestMaps(unittest.TestCase):

    def setUp(self):
        Map.json_file = 'test_maps.json'
        self.test_data = Map('test_map', 32, 32)

    def test_load_map_from_json(self):
        loaded_test_map = self.test_data.load_map_from_json()
        self.assertEqual((16 * 16), len(loaded_test_map)
                         * len(loaded_test_map[0]))
        self.assertEqual(loaded_test_map[0][0].movement_cost, 0)
        self.assertEqual(loaded_test_map[10][8].movement_cost, 10)


if __name__ == '__main__':
    unittest.main()
