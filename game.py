import pygame
import tkinter as tk
import os
import cursor
import numpy
from maps import Map
from character import Character

app_width = 512  # Start width
app_height = 512  # Start height
root = None
screen = None
embed = None
menu_bar = None
current_map = None


def set_current_map(new_map):
    """Set new map as current after clearing old one's character list."""
    global current_map
    try:
        for char in current_map.character_list:
            del char
    except Exception:
        pass

    current_map = new_map


def init_map(map_name, cell_size):
    """Initialize map

    Creates Map object, embed, game window, sets references and globals and adds character.
    """
    global screen
    map = Map(map_name, cell_size)
    map_size = map.get_size()
    create_window(map_size)
    create_screen(map_size)
    map.set_screen(screen)
    set_current_map(map)
    add_character()


def mark_positions(pos_list):
    """Mark list specified positions with a red circle"""
    for pos in pos_list:
        x_pos = pos[0]*current_map.cell_size + current_map.cell_size // 2
        y_pos = pos[1] * current_map.cell_size + current_map.cell_size // 2
        size = current_map.cell_size // 8
        pygame.draw.circle(screen, (255, 0, 0, 100), (x_pos, y_pos), size)


def add_character():
    global current_map
    global character_list
    char = Character('wizard.png', (1, 1), current_map)


def create_window(window_size):
    """Create tkinter embed for Pygame window."""
    global root
    global embed

    window_width = window_size[0]
    window_height = window_size[1]

    # Set window pos on start
    if embed == None:
        root.geometry(f'{window_width}x{window_height}+300+100')

    root.minsize(window_width, window_height)
    root.maxsize(window_width, window_height)

    embed = tk.Frame(root, width=window_width, height=window_height)

    embed.pack(ipadx=window_width, ipady=window_height)


def create_menu_bar():
    """Create menu bar."""
    global root
    global menu_bar
    menu_bar = tk.Menu(root)
    options_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu.add_command(
        label="Create Map1, Cell size: 16x16", command=lambda: init_map('map1', 16))
    options_menu.add_command(
        label="Create Map2, Cell size: 32x32", command=lambda: init_map('map2', 32))
    options_menu.add_command(
        label="Create Map3, Cell size: 64x64", command=lambda: init_map('map3', 64))
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Options", menu=options_menu)


def set_sdl():
    global embed
    """Mysterious OS settings, latter seems obsolete nowadays."""
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'


def create_screen(screen_size):
    """Create Pygame screen."""
    global screen
    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    screen.fill(pygame.Color(31, 31, 31))


# Initialize
root = tk.Tk()
create_window((app_width, app_height))
create_menu_bar()
set_sdl()
create_screen((app_width, app_height))


# Create cursor to replace the awkward default one.
cursor.create_cursor()


def get_kb_input():
    kb_input = pygame.key.get_pressed()
    try:
        if kb_input[pygame.K_a]:
            current_map.character_list[0].move_to_direction(
                'w', clear_sequence=True)
        elif kb_input[pygame.K_d]:
            current_map.character_list[0].move_to_direction(
                'e', clear_sequence=True)
        elif kb_input[pygame.K_w]:
            current_map.character_list[0].move_to_direction(
                'n', clear_sequence=True)
        elif kb_input[pygame.K_s]:
            current_map.character_list[0].move_to_direction(
                's', clear_sequence=True)
        elif kb_input[pygame.K_g]:
            current_map.character_list[0].set_sequence(
                ((2, 1), (3, 1), (4, 1), (4, 2), (5, 2), (5, 3), (6, 3), (7, 3)))
        elif kb_input[pygame.K_j]:
            print(current_map.character_list[0].pos)
    except AttributeError:
        pass


def mouse_on_window():
    global embed
    mouse_x = root.winfo_pointerx() - root.winfo_rootx()
    mouse_y = root.winfo_pointery() - root.winfo_rooty()
    if mouse_x >= 0 and mouse_y >= 0:
        if mouse_x <= root.winfo_width() and mouse_y <= root.winfo_height():
            return True
    return False


def get_mouse_input():
    if mouse_on_window():
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                try:
                    mouse_pos = (pygame.mouse.get_pos()[
                        0] // current_map.cell_size, pygame.mouse.get_pos()[1] // current_map.cell_size)
                    flash_pos(mouse_pos)
                    current_map.character_list[0].find_path_to(mouse_pos)
                except AttributeError:
                    pass


def flash_pos(pos):
    flash_size = current_map.cell_size
    flash_color = (255, 0, 0)
    current_map.get_pos(pos)
    rect = pygame.Rect(pos[0]*flash_size, pos[1] *
                       flash_size, flash_size, flash_size)

    pygame.draw.rect(screen, flash_color, rect)


def game_loop():
    global character_list
    global root
    global current_map
    update_interval = 16
    try:
        current_map.draw()
        for char in current_map.character_list:
            char.move(update_interval)
            char.draw(screen)
            mark_positions(char.move_sequence)
    except Exception:
        pass

    get_kb_input()
    get_mouse_input()
    pygame.display.update()
    root.after(update_interval, game_loop)


# Tkinter Mainloop
root.resizable(False, False)
root.config(menu=menu_bar)
root.title('Grid Game')
img = tk.Image("photo", file="images/wizard.png")
root.wm_iconphoto(True, img)
game_loop()
root.mainloop()
