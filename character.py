import pygame
import math


class Character():
    """Basic game character"""

    def __init__(self, image, start_pos, map):
        self.image = pygame.image.load('images/' + image)
        self.pos = list(start_pos)
        self.map = map
        self.scale_image()
        self.character_list = map.character_list
        self.character_list.append(self)
        self.target_pos = self.pos
        self.draw_pos = None
        self.init_drawing()
        self.move_speed = 5.0
        self.is_moving = False
        self.move_sequence = []

    def init_drawing(self):
        """Keep character's actual position and drawing position separate, making latter float"""
        self.draw_pos = [float(i) for i in self.pos]

    def scale_image(self):
        """Scale image if map's cell size differs from it"""
        original_size = self.image.get_rect().size
        if original_size[0] != self.map.cell_size or original_size[1] != self.map.cell_size:
            self.image = pygame.transform.scale(
                self.image, (self.map.cell_size, self.map.cell_size))

    def draw(self, screen):
        screen.blit(
            self.image, (self.draw_pos[0] * self.map.cell_size, self.draw_pos[1] * self.map.cell_size))

    def move(self, update_interval):
        """Moves drawing position based on move speed and screen update interval"""
        self.is_moving = True
        approx_tolerance = 0.05  # Tolerance to be considered being close to target
        total_movespd = (self.move_speed * update_interval) / 1000

        # If not vertically at target, move towards target
        if not math.isclose(self.draw_pos[0], self.target_pos[0], abs_tol=approx_tolerance):
            if self.draw_pos[0] < self.target_pos[0]:
                self.draw_pos[0] += total_movespd
            else:
                self.draw_pos[0] -= total_movespd
        # If not horizontally at target, move towards target
        elif not math.isclose(self.draw_pos[1], self.target_pos[1], abs_tol=approx_tolerance):
            if self.draw_pos[1] < self.target_pos[1]:
                self.draw_pos[1] += total_movespd
            else:
                self.draw_pos[1] -= total_movespd
        # Set position to be exactly target and set bool to enable setting new target
        else:
            self.is_moving = False
            self.set_pos()

            if len(self.move_sequence) > 0:
                self.move_to_next_in_seq()

    def move_to_next_in_seq(self):
        """
        Moves from position to next in a sequence.
        """
        target = self.move_sequence[0]

        self.pop_first_in_sequence()

        if target[0] > self.pos[0]:
            self.move_to_direction('e')
        elif target[0] < self.pos[0]:
            self.move_to_direction('w')
        elif target[1] > self.pos[1]:
            self.move_to_direction('s')
        elif target[1] < self.pos[1]:
            self.move_to_direction('n')

    def set_pos(self):
        """Sets position and draw position to target position"""
        self.pos = self.target_pos.copy()
        self.draw_pos = self.target_pos.copy()

    def set_sequence(self, sequence):
        """Set new movement sequence"""
        self.move_sequence = sequence

    def pop_first_in_sequence(self):
        """Remove first item from movement sequence"""
        self.move_sequence = self.move_sequence[1:]

    def clear_move_sequence(self):
        if len(self.move_sequence) > 0:
            self.move_sequence = []

    def move_to_direction(self, direction, clear_sequence=False):
        """Set movement direction"""
        desired_pos = self.pos.copy()

        if self.is_moving:
            return

        if clear_sequence:
            self.clear_move_sequence()

        if direction == 'e':
            desired_pos[0] += 1
        elif direction == 'w':
            desired_pos[0] -= 1
        elif direction == 'n':
            desired_pos[1] -= 1
        elif direction == 's':
            desired_pos[1] += 1

        if self.map.can_move_to_position(desired_pos):
            self.target_pos = desired_pos

    def find_path_to(self, destination):
        path = self.map.find_path(self.pos, destination)
        if path and len(path) > 0:
            self.set_sequence(path)
