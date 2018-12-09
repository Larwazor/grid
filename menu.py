import pygame
from functools import partial


class Menu():
    """Menu parent"""

    def __init__(self, screen, color, pos, size):
        self.screen = screen
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.children = []

    def draw(self):

        if not self.screen:
            return

        for child in self.children:
            child.draw()

        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height), 0)


class MenuButton(Menu):
    """Menu button

        **command accepts a callable or a callable and a parameter as a list
    """

    def __init__(self, screen, color, pos, size, text='', highlight_color=None, command=None):
        super().__init__(screen, color, pos, size)
        self.text = text
        self.orig_color = color
        self.highlight_color = highlight_color
        self.command = command
        pygame.font.init()

    def perform_action(self):
        """Calls command with possible argument"""
        if self.command:
            if not callable(self.command):
                partial(self.command[0])(self.command[1])
            else:
                partial(self.command)()

    def draw(self):

        self.mouse_over(pygame.mouse.get_pos())

        super().draw()

        if self.text:
            font = pygame.font.SysFont(
                'Verdana, Segoe UI, Arial, Playbill, Bauhaus 93, Showcard Gothic', int(self.height * 0.75))
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                                    self.y + (self.height/2 - text.get_height()/2)))

    def mouse_over(self, mouse_pos):

        if not pygame.mouse.get_focused():
            self.color = self.orig_color
            return

        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
                self.color = self.highlight_color
                self.perform_action()
                return True
        self.color = self.orig_color
        return False
