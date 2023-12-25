import pygame


class ButtonImage:
    transparency = 255 

    def __init__(self, position, scale, image):
        self.width = image.get_width()
        self.height = image.get_height()
        self.position = position
        self.image = pygame.transform.scale(image, (int(self.width*scale), int(self.height*scale)))
        self.rect = self.image.get_rect(center=self.position)
        self.mouse_pressed = False
        self.time_pressed = 0

    def draw(self, screen):
        action = False

        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()) and self.transparency > 200:
            scale = 0.99
            image = pygame.transform.scale(self.image, (int(self.width*scale), int(self.height*scale)))
            pygame.Surface.set_alpha(image, self.transparency)
            self.rect = image.get_rect(center=self.position)

            if pygame.mouse.get_pressed()[0]:
                self.mouse_pressed = True
                self.time_pressed = pygame.time.get_ticks()

            if self.mouse_pressed and pygame.time.get_ticks()-self.time_pressed > 10:
                action = True

        else:
            pygame.Surface.set_alpha(self.image, self.transparency)
            self.rect = self.image.get_rect(center=self.position)

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def set_transparency(self, percentage):
        self.transparency = int(percentage / 100 * 255)


class ButtonText(ButtonImage):
    color = 'Black'

    def __init__(self, position, scale, image, text, size):
        super().__init__(position, scale, image)
        self.text = text
        self.size = size

    def set_color(self, color):
        self.color = color

    def draw_text(self, screen):
        font_type = pygame.font.Font('font/Lost Emerald.otf', self.size)

        text_surface = font_type.render(self.text, False, self.size)
        if self.transparency < 200:
            pygame.Surface.set_alpha(text_surface, self.transparency)

        text_rect = text_surface.get_rect(center=self.position)
        action = self.draw(screen)
        screen.blit(text_surface, text_rect)
        return action


class Slider:
    color = 'Black'

    def __init__(self, position, size_block, length_slider, slider_thickness):
        self.position = position
        self.size_block = size_block
        self.length_slider = length_slider
        self.slider_thickness = slider_thickness

    def set_color(self, color):
        self.color = color

    def draw(self, screen):
        x, y = self.position
        image_slider = pygame.image.load('graphics/Button.png').convert_alpha()
        image_rect = image_slider.get_rect(center=(0, y))

        pygame.draw.line(screen,
                         self.color,
                         (int(x-self.length_slider/2), y),
                         (int(x-self.length_slider/2), y),
                         self.slider_thickness)

        mouse_position = pygame.mouse.get_pos()
        mouse_x_position = mouse_position[0]

        if int(x-self.length_slider/2) > mouse_x_position:
            image_rect.x = int(x-self.length_slider/2)
            screen.blit(image_slider, image_rect)
        elif mouse_x_position > int(x-self.length_slider/2):
            image_rect.x = int(x-self.length_slider/2)
            screen.blit(image_slider, image_rect)
        else:
            image_rect.x = mouse_x_position
            screen.blit(image_slider, image_rect)
