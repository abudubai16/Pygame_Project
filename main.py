import pygame
import elements
import utility
import board
import music


class GameActive:
    # lists
    positions_red = []
    positions_yellow = []
    height = [0, 0, 0, 0, 0, 0, 0]

    winner = 'No one'
    player_turn = 1
    action = False
    refresh_rate = 60
    locations = []

    def __init__(self, game_state):
        self.game_state = game_state
        self.board_element = board.Board(screen)

        # backgrounds
        self.game_background = pygame.image.load('graphics/game_background.jpg').convert_alpha()
        self.button_image = pygame.image.load('graphics/Button.png').convert_alpha()
        self.intro_background = pygame.image.load('graphics/Intro_background.jpg').convert_alpha()
        self.win_background = pygame.image.load('graphics/Win.jpg').convert_alpha()

    def falling_animation(self, location):
        positions_red = self.positions_red
        positions_yellow = self.positions_yellow

        if self.player_turn % 2 == 0:
            pin = self.board_element.yellow_pin
            positions_yellow = self.positions_yellow[:-1]
        else:
            pin = self.board_element.red_pin
            positions_red = self.positions_red[:-1]

        x = location[0] * 50 + 325 + self.board_element.left_shift
        y = 0 + self.board_element.down_shift
        gravity = 0

        panel = board.SidePanel(screen)

        while y <= 450 - location[1] * 50:
            utility.check_exit()

            y += gravity
            gravity += 0.5
            screen.blit(pin, (x, y // 1))

            self.board_element.draw_game(positions_red, positions_yellow)
            self.board_element.draw_text(self.player_turn)

            pygame.display.update()
            screen.blit(self.game_background, (0, 0))
            panel.draw()
            clock.tick(60)
        else:
            music.pin_falling()

    def undo(self):
        if self.player_turn % 2 == 1 and len(self.positions_yellow) != 0:  # it was yellows turn
            self.player_turn -= 1
            self.positions_yellow.pop()
            self.height[self.locations.pop()] -= 1
            return

        if self.player_turn % 2 == 0 and len(self.positions_red) != 0:  # it was reds turn
            self.player_turn -= 1
            self.positions_red.pop()
            self.height[self.locations.pop()] -= 1

    def user_input_0(self, positions):
        self.action = False
        keys = pygame.key.get_pressed()
        a = [pygame.K_1,
             pygame.K_2,
             pygame.K_3,
             pygame.K_4,
             pygame.K_5,
             pygame.K_6,
             pygame.K_7
             ]

        for i in range(7):
            if keys[a[i]] and self.height[i] < 6:
                self.locations.append(i)
                self.height[i] += 1
                pygame.time.delay(250)
                positions.append((i, self.height[i]))
                self.falling_animation(positions[-1])
                self.player_turn += 1
                self.action = True

        return positions

    def game_restart(self):
        self.positions_red = []
        self.positions_yellow = []
        self.height = [0, 0, 0, 0, 0, 0, 0]
        self.winner = 'No one'
        self.player_turn = 1
        self.locations = []

    def game_state_0(self):
        # side panel
        side_panel = board.SidePanel(screen)

        while True and self.game_state == 0:
            utility.check_exit()

            if (len(self.positions_red) + len(self.positions_yellow)) == 42:

                self.game_state = 1
                continue

            if len(self.locations) == 0:
                side_panel.decrease_transparency()
            else:
                side_panel.increase_transparency()

            action_type = side_panel.draw()
            if action_type == 1:
                self.game_state = 2
                continue
            if action_type == 2:
                self.game_restart()
                return
            if action_type == 3:
                self.undo()
                break

            if self.player_turn % 2:
                self.positions_red = self.user_input_0(self.positions_red)
            else:
                self.positions_yellow = self.user_input_0(self.positions_yellow)

            if len(self.positions_red) > 0 and utility.check_win(self.positions_red) and self.action:
                self.game_state = 1
                self.winner = 'Player 1'
                self.action = False
                continue

            if len(self.positions_yellow) > 0 and utility.check_win(self.positions_yellow) and self.action:
                self.game_state = 1
                self.winner = 'Player 2'

            self.board_element.draw_game(self.positions_red, self.positions_yellow)
            self.board_element.draw_text(self.player_turn)
            self.action = False

            pygame.display.update()
            screen.blit(self.game_background, (0, 0))
            clock.tick(self.refresh_rate)

    def game_state_1(self):
        # text
        end_font = pygame.font.Font("font/Lost Emerald.otf", 50)
        surface_font1 = end_font.render(f"{self.winner} wins the game!!!", False, '#000000')
        end_rect2 = surface_font1.get_rect(center=(500, 150))

        end_font = pygame.font.Font("font/Lost Emerald.otf", 30)
        surface_font2 = end_font.render("Press Space to restart game!!!", False, '#000000')
        end_rect1 = surface_font2.get_rect(center=(500, 200))

        # buttons
        button_image = pygame.image.load('graphics/Button.png')
        button1 = elements.ButtonText((500, 330), 1, button_image, "Intro Screen", 25)
        button2 = elements.ButtonText((500, 480), 1, button_image, 'Exit Game', 25)

        while True and self.game_state == 1:
            utility.check_exit()

            if button1.draw_text(screen):
                self.game_state = 2
                pygame.time.delay(100)

            if button2.draw_text(screen):
                pygame.quit()
                exit()

            screen.blit(surface_font1, end_rect2)
            screen.blit(surface_font2, end_rect1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_restart()
                self.game_state = 0
                break

            pygame.display.update()
            screen.blit(self.win_background, (0, 0))
            clock.tick(60)

    def game_state_2(self):
        # text
        text_font = pygame.font.Font('font/Lost Emerald.otf', 80)
        surface_font = text_font.render("Connect 4", False, '#FFFFFF', 80)
        rect_font = surface_font.get_rect(center=(500, 80))

        # buttons
        scale = 1.05
        image_button = pygame.image.load('graphics/Button.png')
        new_game_button = elements.ButtonText((500, 200), scale, image_button, "New Game", 25)
        continue_game_button = elements.ButtonText((500, 350), scale, image_button, 'Continue Game', 25)
        exit_button = elements.ButtonText((500, 500), scale, image_button, 'Exit', 25)

        while True and self.game_state == 2:
            utility.check_exit()
            screen.blit(surface_font, rect_font)

            if not len(self.positions_red) > 0:  # checks if whether a game already exists
                continue_game_button.set_transparency(50)
            else:
                continue_game_button.set_transparency(255)

            if new_game_button.draw_text(screen):
                self.game_restart()
                self.game_state = 0

            if continue_game_button.draw_text(screen):
                self.game_state = 0

            if exit_button.draw_text(screen):
                pygame.quit()
                exit()

            pygame.display.update()
            screen.blit(self.intro_background, (0, 0))
            clock.tick(self.refresh_rate)

    def game_state_3(self):
        # button
        button_image = pygame.image.load('graphics/Button.png').convert_alpha()
        button1 = elements.ButtonText((500, 300), 1, button_image, 'Back', 25)

        # slider

        while self.game_state == 3:
            utility.check_exit()

            if button1.draw_text(screen):
                self.game_state = 2

            pygame.display.update()
            screen.blit(self.intro_background, (0, 0))
            clock.tick(self.refresh_rate)

    def game_driver(self):

        while True:
            utility.check_exit()

            if self.game_state == 0:  # game screen
                self.game_state_0()

            if self.game_state == 1:  # win screen
                self.game_state_1()
                self.game_restart()

            if self.game_state == 2:  # intro screen
                self.game_state_2()

            if self.game_state == 3:  # settings screen
                self.game_state_3()

            if self.game_state == -1:
                self.game_restart()

            clock.tick(self.refresh_rate)


try:
    pygame.init()
    game_icon = pygame.image.load('graphics/game_icon.png')
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Connect 4")
    pygame.display.set_icon(game_icon)
    clock = pygame.time.Clock()

    game = GameActive(game_state=2)
    game.game_driver()

except ValueError:
    pygame.quit()
    utility.error_handling()
