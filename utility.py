import pygame
from sys import exit


def check_list(list_name, value):
    for i in list_name:
        if i == value:
            return 1
    return 0


def check_win(positions):
    x, y = positions[-1]  # left and right
    counter = 0
    for i in range(3):
        if check_list(positions, (x - 1, y)):
            counter += 1
            x -= 1
        else:
            break
    x, y = positions[-1]
    for i in range(3):
        if check_list(positions, (x + 1, y)):
            counter += 1
            x += 1
        else:
            break
    if counter > 2:
        return True

    x, y = positions[-1]  # leading diagonal
    counter = 0
    for i in range(3):
        if check_list(positions, (x - 1, y + 1)):
            counter += 1
            x -= 1
            y += 1
        else:
            break
    x, y = positions[-1]
    for i in range(3):
        if check_list(positions, (x + 1, y - 1)):
            counter += 1
            x += 1
            y -= 1
        else:
            break
    if counter > 2:
        return True

    x, y = positions[-1]  # non-leading diagonal
    counter = 0
    for i in range(3):
        if check_list(positions, (x - 1, y - 1)):
            counter += 1
            x -= 1
            y -= 1
        else:
            break
    x, y = positions[-1]
    for i in range(3):
        if check_list(positions, (x + 1, y + 1)):
            counter += 1
            x += 1
            y += 1
        else:
            break
    if counter > 2:
        return True

    x, y = positions[-1]
    counter = 0
    for i in range(3):
        if check_list(positions, (x, y - 1)):
            counter += 1
            y -= 1
    if counter > 2:
        return True

    return False


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def error_handling():
    # to reset the size of the screen
    pygame.init()
    game_icon = pygame.image.load('graphics/game_icon.png')
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Connect 4")
    pygame.display.set_icon(game_icon)
    clock = pygame.time.Clock()

    # close the error screen automatically
    tick_start = pygame.time.get_ticks()

    # text
    end_font = pygame.font.Font("font/Lost Emerald.otf", 50)
    # end_font = end_font.render()

    while True:
        check_exit()
        tick_end = pygame.time.get_ticks()

        if tick_end - tick_start == 10000:
            pygame.quit()
            exit()

        screen.display.update()
        screen.fill('Grey')




