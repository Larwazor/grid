import pygame


def create_cursor():
    """
    Create cursor like Windows' default.
    """
    cursor, mask = pygame.cursors.compile(
        arrowz, black='X', white='.', xor='o')
    cursor_sizer = ((24, 24), (0, 0), cursor, mask)
    pygame.mouse.set_cursor(*cursor_sizer)


arrowz = (  # 24x24
    "X                       ",
    "XX                      ",
    "X.X                     ",
    "X..X                    ",
    "X...X                   ",
    "X....X                  ",
    "X.....X                 ",
    "X......X                ",
    "X.......X               ",
    "X........X              ",
    "X.........X             ",
    "X..........X            ",
    "X......XXXXX            ",
    "X...X..X                ",
    "X..X X..X               ",
    "X.X  X..X               ",
    "XX    X..X              ",
    "      X..X              ",
    "       XX               ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ")
