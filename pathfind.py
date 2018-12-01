

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
        print('@@@ NEW GRID @@@')

    def insert_in_open_list(self, node):
        """Insert node in open list ordered by f_score"""
        f_score = node.get_f_score()
        count = len(self.open_list)

        if count == 0:
            self.open_list.append(node)
            #print('added first: ', node)
            #print('closed list: ', self.closed_list)
            # print()
        else:
            for i in range(count):
                if f_score <= self.open_list[i].get_f_score():
                    self.open_list.insert(i, node)
                    break
            #print('added: ', node)

    def compute_h_score_from_to(self, from_position, to_position):
        """Compute distance from node to node with Manhattan method"""
        return abs(to_position[0] - from_position[0]) + abs(to_position[1] - from_position[1])

    def cost_to_move_from_node(self, from_node, to_node):
        return 1

    def node_in_open_list(self, node_to_check):

        if node_to_check in self.open_list:
            print('listcheck')
            return True

        for node in self.open_list:
            if node.position == node_to_check.position:
                print(node.position, node_to_check.position)
                return True
        return False

    def remove_from_open_list(self, node_to_remove):
        for i in self.open_list:
            if list(i.position) == list(node_to_remove.position):
                # print('remove')
                self.open_list.remove(i)

    def node_in_closed_list(self, node_to_check):
        for node in self.closed_list:
            if node.position == node_to_check.position:
                return True
        return False

    def find_path(self, start_pos, end_pos):

        path = []

        # Destination not walkable
        if not self.map_data[end_pos[1]][end_pos[0]]:
            return

        path_found = False

        self.insert_in_open_list(Node([start_pos[0], start_pos[1]]))
        print('first:', self.open_list[0])

        while not path_found:

            # for line in self.open_list:
            #     print(line, line.__hash__)
            # print('### end of list ###')
            # Pop first node from open list and add it to closed list
            print(len(self.open_list))
            current_step = self.open_list[0]
            self.closed_list.append(current_step)
            self.remove_from_open_list(current_step)

            # Current step equals destination
            if list(current_step.position) == list(end_pos):
                #print('Destination reached')
                path_found = True

                temp_step = current_step

                # Get all the nodes from destination to first step
                while temp_step.parent:
                    # print(temp_step.position)
                    path.append(temp_step.position)
                    temp_step = temp_step.parent

                # Clear lists
                self.open_list = []
                self.closed_list = []

                # print('path: ', list(reversed(path)))
                return list(reversed(path))
                break

            adjacent_steps = self.get_walkable_adjacent_nodes(current_step)

            # Loop through current step's adjacent steps
            for step in adjacent_steps:
                # Skip if already in closed list
                if self.node_in_closed_list(step):
                    continue

                move_cost = self.cost_to_move_from_node(current_step, step)

                step.parent = current_step
                step.g_score = current_step.g_score + move_cost
                step.h_score = self.compute_h_score_from_to(
                    step.position, end_pos)

                # Step not in open list
                if self.node_in_open_list(step):
                    # print(step)
                    # Set current step as iterated step's parent
                    # Get g_score by adding parent's g_score and move cost from there
                    # Get h_score(estimated cost to destination)
                    if (current_step.g_score + move_cost) < step.g_score:
                        self.remove_from_open_list(step)
                        self.insert_in_open_list(step)
                # Step already in open list
                else:
                    # print('open_list: ', self.open_list)
                    # Is g_score lower if we use current step to get there
                    # print(step.__hash__)
                    # for i in self.open_list:
                    #     if list(i.position) == list(step.position):
                    #         step = i
                    # print(step.__hash__)

                    # print('modify')
                    # Calculate new g_score and refresh open list
                    self.insert_in_open_list(step)

    def contains_position(self, pos):
        """Test if position is on the map"""
        width = len(self.map_data)
        height = len(self.map_data[0])
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < width and pos[1] < height:
            return True
        else:
            return False

    def get_walkable_adjacent_nodes(self, node):
        """Return walkable adjacent nodes in horizontal or vertical direction"""
        nodes = []
        for i in range(-1, 2, 2):

            x = node.position[0]
            y = node.position[1] + i
            if self.contains_position([x, y]) and self.map_data[y][x]:
                node_to_add = Node([x, y])
                nodes.append(node_to_add)

            x = node.position[0] + i
            y = node.position[1]
            if self.contains_position([x, y]) and self.map_data[y][x]:
                node_to_add = Node([x, y])
                nodes.append(node_to_add)

        return nodes


test_node = Node((1, 1))
test_node.h_score = 5
test_node.g_score = 1
test_node2 = Node((1, 2))
test_node3 = Node((1, 3))
test_node3.h_score = 3
test_nodes = []
test_data = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [
    0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
test_grid = Grid(test_data)
# test_grid.find_path((1, 1), (3, 3))

# for line in test_grid.map_data:
#    print(line)
# print(test_node)
# print(test_node.isEqual(test_node2))
# test_grid.find_path([1, 1], [0, 0])

# print('test:', test_grid.get_walkable_adjacent_nodes(Node([2, 2])))

# for line in test_grid.map_data:
#     print(line)

# for node in test_grid.get_walkable_adjacent_nodes([1, 1]):
#     print(node)


# test_grid.open_list = test_nodes
# for n in test_grid.open_list:
#     print(n)
# print('-----------------------')
# test_grid.insert_in_open_list(test_node)
# for n in test_grid.open_list:
#     print(n)
# print('-----------------------')
# test_grid.insert_in_open_list(test_node2)
# for n in test_grid.open_list:
#     print(n)
# print('-----------------------')
# test_grid.insert_in_open_list(test_node3)
# for n in test_grid.open_list:
#     print(n)
# print('-----------------------')
# test_grid.insert_in_open_list(test_node3)
# for n in test_grid.open_list:
#     print(n)
# print('-----------------------')

# print(test_grid.compute_h_score_from_to(
#     test_node.position, test_node3.position))
