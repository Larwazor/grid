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

    def process_click(self, click_pos):
        # print(click_pos)

        for child in self.children:
            child.get_clicked()

    def draw(self):
        """Draws menu object on screen and calls draw on its children objects"""
        if not self.screen:
            return

        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height), 0)

        index = 0
        for child in self.children:
            child.x = self.x + (child.width * index)
            child.draw()
            index += 1


class MenuButton(Menu):
    """Menu button

        **command accepts a callable or a callable and a parameter as a list
    """

    def __init__(self, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None):
        super().__init__(screen, color, pos, size)
        self.text = text
        self.orig_color = color
        self.highlight_color = highlight_color if highlight_color != None else color
        self.click_color = click_color if click_color != None else color
        self.command = command
        self.hover = False
        self.flash_duration = 7  # How many screen refreshes is the click color shown
        self.click_timer = self.flash_duration
        pygame.font.init()

    def get_clicked(self):
        """Calls command with possible argument"""
        if self.command and self.hover:
            if not callable(self.command):
                self.click_timer = self.flash_duration  # Reset click timer
                partial(self.command[0])(self.command[1])
            else:
                partial(self.command)()

    def draw(self):

        self.click_timer -= 1

        self.hover = self.mouse_over(pygame.mouse.get_pos())

        if self.hover:
            if self.click_timer > 0:  # Recently clicked
                self.color = self.click_color
            else:
                self.color = self.highlight_color
        else:
            self.color = self.orig_color

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
                return True
        return False
