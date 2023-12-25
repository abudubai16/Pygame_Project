import pygame
import elements


class Board:
    left_shift = 150
    down_shift = 0
    color_board = 'Black'
    pin_color_1 = 'Red'
    pin_color_2 = 'Yellow'

    def __init__(self, screen):
        self.screen = screen
        self.red_pin = pygame.image.load('graphics/Red_pin.png')
        self.yellow_pin = pygame.image.load('graphics/Yellow_pin.png')
        self.turn_text = pygame.font.Font("font/Lost Emerald.otf", 40)
        self.watermark = pygame.font.Font("font/Lost Emerald.otf", 18).render('Connect 4', False, '#000000')
        self.creators = pygame.font.Font("font/Lost Emerald.otf", 18).render('Abhyuday & Pawan', False, '#000000')
        self.watermark_rect = self.watermark.get_rect(center=(950, 30))
        self.board_image = pygame.image.load('graphics/board.png').convert_alpha()
        self.board_image = pygame.transform.scale_by(self.board_image, 0.5)

    def set_shift(self, left_shift, down_shift):    # shifts from the center of the screen
        self.left_shift = left_shift
        self.down_shift = down_shift

    def set_board_color(self, color):
        self.color_board = color

    def set_pin_color(self, color1, color2):
        self.pin_color_1 = color1
        self.pin_color_2 = color2

    def draw_board(self):  # draws the board image first
        self.screen.blit(self.board_image, (325 + self.left_shift, 150 + self.down_shift))
        for i in range(7):  # draws the rest of the lines over the board
            pygame.draw.line(self.screen,
                             self.color_board,
                             (325 + self.left_shift, 450 - 50 * i + self.down_shift),
                             (675 + self.left_shift, 450 - 50 * i + self.down_shift))
        for i in range(8):
            pygame.draw.line(self.screen,
                             self.color_board,
                             (325 + 50 * i + self.left_shift, 450 + self.down_shift),
                             ((325 + 50 * i + self.left_shift), 150 + self.down_shift))

    def draw_text(self, player_turn):
        if player_turn % 2 == 1:
            player_text = self.turn_text.render("Red to play!!!", False, 'Red')
            text_outline = self.turn_text.render("Red to play!!!", False, '#000000')
        else:
            player_text = self.turn_text.render("Yellow to play!!!", False, 'Yellow')
            text_outline = self.turn_text.render("Yellow to play!!!", False, '#000000')

        x = 650
        y = 500
        scale = 1
        player_rect = player_text.get_rect(center=(x, y))
        corners = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for corner in corners:
            outline_rect = text_outline.get_rect(center=(x - scale*corner[0], y - scale*corner[1]))
            self.screen.blit(text_outline, outline_rect)
        self.screen.blit(self.creators, (840, 2))
        self.screen.blit(player_text, player_rect)
        self.screen.blit(self.watermark, self.watermark_rect)

    def fill_board(self, positions_red, positions_yellow):

        pin = pygame.Surface((50, 50))
        for points in positions_red:
            x, y = points
            pin.fill(self.pin_color_1)
            self.screen.blit(self.red_pin,
                             (x * 50 + 325 + self.left_shift, 450 - 50 * y + self.down_shift))

        for points in positions_yellow:
            x, y = points
            pin.fill(self.pin_color_2)
            self.screen.blit(self.yellow_pin,
                             (x * 50 + 325 + self.left_shift, 450 - 50 * y + self.down_shift))

    def draw_game(self, positions_red, positions_yellow):
        self.fill_board(positions_red, positions_yellow)
        self.draw_board()


class SidePanel:
    surface = pygame.Surface((300, 600))
    rect = surface.get_rect(topleft=(0, 0))
    action_type = 0

    def __init__(self, screen):
        self.screen = screen

        # buttons
        self.button_image = pygame.image.load('graphics/Button.png').convert_alpha()
        self.back_button = elements.ButtonText((150, 100), 1, self.button_image, "Back", 25)
        self.reset_button = elements.ButtonText((150, 300), 1, self.button_image, "Reset", 25)
        self.undo_button = elements.ButtonText((150, 500), 1, self.button_image, "Undo", 25)

    def draw(self):
        self.screen.blit(self.surface, self.surface.fill('Grey'))
        pygame.draw.line(self.screen, 'Black', (295, 0), (295, 600))
        pygame.draw.line(self.screen, 'Black', (300, 0), (300, 600))

        if self.back_button.draw_text(self.screen):
            self.action_type = 1

        if self.reset_button.draw_text(self.screen):
            self.action_type = 2

        if self.undo_button.draw_text(self.screen):
            self.action_type = 3

        return self.action_type

    def decrease_transparency(self):
        self.undo_button.set_transparency(50)
        self.reset_button.set_transparency(50)

    def increase_transparency(self):
        self.undo_button.set_transparency(100)
        self.reset_button.set_transparency(100)
