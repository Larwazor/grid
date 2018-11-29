

class Node():
    """
    Represents a single node on the pathfinding grid

    Keeps track of its position, score and parent. Provides check for equality with another node.
    """

    def __init__(self, position):
        self.position = position
        self.g_score = 0  # Nodes between start and current point.
        self.h_score = 0  # Estimated nodes between current and destination.
        self.parent = None  # Shortest step to this node

    def __repr__(self):
        return f'{type(self).__name__}, pos: {self.position}, g: {self.g_score}, h: {self.h_score}, f: {self.get_f_score()}'

    def isEqual(self, other):
        return self.position == other.position

    def get_f_score(self):
        return self.g_score + self.h_score


class Grid():
    """
    Represents a grid based map of booleans for pathfinding.
    """

    def __init__(self, map_data):
        self.open_list = []
        self.closed_list = []
        self.map_data = map_data

    def insert_in_open_list(self, node):
        """Insert node in open list ordered by f_score"""
        f_score = node.get_f_score()
        count = len(self.open_list)

        if len(self.open_list) == 0:
            self.open_list.append(node)
        else:
            for i in range(count):
                if f_score <= self.open_list[i].get_f_score():
                    self.open_list.insert(i, node)

    def compute_h_score_from_to(self, from_node, to_node):
        """Compute distance from node to node with Manhattan method"""
        return abs(to_node.position[0] - from_node.position[0]) + abs(to_node.position[1] - from_node.position[1])

    def cost_to_move_from_node(self, from_node, to_node):
        return 1

    def find_path(self, start, end):
        if start == end:
            #print('Destination reached')
            return

        if not self.map_data[end[0]][end[1]]:
            #print('Destination not walkable')
            return


test_node = Node((1, 1))
test_node.h_score = 5
test_node.g_score = 1
test_node2 = Node((1, 2))
test_node3 = Node((1, 3))
test_node3.h_score = 3
test_nodes = []
test_data = [[False, False, False, False], [False, True, True, False], [
    False, True, True, False], [False, False, False, False]]
test_grid = Grid(test_data)
# for line in test_grid.map_data:
#    print(line)
# print(test_node)
# print(test_node.isEqual(test_node2))
#test_grid.find_path([1, 1], [0, 0])
test_grid.open_list = test_nodes
for n in test_grid.open_list:
    print(n)
print('-----------------------')
test_grid.insert_in_open_list(test_node)
for n in test_grid.open_list:
    print(n)
print('-----------------------')
test_grid.insert_in_open_list(test_node2)
for n in test_grid.open_list:
    print(n)
print('-----------------------')
test_grid.insert_in_open_list(test_node3)
for n in test_grid.open_list:
    print(n)
print('-----------------------')
print(test_grid.compute_h_score_from_to(test_node, test_node3))
