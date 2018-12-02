from operator import methodcaller


class Node():
    """
    Represents a single node on the pathfinding grid

    Keeps track of its position, score and parent. Checks equality by position.
    """

    def __init__(self, position):
        self.position = position
        self.g_score = 0  # Nodes between start and current point.
        self.h_score = 0  # Estimated nodes between current and destination.
        self.parent = None  # Shortest step to this node

    def __repr__(self):
        return f'{type(self).__name__}, pos: {self.position}, g: {self.g_score}, h: {self.h_score}, f: {self.get_f_score()}'

    def __eq__(self, other):
        return self.position == other.position

    def get_f_score(self):
        return self.g_score + self.h_score

    def compute_h_score_to_node(self, to_node):
        """Compute distance from node to node with Manhattan method"""
        return abs(to_node.position[0] - self.position[0]) + abs(to_node.position[1] - self.position[1])


class Grid():
    """
    Represents a grid based map of integers for pathfinding.
    """

    def __init__(self, map_data):
        self.open_list = []
        self.closed_list = []
        self.map_data = map_data

    def compute_move_cost(self, from_node, to_node):
        """Return move cost from node to another, always 1 for now"""
        return 1

    def clear_lists(self):
        self.open_list = []
        self.closed_list = []

    def contains_position(self, pos):
        """Test if position is on the map"""
        width = len(self.map_data[0])
        height = len(self.map_data)
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < width and pos[1] < height:
            return True
        else:
            return False

    def node_walkable(self, node):
        return self.map_data[node.position[1]][node.position[0]]

    def get_walkable_adjacent_nodes(self, node, diagonals=False):
        """Return walkable adjacent nodes"""
        nodes = []

        for i in range(-1, 2, 2):

            x = node.position[0]
            y = node.position[1] + i
            if self.contains_position([x, y]) and self.map_data[y][x]:
                node_to_add = Node((x, y))
                nodes.append(node_to_add)

            x = node.position[0] + i
            y = node.position[1]
            if self.contains_position([x, y]) and self.map_data[y][x]:
                node_to_add = Node((x, y))
                nodes.append(node_to_add)

            if diagonals:
                for y in range(-1, 2, 2):
                    pos = ((node.position[0] + i, node.position[1] + y))
                    if self.contains_position(pos) and self.map_data[pos[1]][pos[0]]:
                        nodes.append(Node(pos))

        return nodes

    def get_lowest_f_score(self):
        """Get node with lowest f score in open list"""
        return min(self.open_list, key=methodcaller('get_f_score'))

    def find_closest_walkable_nearby(self, from_node, to_node):
        """Find the most convenient walkable node"""

        adj_nodes = self.get_walkable_adjacent_nodes(to_node)

        # Try to find a non diagonal nearby node
        try:
            node_to_return = min(adj_nodes, key=methodcaller(
                'compute_h_score_to_node', from_node))
        # Try to find diagonal nearby node
        except ValueError:
            try:
                adj_nodes = self.get_walkable_adjacent_nodes(
                    to_node, diagonals=True)
                node_to_return = min(adj_nodes, key=methodcaller(
                    'compute_h_score_to_node', from_node))
            except ValueError:
                return
        return node_to_return

    def find_path(self, start_pos, end_pos):
        """Find path from starting coordinates to end coordinates"""
        self.clear_lists()

        start_node = Node(tuple(start_pos))
        end_node = Node(tuple(end_pos))

        # Try to find a walkable node nearby in case arg is not
        if not self.node_walkable(end_node):
            end_node = self.find_closest_walkable_nearby(start_node, end_node)
            if not end_node:
                return

        self.open_list.append(start_node)

        # End loop if there are no more nodes to go through
        while len(self.open_list) > 0:

            # From open list move node with lowest f_score to closed list
            current_node = self.get_lowest_f_score()
            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            # Found path
            if current_node == end_node:
                path = []

                # Gather nodes from end to start
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent

                # Return all but start
                return [i.position for i in list(reversed(path))][1:]

            adj_nodes = self.get_walkable_adjacent_nodes(current_node)

            # All adjacent walkable nodes
            for adj_node in adj_nodes:

                # Skip if already gone through
                if adj_node in self.closed_list:
                    continue

                move_cost = self.compute_move_cost(current_node, adj_node)

                # Remove from open list if current route is faster, otherwise skip
                if adj_node in self.open_list:
                    if current_node.g_score + move_cost >= adj_node.g_score:
                        continue
                    self.open_list.remove(adj_node)

                adj_node.parent = current_node
                adj_node.g_score = current_node.g_score + move_cost
                adj_node.h_score = adj_node.compute_h_score_to_node(
                    end_node)
                self.open_list.append(adj_node)

        # Found no path
        return


# test_node = Node((1, 1))
# test_node.h_score = 5
# test_node.g_score = 1
# test_node2 = Node((1, 2))
# test_node3 = Node((1, 3))
# test_node3.h_score = 3
# test_nodes = []
# test_data = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [
#     0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
# test_grid = Grid(test_data)

# for line in test_grid.map_data:
#     print(line)
# print()

# diags = test_grid.get_walkable_adjacent_nodes(Node((1, 3)), diagonals=True)
# for diag in diags:
#     print(diag)

# test_grid.open_list.append(Node((2, 1)))
# test_grid.find_path((1, 1), (3, 3))

# test_nodes.append(test_node)
# test_grid.open_list.append(test_node)
# test_grid.open_list.append(test_node2)
# test_grid.open_list.append(test_node3)
# for node in test_grid.open_list:
#     print(node)
# print()
# print('lowest f: ', test_grid.get_lowest_f_score())
# test_grid.closed_list.append(test_node3)
# print(test_grid.node_in_closed_list(Node((1, 3))))
