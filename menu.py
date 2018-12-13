import pygame
from functools import partial


class MenuBar():
    """Top menu bar"""

    def __init__(self, screen, color=[0, 80, 60], pos=[0, 0], size=[512, 32]):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.children = []
        self.open_menu = None
        self.hovered_menu = None
        self.hover_child = None
        pygame.font.init()

    def update(self):

        self.check_hover()
        self.draw()

    def check_hover(self):

        mouse_pos = pygame.mouse.get_pos()

        # When mouse is outside window, reset hover child
        if not pygame.mouse.get_focused():

            if self.hover_child:
                self.hover_child.hover = False

            self.hover_child = None

            self.close_menus()
            return

        # Find child under cursor
        for child in self.children:
            if mouse_pos[0] > child.pos[0] and mouse_pos[0] < child.pos[0] + child.size[0]:
                if mouse_pos[1] > child.pos[1] and mouse_pos[1] < child.pos[1] + child.size[1]:
                    self.hover_child = child
                    child.hover = True

                    # if child.children:
                    #     self.open_menu = child
                    # else:
                    #     self.open_menu = child.parent
                    continue
            child.hover = False

    def draw(self):
        """Draws self and calls draw on children"""
        if not self.screen:
            return

        pygame.draw.rect(self.screen, self.color,
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0)

        for child in self.children:
            child.draw()

    def process_click(self):

        for child in self.children:
            if child.hover:
                child.get_clicked()
                break
        else:
            self.close_menus()

    def close_menus(self):
        if self.open_menu:
            self.open_menu.close()
            self.open_menu = None

    def add_menu(self, text='', command=None):
        menu_size = (int(self.size[0] / 4), self.size[1])
        menu = Menu(self, self.screen, (100, 100, 20),
                    self.pos.copy(), menu_size, text=text, highlight_color=(150, 150, 70), click_color=(200, 200, 100), command=command)

        menu.pos[0] = self.pos[0] + len(self.children) * menu_size[0]

        self.children.append(menu)
        return menu


class Menu():
    """Menu parent"""

    def __init__(self, parent, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None):
        self.parent = parent
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.text = text
        self.orig_color = color
        self.highlight_color = highlight_color if highlight_color != None else color
        self.click_color = click_color if click_color != None else color
        self.command = command
        self.flash_duration = 5  # How many screen refreshes is the click color shown
        self.click_timer = self.flash_duration
        self.children = []
        self.hover = False

    def draw(self):
        """Draws self and calls draw on children"""

        self.click_timer -= 1

        if not self.screen:
            return

        if self.hover:
            if self.click_timer > 0:  # Recently clicked
                self.color = self.click_color
            else:
                self.color = self.highlight_color
        else:
            self.color = self.orig_color

        pygame.draw.rect(self.screen, (self.color),
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0)

        for child in self.children:
            if child.is_active:
                child.draw()

        if self.text:
            font = pygame.font.SysFont(
                'Verdana, Segoe UI, Arial', int(self.size[1] * 0.75))
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(text, (self.pos[0] + (self.size[0]/2 - text.get_width()/2),
                                    self.pos[1] + (self.size[1]/2 - text.get_height()/2)))

    def get_clicked(self):

        if self.parent.open_menu:
            if self.parent.open_menu != self:
                self.parent.open_menu.close()
                self.open()
            else:
                self.parent.open_menu.close()
        else:
            self.click_timer = self.flash_duration  # Reset click timer
            self.open()

        if self.command:
            if not callable(self.command):
                partial(self.command[0])(self.command[1])
            else:
                partial(self.command)()

    def open(self):
        self.parent.open_menu = self
        for child in self.children:
            child.is_active = True

    def close(self):
        self.parent.open_menu = None
        for child in self.children:
            child.is_active = False

    def add_item(self, text='', command=None):
        item = MenuItem(self, self.screen, self.color, self.pos.copy(),
                        self.size, text=text, highlight_color=self.highlight_color, command=command)

        item.pos[1] = self.pos[1] + (item.size[1] * (len(self.children) + 1))
        item.parent = self
        self.children.append(item)
        self.parent.children.append(item)
        return item


class MenuItem(Menu):

    def __init__(self, parent, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None):
        super().__init__(parent, screen, color, pos, size, text=text,
                         highlight_color=highlight_color, click_color=click_color, command=command)
        self.is_active = False

    def get_clicked(self):

        if not self.is_active:
            return

        if self.command:
            if not callable(self.command):
                partial(self.command[0])(self.command[1])
            else:
                partial(self.command)()

        self.parent.close()

    def draw(self):
        """Draws self"""

        if not self.screen or not self.is_active:
            return

        if self.hover:
            self.color = self.highlight_color
        else:
            self.color = self.orig_color

        pygame.draw.rect(self.screen, (self.color),
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0)

        if self.text:
            font = pygame.font.SysFont(
                'Verdana, Segoe UI, Arial', int(self.size[1] * 0.75))
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(text, (self.pos[0] + (self.size[0]/2 - text.get_width()/2),
                                    self.pos[1] + (self.size[1]/2 - text.get_height()/2)))


