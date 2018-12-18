import pygame
from functools import partial


class MenuBar():
    """Menu bar with menu objects as children"""

    def __init__(self, screen, color=[255, 178, 102], pos=[0, 0], size=[512, 32]):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.children = []
        self.open_menu = None
        self.hovered_menu = None
        self.hover_child = None
        self.cached_hover = None
        pygame.font.init()

    def update(self):

        self.check_hover()
        self.draw()

    def check_hover(self):
        """Find a child that has mouse over itself"""

        # When mouse is outside window, reset hover child
        if not pygame.mouse.get_focused():
            if self.hover_child:
                self.hover_child.hover = False
                self.hover_child = None
            return

        mouse_pos = pygame.mouse.get_pos()

        # Find child under cursor
        for child in self.children:
            if mouse_pos[0] > child.pos[0] and mouse_pos[0] < child.pos[0] + child.size[0]:
                if mouse_pos[1] > child.pos[1] and mouse_pos[1] < child.pos[1] + child.size[1]:
                    self.hover_child = child
                    child.hover = True
                    # If a menu has been clicked open but cursor is over another menu, open that one with a click
                    if self.open_menu and self.open_menu != child and child.children:  # Has children, i.e. is a top menu
                        child.get_clicked()
                    continue
            child.hover = False

    def draw(self):
        """Draws self and calls draw on children"""
        if not self.screen:
            return

        pygame.draw.rect(self.screen, self.color,
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0)

        for child in self.children:
            if child.is_active:
                child.draw()

    def process_click(self):
        """Calls click on a children

        Finds out if a child has hover and calls click on it. If not, closes all open menus.
        Returns True if a click hit a menu object, False otherwise."""

        if self.hover_child:
            if self.hover_child.is_active:
                self.hover_child.get_clicked()
                return True
            self.hover_child.get_clicked()

        else:
            self.close_menus()
            return False

    def close_menus(self):
        """Close the currently open menu"""
        if self.open_menu:
            self.open_menu.close()
            self.open_menu = None

    def get_child_size(self):
        """Gets a size for top menus, 25% of own size or at least 64px"""
        width = max(int(self.size[0] / 4), 64)
        height = self.size[1]

        return (width, height)

    def resize_width(self, new_width=512):
        """Scale self and all children menu objects to a new width"""
        self.size = [new_width, self.size[1]]
        child_size = self.get_child_size()

        longest_child = None

        for child in self.children:
            child.size = child_size
            if not longest_child or len(child.text) > len(longest_child.text):
                longest_child = child

        font = longest_child.get_font()

        for index, child in enumerate(self.children):

            if type(child) is Menu:
                child.pos[0] = self.pos[0] + (child.size[0] * index)
                child.set_menu_text(font)
                for grand_child in child.children:
                    grand_child.pos[0] = self.pos[0] + \
                        (grand_child.size[0] * index)
                    grand_child.set_menu_text(font)

    def add_menu(self, text='', command=None):
        """Creates a menu and sorts it horizontally with existing ones"""
        child_size = self.get_child_size()
        menu = Menu(self, self.screen, (255, 178, 102),
                    self.pos.copy(), child_size, text=text, highlight_color=(255, 204, 153), click_color=(255, 229, 204), command=command)

        menu.pos[0] = self.pos[0] + len(self.children) * child_size[0]

        self.children.append(menu)
        self.resize_width()
        return menu


class Menu():
    """Menu parent object with menu items as children"""

    def __init__(self, parent, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None):
        self.parent = parent
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.text = text
        self.menu_text = None
        self.orig_color = color
        self.highlight_color = highlight_color if highlight_color != None else color
        self.click_color = click_color if click_color != None else color
        self.command = command
        self.flash_duration = 30  # How many screen refreshes is the click color shown
        self.click_timer = self.flash_duration
        self.children = []
        self.hover = False
        self.is_active = True
        self.selected_child = None

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

        if self.text:
            self.screen.blit(self.menu_text, (self.pos[0] + (self.size[0]/2 - self.menu_text.get_width()/2),
                                              self.pos[1] + (self.size[1]/2 - self.menu_text.get_height()/2)))

    def set_menu_text(self, font):
        self.menu_text = font.render(self.text, 1, (51, 25, 0))

    def get_font(self):
        """Finds the biggest possible font for self.text to fit in the rect"""
        font = pygame.font.SysFont(
            'Verdana', self.size[1])

        reduction = 1
        while font.size(self.text)[1] + 1 > self.size[1] or font.size(self.text)[0] + 1 > self.size[0]:
            font = pygame.font.SysFont(
                'Verdana', (self.size[1]) - reduction)
            reduction += 1
        return font

    def get_clicked(self):
        """Flash button and call the command"""

        # If there is an open menu and it is not self, make self the open menu, otherwise close self
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
                partial(self.command[0])(*self.command[1:])
            else:
                partial(self.command)()

    def open(self):
        """Mark self as the open menu in parent and activate all children"""
        self.parent.open_menu = self
        for child in self.children:
            child.is_active = True

    def close(self):
        """Remove parent's open menu and deactivate all children"""
        self.parent.open_menu = None
        for child in self.children:
            child.is_active = False

    def add_item(self, text='', command=None, selected=False):
        """Adds a menu item and sorts it vertically with others"""
        item = MenuItem(self, self.screen, self.color, self.pos.copy(),
                        self.size, text=text, highlight_color=self.highlight_color, command=command, selected=selected)

        item.pos[1] = self.pos[1] + (item.size[1] * (len(self.children) + 1))
        item.parent = self
        self.children.append(item)
        self.parent.children.append(item)
        self.parent.resize_width()
        return item


class MenuItem(Menu):

    def __init__(self, parent, screen, color, pos, size, text='', highlight_color=None, click_color=None, command=None, selected=False):
        super().__init__(parent, screen, color, pos, size, text=text,
                         highlight_color=highlight_color, click_color=click_color, command=command)
        self.is_active = False
        if selected:
            self.get_selected()

    def get_clicked(self):
        """Calls command and closes parent menu"""

        if not self.is_active:
            return

        if self.command:
            if not callable(self.command):
                partial(self.command[0])(*self.command[1:])
            else:
                partial(self.command)()

        self.parent.close()

        self.get_selected()

    def draw(self):
        """Draws self"""

        if self.hover:
            self.color = self.highlight_color
        else:
            self.color = self.orig_color

        pygame.draw.rect(self.screen, (self.color),
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0)

        if self.text:
            self.screen.blit(self.menu_text, (self.pos[0] + (self.size[0]/2 - self.menu_text.get_width()/2),
                                              self.pos[1] + (self.size[1]/2 - self.menu_text.get_height()/2)))

        if self.parent.selected_child == self:
            pygame.draw.rect(self.screen, (153, 76, 0),
                             (self.pos[0] + 1, self.pos[1] + 1, self.size[0] - 2, self.size[1]-2), 1)

    def get_selected(self):
        self.parent.selected_child = self
