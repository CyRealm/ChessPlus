import pygame
aspect_ratio = 0.9
rescaled_bg_img = pygame.transform.scale(pygame.image.load("assets/Main_bg.png"),  (1100 * aspect_ratio, 800 * aspect_ratio))

class Button():
    def __init__(self, image, text_input, font, base_colour, hovering_colour):
        self.image = image
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if self.image is None:
            self.image = self.text

    # Checking for mouse input
    def check_for_input(self, position):
        if self.image.collidepoint(position):
            return True
        return False

    # Font colour change when highlighted
    def change_colour(self, position):
        if self.image.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)
            
# Options screen
def options(screen):
    options_mouse_pos = pygame.mouse.get_pos()
    screen.blit(rescaled_bg_img, (0, 0))
    font = pygame.font.SysFont('Calibri', int(75 * aspect_ratio))
    options_text = font.render("Options", True, "White")
    screen.blit(options_text, (screen.get_width() / 2 - options_text.get_width() / 2, screen.get_height() / 2 - (219 * aspect_ratio)))
    pygame.draw.line(screen, "White", (325 * aspect_ratio, 262.5 * aspect_ratio), (775 * aspect_ratio, 262.5 * aspect_ratio), int(4 * aspect_ratio))
    optn_back_btn = pygame.rect.Rect(10, 10, 200 * aspect_ratio, 80 * aspect_ratio)
    pygame.draw.rect(screen, "White", optn_back_btn)

    options_back_button = Button(image=optn_back_btn, text_input="BACK", font=pygame.font.SysFont('Calibri',
                                        int(44 * aspect_ratio)), base_colour="Black", hovering_colour="Green")

    options_back_button.change_colour(options_mouse_pos)
    screen.blit(options_back_button.text, (options_back_button.image.centerx - options_back_button.text.get_width() / 2,
                                           options_back_button.image.centery - options_back_button.text.get_height() / 2))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if options_back_button.check_for_input(options_mouse_pos):
                return 1

    pygame.display.update()
    return 2

# Main menu screen
def main_menu(screen):
    menu_mouse_pos = pygame.mouse.get_pos()
    pygame.font.init()
    title_font = pygame.font.SysFont('Constantia', int(120 * aspect_ratio))
    version_font = pygame.font.SysFont('Consolas', int(20 * aspect_ratio))
    screen.blit(rescaled_bg_img, (0,0))

    # Buttons recting
    play_btn = pygame.rect.Rect(screen.get_width() / 2, screen.get_height() / 2 - 150, 750 * aspect_ratio, 75 * aspect_ratio)
    optn_btn = pygame.rect.Rect(screen.get_width() / 2 - 200, screen.get_height() / 2 - 50, 750 * aspect_ratio, 75 * aspect_ratio)
    quit_btn = pygame.rect.Rect(screen.get_width() / 2 - 200, screen.get_height() / 2 + 50, 750 * aspect_ratio, 75 * aspect_ratio)

    # Buttons centering
    play_btn.centerx = screen.get_width() / 2
    play_btn.centery = screen.get_height() / 2
    optn_btn.centerx = screen.get_width() / 2
    optn_btn.centery = screen.get_height() / 2 + (125 * aspect_ratio)
    quit_btn.centerx = screen.get_width() / 2
    quit_btn.centery = screen.get_height() / 2 + (250 * aspect_ratio)

    # Text/Image Display
    pygame.draw.rect(screen, "#191970", play_btn)
    pygame.draw.rect(screen, "#191970", optn_btn)
    pygame.draw.rect(screen, "#191970", quit_btn)

    menu_text = title_font.render("ChessPlus", True, "White")
    screen.blit(menu_text, ((screen.get_width() / 2 - menu_text.get_width() / 2), (screen.get_height() / 2) - 220 * aspect_ratio ))
    game_version_text = version_font.render("Version Alpha", True, "White")
    screen.blit(game_version_text, (screen.get_width() - (150 * aspect_ratio), screen.get_height() - (24 * aspect_ratio)))

    play_button = Button(image=play_btn, text_input="PLAY", font=pygame.font.SysFont('Calibri',
                            int(44 * aspect_ratio)), base_colour="White", hovering_colour="Green")
    options_button = Button(image=optn_btn, text_input="OPTIONS", font=pygame.font.SysFont('Calibri',
                            int(44 * aspect_ratio)), base_colour="White", hovering_colour = "Green")
    quit_button = Button(image=quit_btn, text_input="QUIT", font=pygame.font.SysFont('Calibri',
                            int(44 * aspect_ratio)), base_colour="White", hovering_colour="Green")

    for button in [play_button, options_button, quit_button]:
        button.change_colour(menu_mouse_pos)
        screen.blit(button.text, (button.image.centerx - button.text.get_width() / 2, button.image.centery - button.text.get_height() / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 4
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(menu_mouse_pos):
                return 3
            if options_button.check_for_input(menu_mouse_pos):
                return 2
            if quit_button.check_for_input(menu_mouse_pos):
                return 4

    pygame.display.flip()
    return 1