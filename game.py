import pygame
import cursor
from maps import Map
from character import Character
from menu import MenuBar, Menu, MenuItem

app_width = 512  # Start width
app_height = 512  # Start height
screen = None
current_map = None
tile_size = 32
diagonal_move = False


def set_current_map(new_map):
    """Set new map as current after clearing old one's character list."""
    global current_map
    try:
        for char in current_map.character_list:
            del char
    except Exception:
        pass

    current_map = new_map


def init_map(map_name):
    """Initialize map

    Creates Map object, game window, sets references and globals and adds character.
    """
    global screen
    global tile_size
    global diagonal_move
    map = Map(map_name, tile_size, diagonal_movement=diagonal_move)
    map_size = map.get_size()
    create_screen(map_size)
    map.set_screen(screen)
    set_current_map(map)
    add_character()


def flash_pos(pos):
    """Flash a position on map"""
    flash_size = current_map.cell_size
    flash_color = (255, 0, 0)
    current_map.get_pos(pos)
    rect = pygame.Rect(pos[0]*flash_size, pos[1] *
                       flash_size, flash_size, flash_size)

    pygame.draw.rect(screen, flash_color, rect)


def mark_positions(pos_list):
    """Mark list specified positions with a red circle"""
    for pos in pos_list:
        x_pos = pos[0]*current_map.cell_size + current_map.cell_size // 2
        y_pos = pos[1] * current_map.cell_size + current_map.cell_size // 2
        size = current_map.cell_size // 8
        pygame.draw.circle(screen, (255, 0, 0, 100), (x_pos, y_pos), size)


def add_character():
    global current_map
    global screen
    char = Character('wizard.png', (5, 1), current_map, screen)


def create_screen(screen_size):
    """Create Pygame screen."""
    global screen
    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    draw_empty_screen()


def draw_empty_screen():
    screen.fill(pygame.Color(31, 31, 31))


def resize_tiles(size):
    """Resize tiles and apply changes to map and character"""
    global current_map
    global tile_size
    if size == tile_size:
        return

    tile_size = size

    if current_map:
        current_map.cell_size = size
        pygame.display.set_mode(current_map.get_size())
        current_map.character_list[0].scale_image()
        main_menu.resize_width(new_width=current_map.get_size()[0])


def toggle_diagonal(diagonal):
    global diagonal_move
    diagonal_move = diagonal
    if current_map:
        current_map.pathfind_grid.diagonal_movement = diagonal


# Initialize
create_screen((app_width, app_height))
pygame.display.set_caption('Grid Game')
icon = pygame.image.load('images/wizard.png')
pygame.display.set_icon(icon)
cursor.create_cursor()
main_menu = MenuBar(screen, size=[app_width, tile_size])
menu0 = main_menu.add_menu('Maps')
menu1 = main_menu.add_menu('Tiles')
menu2 = main_menu.add_menu('Settings')
map01 = menu0.add_item('Map1', command=(init_map, 'map1'))
map02 = menu0.add_item('Map2', command=(init_map, 'map2'))
map03 = menu0.add_item('Map3', command=(init_map, 'map3'))
tile16 = menu1.add_item('16px', command=(resize_tiles, 16))
tile16 = menu1.add_item('32px', command=(resize_tiles, 32))
tile16 = menu1.add_item('48px', command=(resize_tiles, 48))
tile16 = menu1.add_item('64px', command=(resize_tiles, 64))
diag_on = menu2.add_item('Diagonal on', command=(toggle_diagonal, True))
diag_off = menu2.add_item('Diagonal off', command=(toggle_diagonal, False))


def handle_kb_input():
    """Keyboard input handler"""
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


def handle_mouse_input():
    """Directs click to either menu system or character movement"""
    if main_menu.process_click():
        return
    try:
        mouse_tile_pos = (pygame.mouse.get_pos()[
            0] // current_map.cell_size, pygame.mouse.get_pos()[1] // current_map.cell_size)
        flash_pos(mouse_tile_pos)
        current_map.character_list[0].find_path_to(mouse_tile_pos)
    except AttributeError:
        pass


# Main loop
running = True

while running:
    if current_map:
        current_map.draw()
        for char in current_map.character_list:
            char.move(16)
            mark_positions(char.move_sequence)
    else:
        draw_empty_screen()

    main_menu.update()

    handle_kb_input()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            handle_mouse_input()