# class Menu():
#     """Menu parent"""

#     active_menu = []

#     def __init__(self, screen, color, pos, size):
#         self.screen = screen
#         self.color = color
#         self.x = pos[0]
#         self.y = pos[1]
#         self.width = size[0]
#         self.height = size[1]
#         self.children = []

#     def process_click(self):
#         for child in self.children:
#             child.get_clicked()

#     def draw(self):
#         """Draws menu object on screen and calls draw on its children objects"""
#         if not self.screen:
#             return

#         pygame.draw.rect(self.screen, self.color,
#                          (self.x, self.y, self.width, self.height), 0)

#         for child in self.children:
#             child.draw()

#     def add_menu_button(self, color=(208, 208, 208), size=(128, 32), text='', highlight_color=(240, 240, 240), click_color=(255, 255, 255), command=None, h_layout=True):
#         """Adds menu button as a child"""
#         button = MenuButton(self.screen, color,
#                             (self.x, self.y), size, text=text, highlight_color=highlight_color, click_color=click_color, command=command, h_layout=h_layout, parent=self)
#         self.children.append(button)

#         # Sort children vertically or horizontally based on h_layout
#         for index, child in enumerate(self.children):
#             if h_layout:
#                 child.x = self.x + (child.width * index)
#                 child.is_active = True
#             else:
#                 child.y = self.y + (child.height * (index + 1))
#         return button


# class MenuButton(Menu):
#     """Menu button

#         **command accepts a callable or a callable and a parameter as a list
#     """

#     def __init__(self, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None, h_layout=True, parent=None):
#         super().__init__(screen, color, pos, size)
#         self.text = text
#         self.orig_color = color
#         self.highlight_color = highlight_color if highlight_color != None else color
#         self.click_color = click_color if click_color != None else color
#         self.command = command
#         self.hover = False  # Is mouse over self
#         self.flash_duration = 5  # How many screen refreshes is the click color shown
#         self.click_timer = self.flash_duration
#         self.h_layout = h_layout  # Whether children are ordered horizontally or vertically
#         self.is_active = False  # Should we be shown
#         self.parent = parent
#         pygame.font.init()

#     def get_clicked(self):
#         """Calls command with possible argument"""

#         if self.hover:

#             if self not in Menu.active_menu:
#                 self.close_menu()
#             # If we are last child in menu tree, self and siblings inactive
#             if not self.children:
#                 self.close_menu()
#             # If we are top menu button, set children active
#             else:
#                 self.open_menu()
#             # Call command if we have one
#             if self.command:
#                 print('click', id(self))
#                 if not callable(self.command):
#                     self.click_timer = self.flash_duration  # Reset click timer
#                     partial(self.command[0])(self.command[1])
#                 else:
#                     partial(self.command)()
#         # Recurse click to check if a child is hovered
#         else:
#             for child in self.children:
#                 child.get_clicked()

#     def draw(self):

#         self.click_timer -= 1

#         if not self.is_active:
#             return

#         self.hover = self.mouse_over()

#         if self.hover:
#             if self.click_timer > 0:  # Recently clicked
#                 self.color = self.click_color
#             else:
#                 self.color = self.highlight_color
#         else:
#             self.color = self.orig_color

#         pygame.draw.rect(self.screen, self.color,
#                          (self.x, self.y, self.width, self.height), 0)

#         for child in self.children:
#             child.draw()

#         if self.text:
#             font = pygame.font.SysFont(
#                 'Verdana, Segoe UI, Arial, Playbill, Bauhaus 93, Showcard Gothic', int(self.height * 0.75))
#             text = font.render(self.text, 1, (0, 0, 0))
#             self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
#                                     self.y + (self.height/2 - text.get_height()/2)))

#     def mouse_over(self):
#         mouse_pos = pygame.mouse.get_pos()
#         if not pygame.mouse.get_focused():
#             self.color = self.orig_color
#             return False

#         if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
#             if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
#                 #print('mouse over: ', id(self))
#                 return True
#         return False

#     def open_menu(self):
#         # self.close_menu()
#         Menu.active_menu = [child for child in self.children]
#         Menu.active_menu.append(self)
#         for item in Menu.active_menu:
#             item.is_active = True

#     def close_menu(self):
#         for item in Menu.active_menu[:-1]:
#             item.is_active = False
#         Menu.active_menu = []
