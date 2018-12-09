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

    def process_click(self):
        # print(click_pos)

        for child in self.children:
            child.get_clicked()

    def draw(self):
        """Draws menu object on screen and calls draw on its children objects"""
        if not self.screen:
            return

        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height), 0)

        for child in self.children:
            child.draw()

    def add_menu_button(self, color=(208, 208, 208), size=(128, 32), text='', highlight_color=(240, 240, 240), click_color=(255, 255, 255), command=None, h_layout=True):
        """Adds menu button as a child"""
        button = MenuButton(self.screen, color,
                            (self.x, self.y), size, text=text, highlight_color=highlight_color, click_color=click_color, command=command, h_layout=h_layout, parent=self)
        self.children.append(button)

        # Sort children vertically or horizontally based on h_layout
        for index, child in enumerate(self.children):
            if h_layout:
                child.x = self.x + (child.width * index)
                child.is_active = True
            else:
                child.y = self.y + (child.height * (index + 1))
        return button


class MenuButton(Menu):
    """Menu button

        **command accepts a callable or a callable and a parameter as a list
    """

    def __init__(self, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None, h_layout=True, parent=None):
        super().__init__(screen, color, pos, size)
        self.text = text
        self.orig_color = color
        self.highlight_color = highlight_color if highlight_color != None else color
        self.click_color = click_color if click_color != None else color
        self.command = command
        self.hover = False
        self.flash_duration = 5  # How many screen refreshes is the click color shown
        self.click_timer = self.flash_duration
        self.h_layout = h_layout
        self.is_active = False
        self.parent = parent
        pygame.font.init()

    def get_clicked(self):
        """Calls command with possible argument"""

        if self.hover:
            for child in self.children:
                child.is_active = True
            if self.command:
                if not callable(self.command):
                    self.click_timer = self.flash_duration  # Reset click timer
                    partial(self.command[0])(self.command[1])
                else:
                    partial(self.command)()
        else:
            for child in self.children:
                child.get_clicked()

    def draw(self):

        self.click_timer -= 1

        if not self.is_active:
            return

        self.hover = self.mouse_over(pygame.mouse.get_pos())

        if self.hover:
            if self.click_timer > 0:  # Recently clicked
                self.color = self.click_color
            else:
                self.color = self.highlight_color
        else:
            self.color = self.orig_color

        # child_hover = False
        # for child in self.children:
        #     if child.hover:
        #         child_hover = True
        #         print('child hover')
        #         # continue

        # for child in self.children:
        #     if child_hover or self.hover:
        #         child.is_active = True
        #     else:
        #         child.is_active = False

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
