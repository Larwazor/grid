import pygame
import math
import time

start = 0
end = 0


class Character():
    """Basic game character"""

    def __init__(self, image, start_pos, map, screen, menu_height):
        self.orig_image = pygame.image.load('images/' + image)
        self.image = self.orig_image.copy()
        self.pos = list(start_pos)
        self.draw_pos = self.pos.copy()
        self.map = map
        self.scale_image()
        self.map.character_list.append(self)
        self.move_speed = 5.0
        self.move_sequence = []  # List of positions to traverse
        self.screen = screen
        self.menu_height = menu_height
        self.target_pos = []  # Next position to move to
        self.move_dir = []  # Direction of movement
        self.queued_destination = []  # Queued destination from click

    def scale_image(self):
        """Scale image if map's cell size differs from it"""
        original_size = self.image.get_rect().size
        if original_size[0] != self.map.cell_size or original_size[1] != self.map.cell_size:
            self.image = pygame.transform.scale(
                self.orig_image, (self.map.cell_size, self.map.cell_size))

    def draw(self):
        self.screen.blit(
            self.image, (self.draw_pos[0] * self.map.cell_size, self.menu_height + self.draw_pos[1] * self.map.cell_size))  # has + menu_height

    def set_target_and_dir(self):
        """Get last item in move sequence and calculate direction"""
        if self.move_sequence:
            self.target_pos = self.move_sequence[-1]
            self.move_dir = (self.target_pos[0] - self.pos[0],
                             self.target_pos[1] - self.pos[1])

    def move(self, update_interval):
        """Calculates drawing position and moves actual position after"""
        self.draw()

        # No current target position
        if not self.target_pos:

            # There is a queued position for a click and we find a new path
            if self.queued_destination:
                self.find_path()

            # Get new target
            self.set_target_and_dir()

        if not self.move_dir or not self.target_pos:
            return

        approx_tolerance = 0.05  # Tolerance to be considered being close to target

        # Slow down movement by dividing if moving diagonally and take cell.size into account
        divider = (1.4 if abs(
            self.move_dir[0]) + abs(self.move_dir[1]) == 2 else 1) * (320 / self.map.cell_size)
        # Get movement cost from target tile
        terrain_speed = self.map.data[
            self.target_pos[1]][self.target_pos[0]].movement_cost

        total_movespd = (self.move_speed * update_interval) / \
            100 / (divider * terrain_speed)

        # If we are close enough to target position, round positions to integers, clear target and pop
        if math.isclose(self.draw_pos[0], self.target_pos[0], abs_tol=approx_tolerance) and math.isclose(self.draw_pos[1], self.target_pos[1], abs_tol=approx_tolerance):
            self.pos[0] = self.draw_pos[0] = int(self.target_pos[0])
            self.pos[1] = self.draw_pos[1] = int(self.target_pos[1])
            self.move_sequence.pop()
            self.target_pos = []
        else:  # Move in the required direction
            self.draw_pos[0] += self.move_dir[0] * total_movespd
            self.draw_pos[1] += self.move_dir[1] * total_movespd

    def find_path_to(self, destination):
        """Queues up a path find to destination"""
        self.queued_destination = destination

    def find_path(self):
        """Finds a path to queued destination and sets move sequence"""
        path = self.map.find_path(self.pos, self.queued_destination)
        if path:
            self.move_sequence = path[:-1]
            self.queued_destination = []

    def move_to_direction(self, direction, clear_sequence=False):
        """Set movement direction

            Keyboard movement.
        """
        desired_pos = self.pos.copy()

        if direction == 'e':
            desired_pos[0] += 1
        elif direction == 'w':
            desired_pos[0] -= 1
        elif direction == 'n':
            desired_pos[1] -= 1
        elif direction == 's':
            desired_pos[1] += 1

        # If we can move to direction and aren't currently walking
        if self.map.position_walkable(desired_pos) and not self.target_pos:
            self.move_sequence = [desired_pos]
            self.set_target_and_dir()
