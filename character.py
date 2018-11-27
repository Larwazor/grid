import pygame


class Character():
    """Basic game character"""

    def __init__(self, image, start_pos, grid):
        self.image = pygame.image.load('images/' + image)
        self.pos = list(start_pos)
        self.grid = grid
        self.scale_image()
        self.character_list = grid.character_list
        self.character_list.append(self)

    def scale_image(self):
        """Scale image if grid's cell size differs from it"""
        original_size = self.image.get_rect().size
        if original_size[0] != self.grid.cell_size or original_size[1] != self.grid.cell_size:
            self.image = pygame.transform.scale(
                self.image, (self.grid.cell_size, self.grid.cell_size))

    def draw(self, screen):
        screen.blit(
            self.image, (self.pos[0] * self.grid.cell_size, self.pos[1] * self.grid.cell_size))

    def move(self, direction):
        desired_pos = self.pos.copy()

        if direction == 'e':
            desired_pos[0] += 1
        elif direction == 'w':
            desired_pos[0] -= 1
        elif direction == 'n':
            desired_pos[1] -= 1
        elif direction == 's':
            desired_pos[1] += 1

        if self.grid.can_move_to_position(desired_pos):
            self.pos = desired_pos
