import pygame
import math


class Character():
    """Basic game character"""

    def __init__(self, image, start_pos, grid):
        self.image = pygame.image.load('images/' + image)
        self.pos = list(start_pos)
        self.grid = grid
        self.scale_image()
        self.character_list = grid.character_list
        self.character_list.append(self)
        self.target_pos = self.pos
        self.draw_pos = None
        self.init_drawing()
        self.move_speed = 5.0
        self.is_moving = False

    def init_drawing(self):
        self.draw_pos = [float(i) for i in self.pos]

    def scale_image(self):
        """Scale image if grid's cell size differs from it"""
        original_size = self.image.get_rect().size
        if original_size[0] != self.grid.cell_size or original_size[1] != self.grid.cell_size:
            self.image = pygame.transform.scale(
                self.image, (self.grid.cell_size, self.grid.cell_size))

    def draw(self, screen):
        screen.blit(
            self.image, (self.draw_pos[0] * self.grid.cell_size, self.draw_pos[1] * self.grid.cell_size))

    def move(self, update_interval):
        """Moves drawing position based on move speed and screen update interval"""
        self.is_moving = True
        approx_tolerance = 0.1  # Tolerance to be considered being close to target
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
        # Set position to be exactly target and set bool to avoid setting new target
        else:
            self.set_pos()
            self.is_moving = False

    def set_pos(self):
        """Sets position and draw position to target position"""
        self.pos = self.target_pos.copy()
        self.draw_pos = self.target_pos.copy()

    def set_direction(self, direction):
        """Set movement direction based on kb input"""
        desired_pos = self.pos.copy()

        if self.is_moving:
            return

        if direction == 'e':
            desired_pos[0] += 1
        elif direction == 'w':
            desired_pos[0] -= 1
        elif direction == 'n':
            desired_pos[1] -= 1
        elif direction == 's':
            desired_pos[1] += 1

        if self.grid.can_move_to_position(desired_pos):
            self.target_pos = desired_pos
