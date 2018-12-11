import pygame
import tkinter as tk
import os
import cursor
import numpy
from maps import Map
from character import Character
from menu import Menu, MenuButton

app_width = 512  # Start width
app_height = 512  # Start height
root = None
screen = None
embed = None
menu_bar = None
current_map = None
update_interval = 16  # How often(in ms) is screen refreshed


def set_current_map(new_map):
    """Set new map as current after clearing old one's character list."""
    global current_map
    try:
        for char in current_map.character_list:
            del char
    except Exception:
        pass

    current_map = new_map


def init_map(map_name, cell_size, diagonal_move=False):
    """Initialize map

    Creates Map object, embed, game window, sets references and globals and adds character.
    """
    global screen
    map = Map(map_name, cell_size, diagonal_movement=diagonal_move)
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
    global screen
    char = Character('wizard.png', (5, 1), current_map, screen)


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
        label="Create Map2, Cell size: 32x32, diagonal movement allowed", command=lambda: init_map('map2', 32, diagonal_move=True))
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


def test_func(text='default'):
    print('test', text)


# Initialize
root = tk.Tk()
create_window((app_width, app_height))
create_menu_bar()
set_sdl()
create_screen((app_width, app_height))
test_menu = Menu(screen, (208, 208, 208), (0, 0), (512, 32))
# test_button = MenuButton(screen, (16, 208, 24), (0, 0),
#                          (128, 32), "Test", highlight_color=(64, 255, 96), click_color=(128, 255, 192), command=(test_func, 'button 1'))
# test_button2 = MenuButton(screen, (16, 208, 24), (0, 0),
#                           (128, 32), "Test", highlight_color=(64, 255, 96), click_color=(128, 255, 192), command=(test_func, 'button 2'))
# test_menu.children.append(test_button)
# test_menu.children.append(test_button2)
# test_menu.add_menu_button((16, 208, 24), (128, 32), text="Test!", highlight_color=(
#     64, 255, 96), click_color=(128, 255, 192), command=(test_func, 'test btn 1'))
# test_menu.add_menu_button((208, 16, 24), (128, 32), text="Test2!", highlight_color=(
# 255, 64, 96), click_color=(255, 128, 192), command=(test_func, 'test btn 2'))
button_0 = test_menu.add_menu_button(
    text='Button 00', command=(test_func, 'new button 00'))
button_0_0 = button_0.add_menu_button(
    text='Button 01', command=(test_func, 'new button 01'), h_layout=False)
button_0_1 = button_0.add_menu_button(
    text='Button 02', command=(test_func, 'new button 02'), h_layout=False)

button_1 = test_menu.add_menu_button(
    text='Button 10', command=(test_func, 'new button 10'))
button_1_0 = button_1.add_menu_button(
    text='Button 11', command=(test_func, 'new button 11'), h_layout=False)
button_1_1 = button_1.add_menu_button(
    text='Button 12', command=(test_func, 'new button 12'), h_layout=False)


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
                test_menu.process_click()
                try:
                    mouse_tile_pos = (pygame.mouse.get_pos()[
                        0] // current_map.cell_size, pygame.mouse.get_pos()[1] // current_map.cell_size)
                    flash_pos(mouse_tile_pos)
                    current_map.character_list[0].find_path_to(mouse_tile_pos)
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
    global update_interval
    if current_map:
        current_map.draw()
        for char in current_map.character_list:
            char.move(update_interval)
            mark_positions(char.move_sequence)
    test_menu.draw()

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
